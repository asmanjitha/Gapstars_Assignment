# Generated by Django 4.1.1 on 2022-09-15 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocompany', '0004_alter_cart_parts_alter_order_parts'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
