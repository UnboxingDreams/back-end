# Generated by Django 5.0a1 on 2023-10-12 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('petmourning', '0005_alter_user_animaldeathdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='expirationTime',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='answer',
            name='emotion',
            field=models.CharField(max_length=10),
        ),
        migrations.AlterField(
            model_name='user',
            name='animalImgUrl',
            field=models.URLField(default=1, max_length=150),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='death',
            field=models.CharField(max_length=10),
        ),
    ]
