# Generated by Django 2.2.4 on 2020-10-20 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('python_belt_app', '0002_auto_20201020_1718'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quotes', to='python_belt_app.User'),
        ),
    ]