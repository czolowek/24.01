from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Basket, Comment
from .forms import CommentForm
from .serializers import ProductSerializer
import json

def home(request):
    products = Product.objects.all()
    return render(request, 'index.html', {'products': products})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
    return render(request, 'login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        p1 = request.POST.get('password1', '')
        p2 = request.POST.get('password2', '')
        if p1 == p2 and username:
            user = User.objects.create_user(username=username, email=email, password=p1)
            login(request, user)
            return redirect('/')
    return render(request, 'register.html')

def logout_view(request):
    logout(request)
    return redirect('/')

@login_required
def add_to_basket(request, product_id):
    product = Product.objects.get(id=product_id)
    item, created = Basket.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.count += 1
        item.save()
    return redirect('/')

@login_required
def basket_view(request):
    items = Basket.objects.filter(user=request.user)
    return render(request, 'basket.html', {'items': items})

@login_required
def basket_plus(request, product_id):
    item = Basket.objects.get(user=request.user, product_id=product_id)
    item.count += 1
    item.save()
    return redirect('/basket/')

@login_required
def basket_minus(request, product_id):
    item = Basket.objects.get(user=request.user, product_id=product_id)
    if item.count > 1:
        item.count -= 1
        item.save()
    else:
        item.delete()
    return redirect('/basket/')

def product_page(request, product_id):
    product = Product.objects.get(id=product_id)
    comments = Comment.objects.filter(product=product).order_by('-created')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('/login/')
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                product=product,
                user=request.user,
                text=form.cleaned_data['text']
            )
            return redirect(f'/product/{product_id}/')
    else:
        form = CommentForm()
    return render(request, 'product.html', {
        'product': product,
        'comments': comments,
        'form': form
    })

@login_required
@csrf_exempt
def add_comment_ajax(request, product_id):
    if request.method == 'POST':
        data = json.loads(request.body)
        product = Product.objects.get(id=product_id)
        c = Comment.objects.create(
            product=product,
            user=request.user,
            text=data.get('text', '')
        )
        return JsonResponse({'user': c.user.username, 'text': c.text})
    return JsonResponse({'error': 'Invalid method'}, status=400)

class ProductListApi(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = ProductSerializer(products, many=True).data
        return Response(data)

def rest_front(request):
    return render(request, 'rest_front.html')
