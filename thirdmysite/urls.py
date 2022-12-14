from django.conf import settings

from .views import *
from django.urls import path
from django.contrib.auth.views import LogoutView

# app_name = 'thirdmysite'

urlpatterns = [
    path('', Products.as_view(), name='index'),
    path('shop/', Shop.as_view(), name='shop'),
    path('detail/<slug:slug>/', Detail.as_view(), name='detail'),
    path('contact/', contactView, name='contact'),
    path('checkout/', checkout, name='checkout'),
    path('cart/', Cart.as_view(), name='cart'),
    path('shop/?paginate_by=10', Shop.as_view(), name='shop'),
    path('shop/?paginate_by=20', Shop20.as_view(), name='shop20'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('signin/', SignInView.as_view(), name='signin'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('signout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='signout'),
    path('category/<slug:slug>', GetCategoryPage.as_view() , name='category'),
    path('add-to-cart/<slug:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug:slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove_single/<slug:slug>', remove_single_item_from_cart, name='remove_single')
]