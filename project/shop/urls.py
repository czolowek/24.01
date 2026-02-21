from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('add/<int:product_id>/', views.add_to_basket),
    path('basket/', views.basket_view),
    path('basket-plus/<int:product_id>/', views.basket_plus),
    path('basket-minus/<int:product_id>/', views.basket_minus),
    path('product/<int:product_id>/', views.product_page),
    path('product/<int:product_id>/add-comment/', views.add_comment_ajax),
    path('api/products/', views.ProductListApi.as_view()),
    path('rest-front/', views.rest_front),
]
