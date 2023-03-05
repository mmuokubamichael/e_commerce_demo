# Generated by Django 4.0.4 on 2023-02-05 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_my_order_disput_state_my_order_order_state_dispute'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratings',
            name='product',
        ),
        migrations.AddField(
            model_name='ratings',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='products.my_order'),
            preserve_default=False,
        ),
    ]