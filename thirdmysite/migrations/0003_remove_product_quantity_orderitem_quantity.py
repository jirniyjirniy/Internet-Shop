# Generated by Django 4.0.6 on 2022-09-14 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('thirdmysite', '0002_product_quantity_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]
