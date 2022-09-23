from django.http import JsonResponse
from .models import Cart, Order, Part
from users.models import MyUser as User
from autocompany.serializers import CartSerializer, OrderSerializer, PartSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import sys
from datetime import datetime



#-------------------------------PART--------------------------------------------------------------------
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def part_list(request):
    
    if request.method == 'GET':
        #get all the parts
        #serialize and return as a JSON
        parts = Part.objects.all()
        serializer = PartSerializer(parts, many = True)
        return Response({'data': serializer.data})
    
    if request.method == 'POST':
        #Save new part
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'data saved', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'error': 'save new part failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def part_details(request, id):
    try:
        part = Part.objects.get(pk=id)
        
    except Part.DoesNotExist:
        return Response({'msg':'No such part available'}, status=status.HTTP_404_NOT_FOUND)

    #Get details of a certain part
    if request.method == 'GET':
        serializer = PartSerializer(part)
        return Response({'data': serializer.data}, status = status.HTTP_200_OK)





#-----------------------------CART------------------------------------------------------------------------
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_cart(request):
    try:
        user = User.objects.get(id=request.user.id)
    except:
        return Response({'error': "failed to find user", "user": request.user.id}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        #Add new part to the cart
        if user:
            user_id = user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
                if cart:
                    parts = [str(element) for element in cart.parts.split(",")]

                    if not str(request.data['part_id']) in parts:
                        try:
                            part_val = Part.objects.get(id=request.data['part_id'])
                        except:
                            return Response({'error': "No such part available"}, status=status.HTTP_404_NOT_FOUND)
                        parts.append(str(request.data['part_id']))
                    else:
                        pass

                    cart.parts = ",".join(parts)
                    serializer = CartSerializer(cart, data = cart.__dict__)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'msg':'data updated', 'data':serializer.data, 'user':user.name}, status=status.HTTP_202_ACCEPTED)
                    return Response({'error': "failed to update data"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                cart = Cart.create(user_id=user_id)
                parts = []
                parts.append(str(request.data['part_id']))

                cart.parts = ",".join(parts)
                serializer = CartSerializer(cart, data = cart.__dict__)
                if serializer.is_valid():
                    serializer.save()
                    return Response({'msg':'data updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
                return Response({'error': "failed to update data"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error':'an error occured'}, status=status.HTTP_400_BAD_REQUEST)
            
    if request.method == 'GET':
        #get all the items in user's cart
        if user:
            user_id = user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
                if cart:
                    serializer = CartSerializer(cart)
                    return Response({'data': serializer.data})
                else:
                    return Response({'data': {}})
            except:
                cart = None
                return Response({'error':'cart not available'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error':'an error occured'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'DELETE':
        #remove part from cart
        if user:
            user_id = user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
                if cart:
                    parts = [str(element) for element in cart.parts.split(",")]

                    if str(request.data['part_id']) in parts:
                        parts.remove(str(request.data['part_id']))
                    else:
                        return Response({'error':'item not available in the cart'}, status=status.HTTP_400_BAD_REQUEST)

                    cart.parts = ",".join(parts)
                    if len(parts) == 0:
                        Cart.objects.filter(user_id=user_id).delete()
                        return Response({'msg':'all data in cart deleted'}, status=status.HTTP_202_ACCEPTED)
                    serializer = CartSerializer(cart, data = cart.__dict__)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({'msg':'data updated', 'data':serializer.data, 'user':user.name}, status=status.HTTP_202_ACCEPTED)
                    return Response({'error': "failed to update data"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                cart = None
                return Response({'error':'cart not available to remove item'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'error':'an error occured'}, status=status.HTTP_400_BAD_REQUEST)


#----------------------------------------ORDERS-------------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase(request):
    try:
        user = User.objects.get(id=request.user.id)
        user_id = user.id
    except:
        return Response({'error': "failed to find user"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        #Purchase items in current cart
        cart = Cart.objects.get(user_id=user_id)
        if cart:
            order = Order.create(user_id=user.id, parts=cart.parts)
            serializer = OrderSerializer(data = order.__dict__)
            if serializer.is_valid():
                serializer.save()
                Cart.objects.filter(user_id=user_id).delete()
                return Response({'msg':'new order created, please update delivery time', 'data':serializer.data, 'user':user.name}, status=status.HTTP_202_ACCEPTED)
            return Response({'error': "failed to create order", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return Response({'error': "No cart available to create order"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order(request):
    try:
        user = User.objects.get(id=request.user.id)
        user_id = user.id
    except:
        return Response({'error': "failed to find user"}, status=status.HTTP_404_NOT_FOUND)
    
    #return all orders of the given user
    orders = Order.objects.filter(user_id = user_id)
    serializer = OrderSerializer(orders, many = True)
    return Response({'data': serializer.data})
    
        
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_order(request):
    try:
        order = Order.objects.get(id=request.data['order_id'], user_id = request.user.id)
    except:
        return Response({'error': "failed to find order"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        #Update delivery time of the order
        date_time = request.data['date'] + "  " + request.data['time']
        order.delivery_time = datetime.strptime(str(date_time), '%b %d %Y %I:%M %p')

        serializer = OrderSerializer(order, data = order.__dict__)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'delivery date updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        return Response({'error': "failed to update delivery date"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'msg': "an error occurred enter date in 'month day year' format and time in 'H:M AM/PM' format "}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return Response({'msg': "an error occurred enter date and time values "}, status=status.HTTP_400_BAD_REQUEST)
    except TypeError:
        return Response({'msg': "an error occurred enter date and time values as strings"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return Response({'msg': 'an error occurred', 'error':str(exc_type)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

