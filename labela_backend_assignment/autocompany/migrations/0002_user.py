# Generated by Django 4.1.1 on 2022-09-14 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('autocompany', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('password', models.CharField(max_length=250)),
            ],
        ),
    ]