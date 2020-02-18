from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from .forms import CartItemForm
from django.contrib import messages
from django.views.generic.base import View
from shop_project import settings
from .models import Product, Cart, CartItem, Order, Genre
from django.db.models import Q
# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'shop/list-product.html'


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CartItemForm()
        return context
    


class AddCartItem(View):
    """Добавление в корзину"""
    def post(self, request, pk):
        quantity = request.POST.get('quantity', None)
        print(quantity)
        if quantity is not None and int(quantity)>0:
            try:
             cart = Cart.objects.get(user=request.user)
            except Cart.DoesNotExist:
                cart = Cart.objects.create(user=request.user)
            print(f'cart_user-{cart.user}, product_id-{pk}')
            try:
                item = CartItem.objects.get(cart__user=request.user, product_id=pk)
                print(f'item={item}')
                item.quantity += int(quantity)
            except CartItem.DoesNotExist:
                item = CartItem(cart=Cart.objects.get(user=request.user, accepted=False), product_id = pk, quantity=int(quantity))
            item.save()
            messages.add_message(request, settings.MY_INFO, 'Товар добавлен')
            return redirect('/product/{}/'.format(pk))
        else:
            messages.add_message(request, settings.MY_INFO, "Значение не может быть 0")
            return redirect('/product/{}/'.format(pk))


class CartItemList(ListView):
    """Товары в корзине пользователя"""
    template_name = 'shop/cart.html'

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user, cart__accepted=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum = 0
        for item in context['object_list']:
            sum += int(item.price_sum)
        context['sum'] = sum
        return context

    def post(self, request):
        item = Cart.objects.get(user=request.user)
        item.accepted = True
        item.save()
        messages.add_message(request, settings.MY_INFO, 'Товар добавлен в оформление')
        Cart.objects.create(user=request.user)
        Order.objects.create(cart=item)
        return redirect('orders')


class EditCartItem(View):
    """редактирование товара в корзине"""

    def post(self, request, pk):
        quantity = request.POST.get('quantity', None)
        if quantity:
            item = CartItem.objects.get(cart__user=request.user, id=pk)
            item.quantity = int(quantity)
            item.save()
        return redirect('cart_item')


class RemoveCartItem(View):
    """удаления товара с корзины"""

    def get(self, request, pk):
        CartItem.objects.get(cart__user=request.user, id=pk).delete()
        messages.add_message(request, settings.MY_INFO, "Товар удален")
        return redirect('cart_item')


class Search(View):
    """Поиск товаров"""

    def get(self, request):
        search = request.GET.get("search", None)
        products = Product.objects.filter(Q(name__icontains=search) |
                                          Q(category__name__icontains=search))
        return render(request, "shop/list-product.html", {"object_list": products})


class OrderList(ListView):
    """Список заказов пользователя"""
    template_name = 'shop/order-list.html'

    def get_queryset(self):
        return Order.objects.filter(cart__user=self.request.user, accepted=False)

    def post(self, request):
        order = Order.objects.get(cart__user=request.user, accepted=False)
        order.delete()
        cart = Cart.objects.get(accepted=True)
        cart.delete()
        return redirect('orders')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        sum = 0
        cart = CartItem.objects.filter(cart__user=self.request.user)
        for item in cart:
            sum += int(item.price_sum)
        context['sum'] = sum
        return context


class CategoryProduct(ListView):
    """Список товаров из категории"""
    template_name = "shop/list-product.html"

    def get_queryset(self):
        slug = self.kwargs.get("slug")
        node = Genre.objects.get(slug=slug)
        if Product.objects.filter(category__slug=slug).exists():
            products = Product.objects.filter(category__slug=slug)
        else:
            products = Product.objects.filter(category__slug__in=[x.slug for x in node.get_family()])
        return products