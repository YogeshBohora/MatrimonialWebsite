# Generated by Django 2.1.5 on 2021-02-21 11:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wedding', '0005_sucess_story'),
    ]

    operations = [
        migrations.CreateModel(
            name='Religion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('religion', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='sucess_story',
            name='signup',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='caste',
        ),
        migrations.DeleteModel(
            name='Caste',
        ),
        migrations.DeleteModel(
            name='Sucess_Story',
        ),
        migrations.AddField(
            model_name='profile',
            name='religion',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wedding.Religion'),
        ),
    ]
