from django.urls import path

from core.views import CoreViewSet

urlpatterns = [
    path('', CoreViewSet.as_view({"get": "get_landing_page"}), name='get_landing_page'),
]

