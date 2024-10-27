from django.contrib.auth.models import User
from django.db import models
import uuid


class AllManager(models.Manager):
    def get_queryset(self):
        return super(AllManager, self).get_queryset().filter(is_deleted=False)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AllManager()
    admin_manager = models.Manager()

    class Meta:
        abstract = True


class ListingTag(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class ListingImage(BaseModel):
    image_url = models.CharField(max_length=400)
    listing = models.ForeignKey('Listing', related_name='images', on_delete=models.CASCADE)
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return self.listing.name


class Listing(BaseModel):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, null=True)
    price = models.IntegerField(default=50)
    shipping_charges = models.IntegerField(default=50)
    sample_link = models.URLField(default=None, null=True)
    video_url = models.URLField(default=None, null=True)
    weight = models.FloatField(default=0.5)
    dimensions = models.CharField(default=None, null=True, max_length=1000)
    listing_tags = models.ManyToManyField(ListingTag, related_name='tags')
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.name


def create_new_listing(name: str, description: str, images: list, price: int):
    listing = Listing.objects.create(
        name=name,
        description=description,
        images={'images': images},
        price=price
    )
    return listing.name

