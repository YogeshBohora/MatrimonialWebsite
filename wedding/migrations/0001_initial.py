# Generated by Django 2.2.6 on 2020-04-19 14:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Caste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caste', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_name', models.CharField(max_length=100, null=True)),
                ('m_name', models.CharField(max_length=100, null=True)),
                ('f_contact', models.CharField(max_length=10, null=True)),
                ('qualification', models.CharField(max_length=50, null=True)),
                ('salary', models.IntegerField(null=True)),
                ('age', models.IntegerField(null=True)),
                ('family_type', models.CharField(max_length=50, null=True)),
                ('hobby', models.CharField(max_length=100, null=True)),
                ('occupation', models.CharField(max_length=100, null=True)),
                ('work_address', models.CharField(max_length=100, null=True)),
                ('caste', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wedding.Caste')),
            ],
        ),
        migrations.CreateModel(
            name='Signup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen', models.CharField(max_length=10, null=True)),
                ('dob', models.DateField(null=True)),
                ('city', models.CharField(max_length=30, null=True)),
                ('address', models.CharField(max_length=50, null=True)),
                ('contact', models.CharField(max_length=10, null=True)),
                ('image', models.FileField(null=True, upload_to='')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SendMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message1', models.TextField(null=True)),
                ('send_user', models.CharField(max_length=100, null=True)),
                ('profile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wedding.Profile')),
            ],
        ),
        migrations.AddField(
            model_name='profile',
            name='signup',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wedding.Signup'),
        ),
    ]