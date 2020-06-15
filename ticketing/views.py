from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render , redirect
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from .models import Movie, ShowTime, Cinema, Ticket
from .forms import *
from django.urls import reverse
from django.contrib.humanize.templatetags.humanize import *

# Create your views here.


def index(request):
    template_name = 'ticketing/index.html'
    x = intcomma(40000000)
    context = {'x':x}
    return render(request, template_name, context)



def mytest(request):
    # return HttpResponseRedirect(reverse('ticketing:movie_list'))
    return redirect('ticketing:movie_list')

def movie_list(request):
    movies = Movie.objects.all()
    movie_count = len(movies)
    # movie_count = Movie.objects.count()
    template_name = 'ticketing/movie_list.html'
    context = {
        'movie_list' : movies,
        'movie_count' : movie_count,
    }
    return render(request , template_name , context)

    # mystr = ''
    # counter =0
    # for item in movies:
    #     counter +=1
    #     mystr+= '{0} - {1}<br>'.format(str(counter), item)

    # response_text = '\n'.join(
    #     '{} : {} <br>'.format(i, item) for i , item in enumerate (movies, start=1)
    # )


def cinema_list(request):
    cinemas = Cinema.objects.all()
    cinema_count = Cinema.objects.count()

    template_name = 'ticketing/cinema_list.html'
    context = {
        'cinema_list': cinemas,
        'cinema_count' : cinema_count,
    }
    return render(request, template_name, context)


@login_required # اگر کاربر لاگین بود، صفحه را به وی نمایش می دهد. اگر لاگین نبود، وی را هدایت میکند به صفحه لاگین و پارامتر next را برابر با صفحه حال حاضر می گذارد تا کاربر بعد از لاگین، به همان صفحه فعلی هدایت شود.
def showtime_list(request):
    search_form = ShowtimeSearchForm(request.GET)      # Form instance from ShowtimeSearchForm
    if search_form.is_valid():      ## IF FORM WAS WALID, show searched results
        if search_form.cleaned_data['movie_name'] is not None:
            showtimes = ShowTime.objects.filter(movie__name__contains = search_form.cleaned_data['movie_name']).order_by('-start_time')
        if search_form.cleaned_data['is_open']==True : # if checkbox, checked (True)
            showtimes = showtimes.filter(status=ShowTime.SALE_OPEN)
        if search_form.cleaned_data['min_length'] is not None:
            showtimes = showtimes.filter(movie__length__gte= int(search_form.cleaned_data['min_length']))
        if search_form.cleaned_data['max_length'] is not None:
            showtimes = showtimes.filter(movie__length__lte= int(search_form.cleaned_data['max_length']))
        if search_form.cleaned_data['cinema'] is not None:      # آی دی سینما را چک می کند.
            showtimes = showtimes.filter(cinema_id=search_form.cleaned_data['cinema'])

        min_price , max_price = search_form.get_price_boundries()
        if min_price is not None:
            showtimes = showtimes.filter(price__gte=min_price)
        if max_price is not None:
            showtimes = showtimes.filter( price__lt=max_price)

    else:       #SHOW ALL results
        showtimes = ShowTime.objects.all().order_by('start_time')
    template_name = 'ticketing/showtime_list.html'
    context = {'showtimes': showtimes,
               'search_form': search_form
               }
    return render(request, template_name, context)


def movie_details(request, movie_id):
    qs = get_object_or_404(Movie ,pk=movie_id)
    template_name = 'ticketing/movie_details.html'
    context = {'movie' : qs}
    return render(request, template_name, context)

def cinema_details(request, cinema_id):
    qs = get_object_or_404(Cinema ,pk=cinema_id)
    template_name = 'ticketing/cinema_details.html'
    context = {'cinema' : qs}
    return render(request, template_name, context)


def showtime_details(request, showtime_id):
    context = {}
    template_name = 'ticketing/showtime_details.html'
    showtime = ShowTime.objects.filter(pk=showtime_id).first()
    if request.method == "POST":
        try:
            seat_count = int(request.POST['seat_count'])
            # showtime = ShowTime.objects.filter(pk=showtime_id).first()
            total_price = showtime.price * seat_count   # مبلغ کل بلیط های خریداری شده
            assert showtime.status==ShowTime.SALE_OPEN ,'وضعیت این سانس، در حال نمایش نمی باشد'
            assert showtime.free_seats >= seat_count ,'تعداد صندلی خالی به اندازه مورد درخواست شما وجود ندارد'
            assert request.user.profile.balance >= total_price ,'موجودی حساب شما کافی نیست'
            ticket= Ticket.objects.create(showtime = showtime,
                                  customer = request.user.profile,
                                  seat_count = seat_count
                                  )
            request.user.profile.spend(total_price)
            showtime.free_seats -=seat_count    # صندلی های خریداری شده را از تعداد صندلی خالی کم میکند
            showtime.save()

        #  passing error text(s) to the template
        except Exception as e:
            context['error'] = str(e)
        else:
            # return redirect('ticketing:ticket_details' , kwargs={'ticket_id': ticket.id})
            return redirect('ticketing:ticket_details', ticket_id=ticket.id)

    context['showtime'] = showtime
    return render(request, template_name, context)


# Tickets Models

@login_required
def ticket_list(request):
    tickets = Ticket.objects.filter(customer=request.user.profile).order_by('-order_time')
    context = {
        'tickets': tickets
    }
    template_name = 'ticketing/ticket_list.html'
    return render(request, template_name, context)


@login_required
def ticket_details(request, ticket_id):
    ticket = Ticket.objects.filter(pk=ticket_id).first()
    context = {
        'ticket': ticket
    }
    template_name = 'ticketing/ticket_details.html'
    return render(request, template_name, context)