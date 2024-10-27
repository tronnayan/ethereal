from django.shortcuts import render
from rest_framework.viewsets import ViewSet

from core.models import Listing


class CoreViewSet(ViewSet):
    permission_classes = []

    def check_permissions(self, request):
        pass

    def get_landing_page(self, request):
        listings = Listing.objects.all().order_by('-pk')
        context = {
            "listings": listings
        }
        return render(request, 'landing.html', context)