# Generated by Django 3.1.5 on 2021-01-28 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users_transactions', '0002_auto_20210128_1840'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='reference',
            field=models.CharField(max_length=20, primary_key=True, serialize=False),
        ),
    ]