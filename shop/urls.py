from django.urls import path
from . import views

app_name = 'shop'  # Menambahkan app_name di sini

urlpatterns = [
    path('kategori/', views.KategoriListView.as_view(), name='kategori_list'),
    path('', views.ProductListView.as_view(), name='product_list'),  # Ini menangani path kosong
    path('produk/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('keranjang/', views.CartDetailView.as_view(), name='cart_detail'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('pesanan/', views.OrderListView.as_view(), name='order_list'),
    path('pesanan/<int:id>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('kategori/<slug:slug>/', views.ProductListByCategoryView.as_view(), name='product_list_by_category'),
]
