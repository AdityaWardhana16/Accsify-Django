from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.views.generic import ListView, DetailView
from .models import Kategori, Product, Cart, Order, OrderItem
from .forms import AddToCartForm  # Jika menggunakan forms.py untuk validasi input
from django.shortcuts import render, get_object_or_404
from .models import Cart, CartItem

# List dan Detail untuk Kategori dan Produk
class KategoriListView(ListView):
    model = Kategori
    template_name = 'shop/kategori_list.html'
    context_object_name = 'kategoris'

class ProductListView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Kategori.objects.all()  # Mengirimkan kategori ke template
        return context

# View untuk menampilkan produk berdasarkan kategori
class ProductListByCategoryView(ListView):
    model = Product
    template_name = 'shop/product_list.html'
    context_object_name = 'products'

    def get_queryset(self):
        category_slug = self.kwargs['slug']
        return Product.objects.filter(category__slug=category_slug)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Kategori.objects.all()  # Mengirimkan kategori ke template
        return context

# View untuk menampilkan detail produk (gunakan DetailView)
class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product_detail.html'
    context_object_name = 'product'

    def get_object(self):
        return get_object_or_404(Product, slug=self.kwargs['slug'])

# Keranjang Detail (Menampilkan keranjang belanja pengguna)
from django.http import Http404
from .models import Cart, CartItem

class CartDetailView(DetailView):
    model = Cart
    template_name = 'shop/cart_detail.html'
    context_object_name = 'cart'

    def get_object(self):
        try:
            return Cart.objects.get(user=self.request.user)
        except Cart.DoesNotExist:
            raise Http404("Cart does not exist")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = self.get_object()
        context['total_price'] = cart.total_price()  # Menambahkan total harga ke context
        return context
    
    def remove_from_cart(request, cart_item_id):
        cart_item = get_object_or_404(CartItem, id=cart_item_id, cart__user=request.user)
        cart_item.delete()
        return redirect('cart_detail')
    

    def product_detail(request, slug):
        product = get_object_or_404(Product, slug=slug)
        return render(request, 'shop/product_detail.html', {'product': product})


from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, CartItem

@login_required
@login_required
def cart_detail(request):
    # Ambil keranjang belanja milik pengguna yang sedang login
    cart = Cart.objects.get(user=request.user, is_active=True)
    
    # Hitung total harga produk dalam keranjang
    total_price = cart.calculate_total()

    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'total_price': total_price,
    })
def add_to_cart(request, product_id):
    # Ambil produk berdasarkan ID
    product = get_object_or_404(Product, id=product_id)

    # Ambil quantity dari form, set default 1 jika tidak ada atau invalid
    try:
        quantity = int(request.POST.get('quantity', 1))  # Default 1 jika tidak ada quantity
    except ValueError:
        quantity = 1  # Jika ada error saat konversi, set ke 1

    # Validasi quantity tidak melebihi stok yang tersedia
    if quantity > product.stock_produk:
        messages.error(request, f"Jumlah yang diminta melebihi stok yang tersedia. Stok produk: {product.stock_produk}.")
        return redirect('product_detail', slug=product.slug)

    # Ambil atau buat keranjang belanja untuk user
    cart, _ = Cart.objects.get_or_create(user=request.user)

    # Periksa apakah produk sudah ada dalam keranjang
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        # Jika produk sudah ada, tambahkan kuantitasnya
        cart_item.quantity += quantity
        cart_item.save()
        messages.success(request, f'Produk {product.name} telah diperbarui di keranjang.')
    else:
        # Jika produk baru, set kuantitasnya
        cart_item.quantity = quantity
        cart_item.save()
        messages.success(request, f'Produk {product.name} telah ditambahkan ke keranjang.')

    # Redirect ke halaman keranjang setelah menambah produk
    return redirect('cart_detail')

# Order List dan Detail
class OrderListView(ListView):
    model = Order
    template_name = 'shop/order_list.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(DetailView):
    model = Order
    template_name = 'shop/order_detail.html'
    context_object_name = 'order'

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise Http404("You are not authorized to view this order.")
        return obj

# Logika untuk Menambah Produk ke Keranjang
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    # Jika form digunakan untuk menambah produk
    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            # Menggunakan session untuk menyimpan keranjang
            request.session.setdefault('cart', {})
            cart = request.session['cart']

            # Menambahkan produk ke keranjang
            if product_id in cart:
                cart[product_id] += quantity
            else:
                cart[product_id] = quantity
            
            request.session.modified = True

    return redirect('shop:cart_detail')  # Redirect ke halaman cart_detail setelah produk ditambahkan
