from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render , redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.models import User
# from cinema.ticketing.models import *
from .models import Payment
from .forms import PaymentModelForm, ProfileModelForm, MyUserForm


# Create your views here.


def login_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Successful login
            login(request, user)
            redirect_url = next_url if next_url else reverse('ticketing:showtime_list')
            return HttpResponseRedirect(redirect_url)
        else:
            # undefined user or wrong password
            context = {
                'username': username,
                'error': 'کاربری با این مشخصات یافت نشد'
            }
    context = {}
    return render(request, 'accounts/login.html', context)



def logout_view(request):
    logout(request)     # from django.contrib.auth import authenticate, login, logout
    # return HttpResponseRedirect(reverse('accounts:login'))
    return redirect('accounts:login')


# ثبت نام کردن (از ویدیوی Udemy آورده شده است)

# نکته : قسمت سیو کردن پسورد مشکل دارد.
def register(request):
    if request.method == 'POST':
        #Get form values:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        user_name = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        #Check if passwords match
        if password==password2:
            if User.objects.filter(username=user_name).exists():
                messages.ERROR(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.ERROR(request, 'Email is being used')
            # if everything ok
            else:
                user = User(username= user_name, password=password,
                         first_name=first_name, last_name=last_name,
                         email=email
                         )
                user.save()
                messages.success(request, 'You are now registered and cant log in')
                return redirect('accounts:login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('accounts:register')
    else:
        template_name = 'accounts/register.html'
        context = {}
        return render(request, template_name, context)


@login_required
def profile_details(request):
    profile = request.user.profile
    context = {
        'profile' : profile
    }
    template_name = 'accounts/profile_details.html'
    return render(request, template_name, context)


## PAYMENTS ##

@login_required()
def payment_list(request):
    template_name = 'accounts/payment_list.html'
    payments = Payment.objects.filter(profile=request.user.profile)
    context = {'payments': payments}
    return render(request, template_name, context)

@login_required
def payment_details(request, payment_id):
    template_name = 'accounts/payment_details.html'
    payment = Payment.objects.filter(pk=payment_id).first()
    # payment = get_object_or_404(Payment, pk=payment_id)
    context = {'payment': payment}
    return render(request, template_name, context)

@login_required
def payment_create(request):
    template_name = 'accounts/payment_create.html'
    if request.method == 'POST':
        form = PaymentModelForm(request.POST, request.FILES)
        if form.is_valid():
            payment = form.save(commit=False)     # این خط به تنهایی کل فرم را سیو میکند.
            payment.profile = request.user.profile      # changing a field,s value manually
            payment.save()  #saving in database
            request.user.profile.deposit(payment.amount)    #(اسم تابعی که خودمان تعریف کردیم،  deposit است. ) اضافه کردن پول به اکانت(پروفایل) شخص
            return redirect('accounts:payment_list')

            # payment.profile = form.cleaned_data['profile']
            # payment.amount = form.cleaned_data['amount']
            # payment.transaction_code = form.cleaned_data['transaction_code']
            # payment.save()
    else:
        form = PaymentModelForm()
    context = {'form': form}
    return render(request, template_name ,context)



@login_required
def profile_edit(request):
    if request.method == 'POST':
        profile_form = ProfileModelForm(request.POST,files=request.FILES ,instance=request.user.profile)  # قسمت instance برای لود کردن اطلاعات اولیه قبلی ، پیش از ویرایش فرم است.
        user_form = MyUserForm(request.POST, instance=request.user)
        if profile_form.is_valid() and user_form.is_valid():
            profile_form.save()
            user_form.save()
            return redirect('accounts:profile_details')
    else:
        profile_form = ProfileModelForm(instance=request.user.profile)
        user_form = MyUserForm(instance=request.user)
    template_name = 'accounts/profile_edit.html'
    context = {'profile_form': profile_form ,
               'user_form' : user_form
               }
    return render(request, template_name ,context)