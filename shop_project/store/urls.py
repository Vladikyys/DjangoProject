from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('product/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path("add-cartitem/<int:pk>/", views.AddCartItem.as_view(), name="add_cartitem"),
    path("cart/", views.CartItemList.as_view(), name="cart_item"),
    path("delete/<int:pk>/", views.RemoveCartItem.as_view(), name="del_item"),
    path("edit/<int:pk>/", views.EditCartItem.as_view(), name="edit_item"),
    path('search/', views.Search.as_view(), name='search'),
    path('orders/', views.OrderList.as_view(), name='orders')
]
