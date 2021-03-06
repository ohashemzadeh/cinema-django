# Generated by Django 2.2 on 2020-02-24 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ticketing', '0003_auto_20200224_2116'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShowTime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('price', models.IntegerField()),
                ('salable_seats', models.IntegerField()),
                ('free_seats', models.IntegerField()),
                ('status', models.IntegerField(choices=[(1, 'فروش آغاز نشده'), (2, 'در حال فروش بلیط'), (3, 'بلیط ها تمام شد'), (4, 'فروش بلیط بسته شد'), (5, 'فیلم پخش شد'), (6, 'سانس لغو شد')])),
                ('cinema', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.Cinema')),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ticketing.Movie')),
            ],
        ),
    ]
