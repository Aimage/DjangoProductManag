# Generated by Django 2.1 on 2018-08-28 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=250)),
                ('price', models.FloatField()),
                ('quantity', models.IntegerField(default=0)),
            ],
        ),
        migrations.AddField(
            model_name='category',
            name='products',
            field=models.ManyToManyField(to='api.Product'),
        ),
    ]