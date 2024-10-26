from django.shortcuts import render
from rest_framework.viewsets import ViewSet


class CoreViewSet(ViewSet):
    permission_classes = []

    def check_permissions(self, request):
        pass

    def get_landing_page(self, request):
        return render(request, 'index.html', {})