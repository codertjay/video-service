# Generated by Django 3.0.3 on 2020-05-08 21:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('memberships', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermembership',
            name='memberships',
            field=models.ForeignKey(default='Free', null=True, on_delete=django.db.models.deletion.SET_NULL, to='memberships.Membership'),
        ),
    ]
