from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from store_app import views
from django.contrib.staticfiles.storage import staticfiles_storage
from django.views.generic.base import RedirectView
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'),
    path('base/', views.BaseFile, name='base'),
    path('login/', views.Login, name='login'),
    path('logout/', views.Logout, name='logout'),
    path('signup/', views.Signup, name='signup'),
    path('about/', views.About, name='about'),
    path('contact/', views.ContactUs, name='Contact-Us'),
    path('product/<slug:pk>', views.ProductDetail, name='Product-Detail'),
    path('store/', views.Store, name='Store'),
    path('cart/', views.CartDetail, name='cart'),
    path('address/', views.Address_detail, name='Address'),
    path('thanks/', views.ThankYou, name='ThankYou'),
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('img/favicon.ico'))),

    # cart
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    # social
    path('accounts/', include('allauth.urls')), 

]  + static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
