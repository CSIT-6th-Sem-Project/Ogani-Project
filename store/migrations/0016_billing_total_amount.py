# Generated by Django 4.2 on 2023-05-19 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_productreview_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='billing',
            name='total_amount',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
