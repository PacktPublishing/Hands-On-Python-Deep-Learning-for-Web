# Generated by Django 2.2.5 on 2019-12-05 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='delivery_date',
        ),
        migrations.AlterField(
            model_name='order',
            name='name',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(default='Confirmed', max_length=20),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_id',
            field=models.IntegerField(),
        ),
    ]