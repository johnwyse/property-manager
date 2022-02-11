# Generated by Django 4.0 on 2022-02-11 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0006_alter_issue_image_alter_message_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='image',
            field=models.ImageField(blank=True, upload_to='issue_images/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='message_images/'),
        ),
        migrations.AlterField(
            model_name='unit',
            name='image',
            field=models.ImageField(blank=True, upload_to='unit_images/'),
        ),
    ]
