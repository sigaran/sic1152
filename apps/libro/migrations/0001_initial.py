# Generated by Django 2.2.3 on 2019-11-25 22:17

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('catalogo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(blank=True, default=django.utils.timezone.now)),
                ('descripcion', models.CharField(max_length=50)),
                ('monto_contado', models.FloatField(default=0.0)),
                ('monto_credito', models.FloatField(default=0.0)),
                ('tipo_transaccion', models.IntegerField(default=0)),
                ('descripcion_cargo', models.CharField(max_length=50)),
                ('descripcion_abono', models.CharField(max_length=50)),
                ('monto', models.FloatField(default=0.0)),
                ('abono', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='abono', to='catalogo.SubCuenta')),
                ('abono_alt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='abono_alt', to='catalogo.SubCuenta')),
                ('cargo', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cargo', to='catalogo.SubCuenta')),
                ('cargo_alt', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cargo_alt', to='catalogo.SubCuenta')),
            ],
        ),
    ]
