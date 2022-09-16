from ast import Delete
from django.http import JsonResponse
from .models import Cart, Order, Part, User
from .serializers import CartSerializer, OrderSerializer, PartSerializer, UserSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import sys
from datetime import datetime



#-------------------------------PART--------------------------------------------------------------------
@api_view(['GET', 'POST'])
def part_list(request):
    
    if request.method == 'GET':
        #get all the parts
        #serialize and return as a JSON
        parts = Part.objects.all()
        serializer = PartSerializer(parts, many = True)
        return JsonResponse({'data': serializer.data})
    
    if request.method == 'POST':
        #Save new part
        serializer = PartSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'msg':'data saved', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'save new part failed'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def part_details(request, id):
    try:
        part = Part.objects.get(pk=id)
        
    except Part.DoesNotExist:
        return JsonResponse({'msg':'No such part available'}, status=status.HTTP_404_NOT_FOUND)

    #Get details of a certain part
    if request.method == 'GET':
        serializer = PartSerializer(part)
        return JsonResponse({'data': serializer.data}, status = status.HTTP_200_OK)



#--------------------------------USER-------------------------------------------------------------------
@api_view(['GET', 'POST'])
def user_list(request):
    
    if request.method == 'GET':
        #get all the users
        #serialize and return as a JSON
        users = User.objects.all()
        serializer = UserSerializer(users, many = True)
        return JsonResponse({'data': serializer.data})
    
    if request.method == 'POST':
        #Save new user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'msg':'data saved', 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return JsonResponse({'error': 'user creation failed'}, status=status.HTTP_400_BAD_REQUEST)



#-----------------------------CART------------------------------------------------------------------------
@api_view(['GET', 'PUT', 'DELETE'])
def user_cart(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
    except:
        return JsonResponse({'error': "failed to find user"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        #Add new part to the cart
        if user:
            user_id = user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
                if cart:
                    parts = [str(element) for element in cart.parts.split(",")]

                    if not str(request.data['part_id']) in parts:
                        parts.append(str(request.data['part_id']))
                    else:
                        pass

                    cart.parts = ",".join(parts)
                    serializer = CartSerializer(cart, data = cart.__dict__)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'msg':'data updated', 'data':serializer.data, 'user':user.name}, status=status.HTTP_202_ACCEPTED)
                    return JsonResponse({'error': "failed to update data"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                cart = Cart.create(user_id=user_id)
                parts = []
                parts.append(str(request.data['part_id']))

                cart.parts = ",".join(parts)
                serializer = CartSerializer(cart, data = cart.__dict__)
                if serializer.is_valid():
                    serializer.save()
                    return JsonResponse({'msg':'data updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
                return JsonResponse({'error': "failed to update data"}, status=status.HTTP_400_BAD_REQUEST)
        return JsonResponse({'error':'an error occured'}, status=status.HTTP_400_BAD_REQUEST)
            
    if request.method == 'GET':
        #get all the items in user's cart
        if user:
            user_id = user.id
            try:
                cart = Cart.objects.get(user_id=user_id)
                if cart:
                    serializer = CartSerializer(cart)
                    return JsonResponse({'data': serializer.data})
                else:
                    return JsonResponse({'data': {}})
            except:
                cart = None
                return JsonResponse({'error':'cart not available'}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'error':'an error occured'}, status=status.HTTP_400_BAD_REQUEST)
    
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
                        return JsonResponse({'error':'item not available in the cart'}, status=status.HTTP_400_BAD_REQUEST)

                    cart.parts = ",".join(parts)
                    if len(parts) == 0:
                        Cart.objects.filter(user_id=user_id).delete()
                        return JsonResponse({'msg':'all data in cart deleted'}, status=status.HTTP_202_ACCEPTED)
                    serializer = CartSerializer(cart, data = cart.__dict__)
                    if serializer.is_valid():
                        serializer.save()
                        return JsonResponse({'msg':'data updated', 'data':serializer.data, 'user':user.name}, status=status.HTTP_202_ACCEPTED)
                    return JsonResponse({'error': "failed to update data"}, status=status.HTTP_400_BAD_REQUEST)
            except:
                cart = None
                return JsonResponse({'error':'cart not available to remove item'}, status=status.HTTP_404_NOT_FOUND)
        return JsonResponse({'error':'an error occured'}, status=status.HTTP_400_BAD_REQUEST)


#----------------------------------------ORDERS-------------------------------------------------------------------------
@api_view(['POST'])
def purchase(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
        user_id = user.id
    except:
        return JsonResponse({'error': "failed to find user"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        #Purchase items in current cart
        cart = Cart.objects.get(user_id=user_id)
        if cart:
            order = Order.create(user_id=user.id, parts=cart.parts)
            serializer = OrderSerializer(data = order.__dict__)
            if serializer.is_valid():
                serializer.save()
                Cart.objects.filter(user_id=user_id).delete()
                return JsonResponse({'msg':'new order created, please update delivery time', 'data':serializer.data, 'user':user.name}, status=status.HTTP_202_ACCEPTED)
            return JsonResponse({'error': "failed to create order", "error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return JsonResponse({'error': "No cart available to create order"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def order(request):
    try:
        user = User.objects.get(id=request.data['user_id'])
        user_id = user.id
    except:
        return JsonResponse({'error': "failed to find user"}, status=status.HTTP_404_NOT_FOUND)
    
    #return all orders of the given user
    orders = Order.objects.filter(user_id = user_id)
    serializer = OrderSerializer(orders, many = True)
    return JsonResponse({'data': serializer.data})
        
@api_view(['POST'])
def update_order(request):
    try:
        order = Order.objects.get(id=request.data['order_id'], user_id = request.data['user_id'])
    except:
        return JsonResponse({'error': "failed to find order"}, status=status.HTTP_404_NOT_FOUND)
    
    try:
        #Update delivery time of the order
        date_time = request.data['date'] + "  " + request.data['time']
        order.delivery_time = datetime.strptime(str(date_time), '%b %d %Y %I:%M %p')

        serializer = OrderSerializer(order, data = order.__dict__)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'msg':'delivery date updated', 'data':serializer.data}, status=status.HTTP_202_ACCEPTED)
        return JsonResponse({'error': "failed to update delivery date"}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return JsonResponse({'msg': "an error occurred enter date in 'month day year' format and time in 'H:M AM/PM' format "}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JsonResponse({'msg': "an error occurred enter date and time values "}, status=status.HTTP_400_BAD_REQUEST)
    except TypeError:
        return JsonResponse({'msg': "an error occurred enter date and time values as strings"}, status=status.HTTP_400_BAD_REQUEST)
    except:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        return JsonResponse({'msg': 'an error occurred', 'error':str(exc_type)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
