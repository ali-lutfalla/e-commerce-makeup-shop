# Generated by Django 4.2.16 on 2024-09-12 01:15

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_wishlistitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wishlistitem',
            name='wishlisit_item_id',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='abcdefghijk123456789', length=10, max_length=27, prefix='wishlist-item', unique=True),
        ),
    ]
