# Generated by Django 5.0.6 on 2024-08-12 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wuming', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='old_cart',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]