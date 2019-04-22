# Generated by Django 2.2 on 2019-04-12 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Board_app', '0003_myaccount'),
    ]

    operations = [
        migrations.AddField(
            model_name='myaccount',
            name='uploaded_image_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='myaccount',
            name='userimage',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]