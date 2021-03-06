# Generated by Django 2.1.3 on 2018-11-15 12:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('app01', '0004_auto_20181115_1130'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='菜单')),
                ('icon', models.CharField(blank=True, max_length=32, null=True, verbose_name='图标')),
            ],
        ),
        migrations.CreateModel(
            name='Permission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='标题')),
                ('url', models.CharField(max_length=32, verbose_name='权限')),
                ('Positions', models.ManyToManyField(blank=True, to='app01.Position', verbose_name='职位所拥有的权限')),
                ('menu', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='rbac.Menu')),
            ],
        ),
    ]
