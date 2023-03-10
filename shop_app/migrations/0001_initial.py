# Generated by Django 3.2.9 on 2021-11-17 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('model', models.CharField(max_length=128)),
                ('price', models.FloatField()),
                ('color', models.CharField(max_length=30)),
                ('warranty', models.IntegerField()),
                ('count', models.IntegerField()),
                ('category', models.CharField(choices=[('notebook', 'Notebook'), ('dishwasher', 'Dishwasher'), ('vacuumCleaner', 'Vacuum Cleaner'), ('tv', 'Tv')], max_length=150)),
                ('brand_name', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='shop_app.brand')),
            ],
        ),
        migrations.CreateModel(
            name='Dishwasher',
            fields=[
                ('products_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop_app.products')),
                ('energy_saving_class', models.CharField(default='A+', max_length=2)),
                ('power', models.IntegerField(default=0)),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
            ],
            bases=('shop_app.products',),
        ),
        migrations.CreateModel(
            name='Notebook',
            fields=[
                ('products_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop_app.products')),
                ('display', models.DecimalField(decimal_places=3, max_digits=5)),
                ('memory', models.IntegerField()),
                ('video_memory', models.IntegerField()),
                ('cpu', models.CharField(max_length=128)),
            ],
            bases=('shop_app.products',),
        ),
        migrations.CreateModel(
            name='TV',
            fields=[
                ('products_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop_app.products')),
                ('display', models.DecimalField(decimal_places=3, max_digits=5)),
                ('memory', models.IntegerField()),
                ('display_type', models.CharField(max_length=8)),
                ('smart_tv', models.BooleanField(default=False)),
            ],
            bases=('shop_app.products',),
        ),
        migrations.CreateModel(
            name='VacuumCleaner',
            fields=[
                ('products_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='shop_app.products')),
                ('noise_level', models.FloatField()),
                ('power', models.IntegerField()),
                ('width', models.FloatField()),
                ('height', models.FloatField()),
                ('eco_engine', models.BooleanField(default=False)),
            ],
            bases=('shop_app.products',),
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('purchase_date', models.DateField(auto_now=True, null=True)),
                ('product', models.ManyToManyField(to='shop_app.Products')),
                ('user_bayer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='auth_user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='Backpack',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(default=0)),
                ('bayer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_user.userprofile')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.products')),
            ],
        ),
    ]
