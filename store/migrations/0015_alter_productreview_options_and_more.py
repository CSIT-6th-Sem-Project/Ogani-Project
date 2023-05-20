# Generated by Django 4.2 on 2023-05-19 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0014_productreview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ['-created_at']},
        ),
        migrations.RenameField(
            model_name='billing',
            old_name='mobile_no',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='billing',
            name='country',
        ),
        migrations.RemoveField(
            model_name='billing',
            name='state',
        ),
        migrations.RemoveField(
            model_name='billing',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='billing',
            name='order_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='billing',
            name='payment_type',
            field=models.CharField(choices=[('cash_on_delivery', 'Cash on Delivery'), ('khalti_wallet', 'Khalti Wallet')], default='khalti_wallet', max_length=100),
        ),
        migrations.AddField(
            model_name='billing',
            name='shipping_address',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='billing',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='billing_user', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
