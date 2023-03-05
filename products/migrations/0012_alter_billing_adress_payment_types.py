# Generated by Django 4.0.4 on 2023-01-25 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_rename_payment_type_billing_adress_payment_types'),
    ]

    operations = [
        migrations.AlterField(
            model_name='billing_adress',
            name='payment_types',
            field=models.CharField(choices=[('stripe', 'stripe'), ('paypal', 'paypal')], default='stripe', max_length=6),
        ),
    ]