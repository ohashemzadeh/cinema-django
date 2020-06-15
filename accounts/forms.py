from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import Payment, Profile


class PaymentModelForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['amount','transaction_code']

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount % 1000 != 0:
            raise ValidationError('مقدار فیش پرداختی بایستی مضربی از هزار تومن باشد.')
        return amount

    def clean_transaction_code(self):
        code = str(self.cleaned_data.get('transaction_code'))
        try:
            #should be in format :   bank-<amount>-<TOKEN>#
            # e.g. bank-30000-UHB454GRH73BDYU#
            assert code.startswith('bank-')
            assert code.endswith('#')
            parts = code.split('-')
            assert len(parts) == 3
            int(parts[1])       # اگر ارور بدهد یعنی قسمت دوم عبارت، عدد نیست
        except:
            raise ValidationError('قالب (فرمت) رسید معتبر نیست')
        return code


    # تابع clean، بعد از اینکه cleanبودن تک تک فیلد ها چک شد اجرا می شود.
    def clean(self):
        super().clean() # یک سری توابع default هستند که باید اجرا شوند
        code = self.cleaned_data.get('transaction_code')
        amount = self.cleaned_data.get('amount')
        if amount is not None and code is not None:
            if int(code.split('-')[1]) != amount:
                    raise ValidationError('مبلغ و رسید تراکنش با هم خوانایی ندارند.')


class ProfileModelForm(ModelForm):

    class Meta:
        model = Profile
        fields = ['mobile','gender','birth_date','address','profile_image']

class MyUserForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):    # باید کلاس اصلی، override شود تا فقط فیلد های مورد نظرمان نمایش داده شوند.
        fields = ['username', 'first_name', 'last_name', 'email']
    password = None # این خط باید نوشته شود . چون فیلد پسورد، در کلاس UserChangeForm ، عملکرد متفاوتی دارد.