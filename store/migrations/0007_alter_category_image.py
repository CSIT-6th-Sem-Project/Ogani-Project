# Generated by Django 4.2 on 2023-05-14 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_category_labels_product_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='categories'),
        ),
    ]
