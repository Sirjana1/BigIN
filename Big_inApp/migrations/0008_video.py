# Generated by Django 3.2.19 on 2023-12-25 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Big_inApp', '0007_delete_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('video_id', models.CharField(max_length=20)),
            ],
        ),
    ]
