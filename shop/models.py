#apabila belum memiliki APP, silahkan membuatnya terlebih dahulu.
# python manage.py startapp shop

from django.db import models
from django.utils.text import slugify
from django.conf import settings



class Kategori(models.Model):
    name = models.CharField(max_length=25, unique=True, verbose_name="Nama Kategori")
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")
    #price = models.DecimalField(blank=False)

    class Meta:
        verbose_name = "Kategori"
        verbose_name_plural = "Kategori"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Nama Produk")
    slug = models.SlugField(max_length=50, unique=True, blank=True)
    description = models.TextField(verbose_name="Deskripsi", blank=True)
    price = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Harga")
    category = models.ForeignKey('Kategori', on_delete=models.CASCADE, related_name='products', verbose_name="Kategori")
    stock_produk = models.PositiveIntegerField(verbose_name="Stok")
    stock_diskon = models.PositiveIntegerField(verbose_name="Stok Diskon")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui pada")
    merek_produk = models.CharField(max_length=50)
    bahan = models.CharField(max_length=50, default='Tidak Diketahui')
    is_active = models.BooleanField(default=True, verbose_name="Aktif")
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)



    class Meta:
        verbose_name = "Produk"
        verbose_name_plural = "Produk"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
from django.db import models
from django.conf import settings
from .models import Product

class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

    def total_price(self):
        return sum(item.total_price() for item in self.items.all())  # Menggunakan related_name 'items'

    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # Perbaikan di sini
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} of {self.product.name}"

    def total_price(self):
        return self.product.price * self.quantity


    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, related_name='orders')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('SHIPPED', 'Shipped'), ('DELIVERED', 'Delivered')])

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} for order {self.order.id}"
