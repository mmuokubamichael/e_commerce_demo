# Generated by Django 4.0.4 on 2023-02-05 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_ratings_delete_rating'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ratings',
            name='order',
        ),
        migrations.AddField(
            model_name='ratings',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='products.products'),
        ),
    ]