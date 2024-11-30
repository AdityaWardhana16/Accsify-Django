from django.contrib import admin
from .models import Kategori, Product, Cart, CartItem, Order, OrderItem

# Register your models here.
# Kategori Admin
class KategoriAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at', 'updated_at',)  # Tampilkan kolom-kolom di daftar admin
    prepopulated_fields = {'slug': ('name',)}  # Otomatis mengisi slug berdasarkan nama
    search_fields = ('name', 'description')  # Fitur pencarian berdasarkan nama dan deskripsi
    list_filter = ('created_at',)  # Filter berdasarkan tanggal pembuatan

admin.site.register(Kategori, KategoriAdmin)

# Product Admin
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category', 'price', 'stock_produk', 'stock_diskon', 'created_at', 'updated_at', 'is_active')  # Kolom yang ditampilkan
    prepopulated_fields = {'slug': ('name',)}  # Otomatis mengisi slug berdasarkan nama
    list_filter = ('is_active', 'created_at', 'category')  # Filter berdasarkan status aktif, kategori, dan tanggal
    search_fields = ('name', 'description', 'category__name')  # Pencarian berdasarkan nama produk, deskripsi, dan kategori
    
admin.site.register(Product, ProductAdmin)

# Cart Admin
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'created_at')  # Menampilkan user dan tanggal pembuatan
    search_fields = ('user__username',)  # Pencarian berdasarkan username user

admin.site.register(Cart, CartAdmin)

# CartItem Admin
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'quantity')  # Menampilkan cart, produk, dan jumlah
    search_fields = ('cart__id', 'product__name')  # Pencarian berdasarkan ID cart dan nama produk

admin.site.register(CartItem, CartItemAdmin)

# Order Admin
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'order_date', 'status', 'total_amount')  # Menampilkan user, tanggal order, status, dan total harga
    list_filter = ('status', 'order_date')  # Filter berdasarkan status dan tanggal order
    search_fields = ('user__username',)  # Pencarian berdasarkan username user

admin.site.register(Order, OrderAdmin)

# OrderItem Admin
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity', 'price')  # Menampilkan order, produk, jumlah, dan harga
    search_fields = ('order__id', 'product__name')  # Pencarian berdasarkan ID order dan nama produk
    
admin.site.register(OrderItem, OrderItemAdmin)