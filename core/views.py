from django.shortcuts import render
from rest_framework.viewsets import ViewSet

from core.models import Listing, ListingCategory


class CoreViewSet(ViewSet):
    permission_classes = []

    def check_permissions(self, request):
        pass

    def get_landing_page(self, request):
        listings = Listing.objects.all().select_related('category').order_by('-pk')
        listing_categories = ListingCategory.objects.all().order_by('pk')
        context = {
            "listings": listings,
            "listing_categories": listing_categories
        }
        return render(request, 'landing.html', context)