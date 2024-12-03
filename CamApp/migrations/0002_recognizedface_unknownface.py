# Generated by Django 5.1 on 2024-11-18 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CamApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecognizedFace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('confidence', models.FloatField()),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('processed_image', models.ImageField(upload_to='recognized_faces/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UnknownFace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('x', models.IntegerField()),
                ('y', models.IntegerField()),
                ('width', models.IntegerField()),
                ('height', models.IntegerField()),
                ('processed_image', models.ImageField(upload_to='unknown_faces/')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]