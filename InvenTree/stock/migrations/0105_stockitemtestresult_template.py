# Generated by Django 4.2.9 on 2024-02-07 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('part', '0121_auto_20240207_0344'),
        ('stock', '0104_alter_stockitem_purchase_price_currency'),
    ]

    operations = [
        migrations.AddField(
            model_name='stockitemtestresult',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='test_results', to='part.parttesttemplate'),
        ),
    ]