import imp
from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import part_list, part_details, user_cart, purchase, order, update_order
from users.views import user_list, user_signup, MyTokenObtainPairView


class TestURLs(SimpleTestCase):
    def test_part_url(self):
        url = reverse('parts')
        self.assertEquals(resolve(url).func, part_list)
    
    def test_part_details_url(self):
        url = reverse('part_details', args='1')
        self.assertEquals(resolve(url).func, part_details)
    
    def test_user_list_url(self):
        url = reverse('user_list')
        self.assertEquals(resolve(url).func, user_list)
    
    def test_user_signup_url(self):
        url = reverse('user_signup')
        self.assertEquals(resolve(url).func, user_signup)

    def test_user_cart_url(self):
        url = reverse('user_cart')
        self.assertEquals(resolve(url).func, user_cart)
    
    def test_user_orders_url(self):
        url = reverse('orders')
        self.assertEquals(resolve(url).func, order)
    
    def test_purchase_url(self):
        url = reverse('purchase')
        self.assertEquals(resolve(url).func, purchase)
    
    def test_update_order_url(self):
        url = reverse('update')
        self.assertEquals(resolve(url).func, update_order)