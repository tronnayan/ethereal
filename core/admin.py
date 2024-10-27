from django.contrib import admin

from .models import ListingTag, Listing, ListingImage, ListingCategory


class ModelAdminMod(admin.ModelAdmin):
    """
    This helps display the is_deleted objects in admin
    """
    def get_queryset(self, request):
        qs = self.model.admin_manager.get_queryset()
        ordering = self.get_ordering(request)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


@admin.register(ListingTag)
class ListingTagAdmin(ModelAdminMod):
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
class ListingAdmin(ModelAdminMod):
    list_display = (
        'id',
        'is_active',
        'name',
        'description',
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


@admin.register(ListingImage)
class ListingImageAdmin(ModelAdminMod):
    list_display = (
        'id',
        'is_active',
        'image_url',
        'listing',
        'is_primary',
    )
    list_filter = (
        'created_at',
        'modified_at',
        'is_deleted',
        'is_active',
        'listing',
        'is_primary',
    )


@admin.register(ListingCategory)
class ListingCategoryAdmin(ModelAdminMod):
    list_display = (
        'id',
        'is_active',
        'logo',
        'name'
    )
    list_filter = (
        'is_deleted',
        'is_active'
    )
