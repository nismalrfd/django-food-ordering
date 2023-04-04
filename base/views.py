from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


from base.models import *

from instamojo_wrapper import Instamojo
from django.conf import settings

api = Instamojo(api_key=settings.API_KEY,
                auth_token=settings.AUTH_TOKEN, endpoint='https://test.instamojo.com/api/1.1/')


# Create your views here.
def home(request):
    pizza = Pizza.objects.all()
    search_in = request.GET.get('search-area')
    if search_in:
        pizza = Pizza.objects.filter(pizza_name__icontains=search_in)
    else:
        pizza = Pizza.objects.all()
        search_in = ''
    context = {
        'pizza': pizza,
        'search_in': search_in
    }
    return render(request, 'index.html', context)


def login_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)
            if not user_obj.exists():
                messages.warning(request, 'User not Found ')
                return redirect('/login')
            user_obj = authenticate(username=username, password=password)
            if user_obj:
                login(request, user_obj)
                return redirect('/')

            messages.warning(request, 'wrong password ')
            return redirect('login')

        except Exception as e:
            messages.warning(request, 'Something went wrong')

    return render(request, 'login.html')


def register_page(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')

            user_obj = User.objects.filter(username=username)
            if user_obj.exists():
                messages.warning(request, 'username already exists')
                return redirect('/register')
            user_obj = User.objects.create(username=username)
            user_obj.set_password(password)
            user_obj.save()

            messages.success(request, 'Account created')
            return redirect('login')
        except Exception as e:
            messages.warning(request, 'Something went wrong')

    return render(request, 'register.html')


@login_required(login_url='/login/')
def add_cart(request, id):
    user = request.user

    pizza_obj = Pizza.objects.get(id=id)
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_items = CartItems.objects.create(
        cart= cart,
        pizza= pizza_obj
    )
    return redirect('/')


@login_required(login_url='/login/')
def cart(request):
    try:
        cart = Cart.objects.get(is_paid=False, user=request.user)

        response = api.payment_request_create(
            amount=cart.get_cart_total(),
            purpose='order',
            buyer_name=request.user.username,
            email='nismalr32@gmail.com',
            redirect_url='http://127.0.0.1:9000/success/'
        )
        cart.instamojo_id = response['payment_request']['id']
        cart.save()

        # if request.mrthod == 'POST':
        #     coupon = request.POST.get('coupon')
        #     coupon_obj = Coupon.objects.filter(coupon_code_icontains=coupon)
        #     if coupon_obj.exists():
        #         messages.warning(request, "invalid coupon...")
        #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        #     if cart.coupon:
        #         messages.warning(request, " coupon already exists ...")
        #         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        #     cart.coupon = coupon_obj[0]
        #     cart.save()
        #     messages.warning(request, " coupon applied ...")
        #     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        context = {
            'cart': cart,
            'payment_url': response['payment_request']['longurl']
        }
        return render(request, 'cart.html', context)
    except:
        messages.warning(request, "Empty Cart .......!")
        return redirect('/')





@login_required(login_url='/login/')
def remove_cart_items(request, pk):
    try:
        CartItems.objects.get(id=pk).delete()
        return redirect('/cart')
    except Exception as e:
        print(e)


@login_required(login_url='/login/')
def orders(request):
    orders = Cart.objects.filter(is_paid=True, user=request.user)
    context = {
        'orders': orders
    }
    messages.success(request, 'order successfully placed')
    return render(request, 'orders.html', context)


@login_required(login_url='/login/')
def success(request):
    payment_request = request.GET.get('payment_request_id')
    cart = Cart.objects.get(instamojo_id=payment_request)
    cart.is_paid = True
    cart.save()
    return redirect('orders')


def logout_view(request):
    logout(request)
    return redirect('login')

# def process_payment(request):
