# Generated by Django 3.0 on 2019-12-15 09:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('past_address', models.CharField(max_length=256)),
                ('present_address', models.CharField(max_length=256)),
                ('phone_number', models.CharField(max_length=256)),
            ],
        ),
    ]