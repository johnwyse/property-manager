# Generated by Django 4.0 on 2022-02-10 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('property', '0005_unit_lease_alter_unit_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issue',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
        migrations.AlterField(
            model_name='message',
            name='image',
            field=models.ImageField(blank=True, upload_to='images/'),
        ),
    ]
