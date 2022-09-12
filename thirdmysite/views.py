from django.contrib.auth import login, authenticate
from django.core.mail import send_mail, BadHeaderError
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import F, Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.list import BaseListView

from thirdmysite.form import ReviewsForm, ContactForm, SignUpForm, SignInForm
from thirdmysite.models import Product, Category


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


def cart(request):
    return render(request, 'blog/sb/cart.html')


def checkout(request):
    return render(request, 'blog/sb/checkout.html')