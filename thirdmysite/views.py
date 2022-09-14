from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.list import BaseListView
from django.contrib import messages

from thirdmysite.form import ReviewsForm, ContactForm, SignUpForm, SignInForm
from thirdmysite.models import Product, Category, OrderItem, Order


class Products(ListView):
    model = Product
    paginate_by = 8
    template_name = 'blog/sb/index.html'
    context_object_name = 'product'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        return context


class GetCategoryPage(ListView):
    template_name = 'blog/sb/category_page.html'
    context_object_name = 'posts'
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(category__slug=self.kwargs['slug'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Posts by category: {Category.objects.get(slug=self.kwargs["slug"])}'
        return context

class Detail(DetailView):
    model = Product
    template_name = 'blog/sb/detail.html'
    context_object_name = 'detail'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_post'] = Product.objects.all().order_by('id')[:5]
        self.object.view = F('view') + 1
        self.object.save()
        self.object.refresh_from_db()
        return context


class Contact(ListView):
    model = Product
    template_name = 'blog/sb/contact.html'
    context_object_name = 'contact'


class Shop(ListView):
    model = Product
    template_name = 'blog/sb/shop.html'
    context_object_name = 'product'
    paginate_by = 10


class Shop20(ListView):
    model = Product
    template_name = 'blog/sb/shop.html'
    context_object_name = 'product'
    paginate_by = 20

    def get_paginate_by(self, queryset):
        return self.request.GET.get("paginate_by", self.paginate_by)


class AddReview(View):
    def post(self, request, pk):
        form = ReviewsForm(request.POST)
        product = Product.objects.get(id=pk)
        if form.is_valid:
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.product = product
            form.save()
        return redirect('index')


# class ContactView(View):
def contactView(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'blog/froma.html')
    form = ContactForm()
    context = {'form': form}
    return render(request, 'blog/sb/contact.html', context)


class SignUpView(View):
    def get(self, request, *args, **kwargs):
        form = SignUpForm()
        return render(request, 'blog/sb/signup.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/sb/signup.html', context={
            'form': form,
        })

class SignInView(View):
    def get(self, request, *args, **kwargs):
        form = SignInForm()
        return render(request, 'blog/sb/signin.html', context={
            'form': form
        })

    def post(self, request, *args, **kwargs):
        form = SignInForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'blog/sb/signin.html', context={
            'form': form,
        })


class Cart(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'order': order
            }
            return render(self.request, 'blog/sb/cart.html', context)
        except ObjectDoesNotExist:
            messages.error(self.request, "You don't have an active order.")
            return redirect('/')


def checkout(request):
    return render(request, 'blog/sb/checkout.html')

@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_item, create = OrderItem.objects.get_or_create(item=item, user=request.user, ordered=False)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'This item quantity was updated!')
        else:
            messages.info(request, 'This item was added to your cart!')
            order.items.add(order_item)
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, 'This item was added to your cart!')
    return redirect('cart')

@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request, 'This item was removed from your cart!')
            return redirect('cart')
        else:
            messages.info(request, 'This item was not in your cart!')
            return redirect('cart')

    else:
        messages.info(request, 'You don\'t have an active order!')
        return redirect('cart')

@login_required
def remove_single_item_from_cart(request, slug):
    item = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(user=request.user, ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)
            messages.info(request, 'This item quantity was updated')
            return redirect('cart')
        else:
            messages.info(request, 'This item was not in your cart!')
            return redirect('cart')

    else:
        messages.info(request, 'You don\'t have an active order!')
        return redirect('cart')
