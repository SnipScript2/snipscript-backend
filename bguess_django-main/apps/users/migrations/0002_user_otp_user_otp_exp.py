# Generated by Django 5.1.6 on 2025-02-28 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='otp_exp',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
