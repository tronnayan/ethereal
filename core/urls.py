from django.urls import path

from core.views import CoreViewSet

urlpatterns = [
    path('', CoreViewSet.as_view({"get": "get_landing_page"}), name='get_landing_page'),
    path('listing/<str:slug>/', CoreViewSet.as_view({"get": "get_listing_detail_page"}), name='get_listing_detail_page'),
    path('category/<int:category_id>/', CoreViewSet.as_view({"get": "get_category_detail_page"}), name='get_category_detail_page'),
    path('checkout/', CoreViewSet.as_view({"get": "get_checkout_page"}), name='get_checkout_page'),
]

