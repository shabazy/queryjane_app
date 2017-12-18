# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-01 01:01
from __future__ import unicode_literals

from django.db import migrations


initial_categories = [
    {
        'name_es': 'Construcción',
        'name_en': 'Construction',
    },
    {
        'name_es': 'Negocios',
        'name_en': 'Business',
    },
    {
        'name_es': 'Dispensario',
        'name_en': 'Dispensary',
    },
    {
        'name_es': 'Cañamo',
        'name_en': 'Hemp',
    },
    {
        'name_es': 'Servicio al cliente',
        'name_en': 'Customer service',
    },
    {
        'name_es': 'Cultivo',
        'name_en': 'Cultivation',
    },
    {
        'name_es': 'Distribución',
        'name_en': 'Distribution',
    },
    {
        'name_es': 'Comestibles',
        'name_en': 'Edible',
    },
    {
        'name_es': 'Extracción',
        'name_en': 'Extraction',
    },
    {
        'name_es': 'Investigación',
        'name_en': 'Research',
    },
    {
        'name_es': 'Hidroponía',
        'name_en': 'hydroponics',
    },
    {
        'name_es': 'Medicinal',
        'name_en': 'Medical',
    },
    {
        'name_es': 'Administración',
        'name_en': 'Management',
    },
    {
        'name_es': 'Informática',
        'name_en': 'IT',
    },
    {
        'name_es': 'Ventas y Marketing',
        'name_en': 'Sales & Marketing',
    },
    {
        'name_es': 'Seguridad',
        'name_en': 'Security',
    },
    {
        'name_es': 'Social media',
        'name_en': 'Social media',
    },
    {
        'name_es': 'Laboratorio',
        'name_en': 'Laboratory',
    },
    {
        'name_es': 'Transporte',
        'name_en': 'Transportation',
    },
    {
        'name_es': 'Publicidad',
        'name_en': 'Advertising',
    },
    {
        'name_es': 'Medicina veterinaria',
        'name_en': 'Veterinary Medicine',
    },
]


def create_initial_industry_categories(apps, schema_editor):
    IndustryCategoryModel = apps.get_model('account', 'IndustryCategory')

    for category in initial_categories:
        i = IndustryCategoryModel(**category)
        i.save()


class Migration(migrations.Migration):

    dependencies = [
        ('entrepreneur', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_industry_categories),
    ]
