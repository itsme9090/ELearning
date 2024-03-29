# Generated by Django 4.2.4 on 2023-08-08 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ELearning', '0002_course_details'),
    ]

    operations = [
        migrations.CreateModel(
            name='Videos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('video_title', models.CharField(blank=True, max_length=100, null=True)),
                ('video_id', models.CharField(blank=True, max_length=100, null=True)),
                ('is_preview', models.BooleanField(default=False)),
            ],
        ),
    ]
