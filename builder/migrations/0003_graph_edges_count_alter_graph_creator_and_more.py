# Generated by Django 4.2.5 on 2023-11-02 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('extended_user', '0001_initial'),
        ('builder', '0002_graph_directed'),
    ]

    operations = [
        migrations.AddField(
            model_name='graph',
            name='edges_count',
            field=models.IntegerField(default=0, verbose_name='Количество вершин'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='graphs_by_creator', to='extended_user.profile', verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='graph',
            name='name',
            field=models.CharField(max_length=1024, null=True, verbose_name='Название'),
        ),
    ]