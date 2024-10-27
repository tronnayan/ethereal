from django.contrib import admin

# Register your models here.
# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import ListingTag, Listing


@admin.register(ListingTag)
class ListingTagAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'uuid',
        'modified_at',
        'is_deleted',
        'is_active',
        'name',
    )
    list_filter = ('created_at', 'modified_at', 'is_deleted', 'is_active')
    search_fields = ('name',)


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'is_active',
        'name',
        'description',
        'images',
        'price',
        'shipping_charges',
        'is_featured',
    )
    list_filter = (
        'created_at',
        'modified_at',
        'is_deleted',
        'is_active',
        'is_featured',
    )
    search_fields = ('name',)
    readonly_fields = ('video_url', 'sample_link', 'weight', 'dimensions', 'listing_tags')
