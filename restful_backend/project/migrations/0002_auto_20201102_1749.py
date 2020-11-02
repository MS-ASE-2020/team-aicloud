# Generated by Django 3.1.2 on 2020-11-02 09:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dataset',
            name='related_project',
        ),
        migrations.AddField(
            model_name='dataset',
            name='related_user',
            field=models.ForeignKey(default='', help_text='The user this dataset belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='datasets', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='dataset',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, help_text='generate uuid by uuid1 algorithm', verbose_name='dataset uuid'),
        ),
        migrations.AddField(
            model_name='project',
            name='related_data',
            field=models.ForeignKey(default='', help_text='The data this project hold', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='project.dataset'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='name',
            field=models.CharField(help_text='the max length is 32, composed with "A-Za-z0-9_"', max_length=32, verbose_name='dataset name'),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='time_created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='the time at which the user uploaded the data; auto-generated', verbose_name='creation time'),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(help_text='the max length is 32, composed with "A-Za-z0-9_"', max_length=32, verbose_name='project name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='related_user',
            field=models.ForeignKey(default='', help_text='The user this project belongs to', on_delete=django.db.models.deletion.CASCADE, related_name='projects', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='project',
            name='time_created',
            field=models.DateTimeField(default=django.utils.timezone.now, help_text='the time at which the user created the project; auto-generated', verbose_name='creation time'),
        ),
    ]
