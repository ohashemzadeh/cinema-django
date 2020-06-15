from django.urls import path

from . import views
from .views import *



app_name = 'accounts' # for using in app urls #   path('ticketing/', include('ticketing.urls'))
urlpatterns = [
    path('login', views.login_view , name='login'),
    path('logout', views.logout_view, name='logout'),
    path('profile/details', views.profile_details, name='profile_details'),
    path('profile/edit', views.profile_edit, name='profile_edit'),

    path('register', views.register, name='register'),

    path('payment/list', payment_list, name='payment_list'),
    path('payment/details/<int:payment_id>', payment_details, name='payment_details'),
    path('payment/create', payment_create, name='payment_create'),

]