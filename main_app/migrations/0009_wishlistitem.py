# Generated by Django 4.2.16 on 2024-09-11 23:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0008_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='WishlistItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('wishlisit_item_id', shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijk123456789', length=10, max_length=20, prefix='wishlist-item', unique=True)),
                ('sku', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='main_app.productentry')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Wishlist Items',
            },
        ),
    ]
