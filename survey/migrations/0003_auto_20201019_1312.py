# Generated by Django 3.0.8 on 2020-10-19 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0002_auto_20201019_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questionimage',
            name='survey',
        ),
        migrations.AddField(
            model_name='questionimage',
            name='response',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='response', to='survey.Response'),
        ),
    ]
