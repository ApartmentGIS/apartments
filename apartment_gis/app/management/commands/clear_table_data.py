# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand, CommandError
from app.models import Apartment, Organization


class Command(BaseCommand):
    args = ''
    help = 'Delete records in tables with apartments and organizations'

    def handle(self, *args, **options):
        try:
            Apartment.objects.all().delete()
            Organization.objects.all().delete()
        except Exception as e:
            raise CommandError('Error when clear db: %s' % e)
