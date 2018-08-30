# Generated by Django 2.1 on 2018-08-29 09:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.SET_DEFAULT, to='api.Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(blank=True, to='api.Product'),
        ),
    ]