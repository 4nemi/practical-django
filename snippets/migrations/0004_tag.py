# Generated by Django 5.0.6 on 2024-06-03 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('snippets', '0003_alter_snippet_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='タグ名')),
                ('snippets', models.ManyToManyField(related_name='tags', related_query_name='tag', to='snippets.snippet')),
            ],
            options={
                'db_table': 'tags',
            },
        ),
    ]