# Generated by Django 4.2.4 on 2023-08-10 04:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ELearning', '0006_user_course'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(blank=True, max_length=200, null=True)),
                ('payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('status', models.BooleanField(default=False)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ELearning.course_details')),
                ('course_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ELearning.user_course')),
                ('user_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ELearning.signup')),
            ],
        ),
    ]
