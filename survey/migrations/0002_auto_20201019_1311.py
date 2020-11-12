# Generated by Django 3.0.8 on 2020-10-19 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='questionimage',
            name='survey',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='survey', to='survey.Survey'),
        ),
        migrations.AlterField(
            model_name='questionimage',
            name='question',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='question', to='survey.Question'),
        ),
    ]
