from django.urls import path

from core.views import CoreViewSet

urlpatterns = [
    path('', CoreViewSet.as_view({"get": "get_landing_page"}), name='get_landing_page'),
    path('listing/<int:listing_id>/', CoreViewSet.as_view({"get": "get_listing_detail_page"}), name='get_listing_detail_page'),
]

