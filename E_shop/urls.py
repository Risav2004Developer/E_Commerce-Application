from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import veiws

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', veiws.HOME, name='home'),
    path('base/', veiws.BASE, name='base'),
    path('products/',veiws.PRODUCT, name='product'),
    path('search/',veiws.SEARCH, name='search'),
    path('register/',veiws.HANDLEREGISTER, name='register'),
    path('login/',veiws.HANDLELOGIN, name='login'),
    path('logout/', veiws.HANDLELOGOUT, name='logout'),


    #cart
    path('cart/add/<int:id>/', veiws.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', veiws.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         veiws.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         veiws.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', veiws.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',veiws.cart_detail,name='cart_detail'),
    path('cart/checkout/',veiws.checkout,name='checkout'),
    path('cart/checkout/placeorder', veiws.PLACE_ORDER, name='place_order'),
    path('success', veiws.SUCCESS, name='success')

              ] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
