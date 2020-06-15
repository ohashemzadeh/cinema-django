from django.contrib import admin
from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'ticketing' # for using in app urls #   path('ticketing/', include('ticketing.urls'))
urlpatterns = [
    path('movie/list', movie_list , name='movie_list'),
    path('movie/details/<int:movie_id>', movie_details, name='movie_details'),
    path('cinema/list', cinema_list , name='cinema_list'),
    path('cinema/details/<int:cinema_id>', cinema_details, name='cinema_details'),
    path('showtime/list', showtime_list , name='showtime_list'),
    path('showtime/details/<int:showtime_id>', showtime_details, name='showtime_details'),
    path('ticket/list', ticket_list, name='ticket_list'),
    path('ticket/details/<int:ticket_id>', ticket_details, name='ticket_details'),

]
 # + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)