# Generated by Django 2.2.6 on 2019-10-16 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.IntegerField(db_column='id', primary_key=True, serialize=False)),
                ('bookName', models.CharField(max_length=20)),
                ('author', models.CharField(max_length=20)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5, null=True)),
                ('publish', models.CharField(max_length=20, null=True)),
            ],
            options={
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.IntegerField(db_column='userId', primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=64)),
                ('email', models.CharField(max_length=20, null=True)),
                ('avatar', models.CharField(max_length=100, null=True)),
                ('signature', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=20, null=True)),
                ('group', models.CharField(max_length=50, null=True)),
                ('notifyCount', models.IntegerField(null=True)),
                ('unreadCount', models.IntegerField(null=True)),
                ('country', models.CharField(max_length=120, null=True)),
                ('address', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
