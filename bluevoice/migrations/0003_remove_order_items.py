# Generated by Django 4.2.6 on 2023-10-09 14:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bluevoice', '0002_cart_order_created_order_cart_alter_cartitem_cart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='items',
        ),
    ]