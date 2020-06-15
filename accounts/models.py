from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Profile(models.Model):
    """
    Represents a user's profile
    """

    class Meta:
        verbose_name = 'پروفایل'
        verbose_name_plural = 'پروفایل'

    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='حساب کاربری')
    # important fields that are stored in User model:
    #   first_name, last_name, email, date_joined

    mobile = models.CharField('تلفن همراه', max_length=11)

    MALE = 1
    FEMALE = 2
    GENDER_CHOICES = ((MALE, 'مرد'), (FEMALE, 'زن'))
    gender = models.IntegerField('جنسیت', choices=GENDER_CHOICES, null=True, blank=True)

    birth_date = models.DateField('تاریخ تولد', null=True, blank=True)
    address = models.TextField('آدرس', null=True, blank=True)
    profile_image = models.ImageField('تصویر', upload_to='users/profile_images/', null=True, blank=True)

    # fields related to tickets
    balance = models.IntegerField('اعتبار', default=0)

    def __str__(self):
        return self.user.get_full_name()

    def get_balance_display(self):
        return '{} تومان'.format(self.balance)

    # behaviors
    def deposit(self, amount):
        self.balance += amount
        self.save()

    def spend(self, amount):
        if self.balance < amount:
            return False
        self.balance -= amount
        self.save()
        return True


class Payment(models.Model):
    class Meta:
        verbose_name = 'پرداخت'
        verbose_name_plural = 'پرداخت'

    profile = models.ForeignKey(Profile , on_delete=models.PROTECT, verbose_name= 'پروفایل')
    amount = models.PositiveIntegerField(verbose_name='مبلغ')
    transaction_time = models.DateTimeField(verbose_name='زمان تراکنش', auto_now_add=True)
    transaction_code = models.CharField(verbose_name='رسید تراکنش', max_length=30)

    def __str__(self):
        return '{} تومان افزایش اعتبار برای {}'.format(self.amount, self.profile)