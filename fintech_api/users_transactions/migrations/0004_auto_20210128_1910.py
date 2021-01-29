# Generated by Django 3.1.5 on 2021-01-28 19:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users_transactions', '0003_auto_20210128_1848'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='created_at',
        ),
        migrations.AddField(
            model_name='transaction',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]