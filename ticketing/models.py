from django.db import models
from accounts.models import Profile

# Create your models here.
from django.db.models import F


class Movie(models.Model):

    class Meta:
        verbose_name = 'فیلم'
        verbose_name_plural = 'فیلم'

    name = models.CharField(verbose_name= 'عنوان فیلم', max_length=100)
    director = models.CharField(verbose_name= 'کارگردان',max_length=50)
    year = models.IntegerField(verbose_name= 'سال ساخت فیلم')
    length = models.IntegerField(verbose_name= 'مدت زمان (دقیقه)')
    description = models.TextField(verbose_name= 'توضیحات')
    poster = models.ImageField(verbose_name='پوستر',upload_to='movie_images/')

    def __str__(self):
        return self.name

class Cinema(models.Model):
    cinema_code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    city = models.CharField(max_length=30, default='Tehran')
    capacity = models.IntegerField()
    phone = models.CharField(max_length=20, null=True)
    address = models.TextField()
    image = models.ImageField(verbose_name='تصویر',upload_to='cinema_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class ShowTime(models.Model):
    # Respresents a movie show in a cinema at a spec  ific time
    movie = models.ForeignKey(Movie, on_delete=models.PROTECT)
    cinema = models.ForeignKey(Cinema, on_delete=models.PROTECT)

    start_time = models.DateTimeField()
    price = models.IntegerField()
    salable_seats = models.IntegerField()       # تعداد صندلی های قابل فروش
    free_seats = models.IntegerField()      # تعداد صندلی های خالی

    SALE_NOT_STARTED = 1
    SALE_OPEN = 2
    TICKETS_SOLD = 3
    SALE_CLOSED = 4
    MOVIE_PLAYED = 5
    SHOW_CANCELED = 6
    status_choices = (
        (SALE_NOT_STARTED, 'فروش آغاز نشده'),
        (SALE_OPEN, 'در حال فروش بلیت'),
        (TICKETS_SOLD, 'بلیت‌ها تمام شد'),
        (SALE_CLOSED, 'فروش بلیت بسته شد'),
        (MOVIE_PLAYED, 'فیلم پخش شد'),
        (SHOW_CANCELED, 'سانس لغو شد'),
    )
    status = models.IntegerField('وضعیت', choices=status_choices, default=SALE_NOT_STARTED)

    def __str__(self):
        return '{} - {} - {}'.format(self.movie, self.cinema, self.start_time)   # اسم فیلم- اسم سینما - زمان شروع سانس

    def get_price_display(self):
        return '{} تومان'.format(self.price)


class Ticket(models.Model):
    class Meta:
        verbose_name = 'بلیت'
        verbose_name_plural = 'بلیت'

    showtime = models.ForeignKey(ShowTime, on_delete=models.PROTECT, verbose_name='سانس')
    customer = models.ForeignKey(Profile, on_delete=models.PROTECT, verbose_name='خریدار')
    seat_count = models.IntegerField('تعداد صندلی')
    order_time = models.DateTimeField('زمان خرید', auto_now_add=True)

    def __str__(self):
        return '{} بلیت به نام {} برای فیلم {}'.format(self.seat_count, self.customer, self.showtime.movie)