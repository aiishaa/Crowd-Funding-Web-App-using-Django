# Generated by Django 5.0.3 on 2024-03-25 11:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Project', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='donation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Project.category'),
        ),
        migrations.AddField(
            model_name='project',
            name='p_owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='picture',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project'),
        ),
        migrations.AddField(
            model_name='donation',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project'),
        ),
        migrations.AddField(
            model_name='comment',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project'),
        ),
        migrations.AddField(
            model_name='rate',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project'),
        ),
        migrations.AddField(
            model_name='rate',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='report',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Project.project'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='project',
            name='tags',
            field=models.ManyToManyField(to='Project.tag'),
        ),
    ]
