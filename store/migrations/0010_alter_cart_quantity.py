# Generated by Django 4.2 on 2023-05-14 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0009_alter_product_description_alter_product_information'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]