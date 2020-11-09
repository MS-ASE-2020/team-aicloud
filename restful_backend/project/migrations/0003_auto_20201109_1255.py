# Generated by Django 3.1.2 on 2020-11-09 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0002_auto_20201105_1517'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='predictor',
            name='status',
        ),
        migrations.AddField(
            model_name='predictor',
            name='related_series',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='predictor', to='project.series'),
        ),
        migrations.AddField(
            model_name='series',
            name='status',
            field=models.IntegerField(choices=[(0, 'Created'), (1, 'Uncomitted'), (2, 'Comitted'), (3, 'Done'), (4, 'Exception')], default=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='status',
            field=models.IntegerField(choices=[(0, 'Created'), (1, 'Uncomitted'), (2, 'Comitted'), (3, 'Done'), (4, 'Exception')], default=0),
        ),
    ]