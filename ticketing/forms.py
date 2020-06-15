from django import forms

from .models import Cinema


class ShowtimeSearchForm(forms.Form):
    movie_name = forms.CharField(label='عنوان فیلم', max_length=100, required=False)
    is_open = forms.BooleanField(label='آیا سانس در حال نمایش است؟', required=False)
    min_length = forms.IntegerField(label= 'حداقل زمان فیلم', min_value=0, max_value=200, required=False)
    max_length = forms.IntegerField(label='حداکثر زمان فیلم', min_value=0, max_value=200, required=False)

    PRICE_ANY = '0'
    PRICE_UNDER_10 = '1'
    PRICE_10_TO_15 = '2'
    PRICE_15_TO_20 = '3'
    PRICE_ABOVE_20 = '4'
    PRICE_LEVEL_CHOICES = (
        (PRICE_ANY, "هر قیمتی"),
        (PRICE_UNDER_10, "تا 10 هزار تومان"),
        (PRICE_10_TO_15, "10 تا 15 هزار تومان"),
        (PRICE_15_TO_20, "15 تا 20 هزار تومان"),
        (PRICE_ABOVE_20, "بیش از 20 هزار تومان"),
    )
    price_level = forms.ChoiceField(label="محدوده قیمت", choices=PRICE_LEVEL_CHOICES, required=False)       # ChoiceField Gets Tupple as input
    cinema = forms.ModelChoiceField(label='سینما', queryset=Cinema.objects.all(), required=False)       #ModelChoiceField Gets queryset as input


    def get_price_boundries(self):
        price_level = self.cleaned_data['price_level']
        if price_level == ShowtimeSearchForm.PRICE_UNDER_10:
            return None, 10000
        elif price_level == ShowtimeSearchForm.PRICE_10_TO_15:
            return 10000, 15000
        elif price_level == ShowtimeSearchForm.PRICE_15_TO_20:
            return 15000, 20000
        elif price_level == ShowtimeSearchForm.PRICE_ABOVE_20:
            return 20000, None
        else:
            return None, None