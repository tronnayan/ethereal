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
    slug = models.CharField(max_length=200, unique=True, null=True)
    description = models.CharField(max_length=1000, null=True)
    price = models.IntegerField(default=50)
    shipping_charges = models.IntegerField(default=50)
    sample_link = models.URLField(default=None, null=True)
    video_url = models.URLField(default=None, null=True)
    weight = models.FloatField(default=0.5)
    dimensions = models.CharField(default=None, null=True, max_length=1000)
    listing_tags = models.ManyToManyField(ListingTag, related_name='tags')
    is_featured = models.BooleanField(default=False)
    category = models.ForeignKey('ListingCategory', related_name='items', on_delete=models.CASCADE, null=True)

    def get_primary_image(self):
        primary_image = self.images.filter(is_primary=True).first()
        if not primary_image:
            return self.images.first().image_url if self.images.first() else ''
        return primary_image.image_url

    def get_starting_images(self):
        return self.images.all().order_by('-pk')[:2]

    def get_all_images(self):
        return self.images.all().order_by('-pk')[2:]

    def __str__(self):
        return self.name


class ListingCategory(BaseModel):
    name = models.CharField(max_length=100)
    logo = models.CharField(max_length=500)

    def __str__(self):
        return self.name


# categories = [
#     "Room Decor",
#     "Special Occasion Gifts",
#     "Themed Gift Boxes & Albums",
#     "Home Decor"
# ]
#
# listing = Listing.objects.create(name='Wooden Photo Box', description="Cherish your precious memories in our unique pull-out photo album box, beautifully crafted from premium wood. This ingenious design features an accordion-style photo strip that gracefully unfolds to display your favorite moments in sequence, while staying safely stored in an elegant wooden case. The lid can be personalized with your chosen text, making each box uniquely yours. Perfect for wedding photos, family memories, anniversaries, or any special moments worth preserving.", price=1799)
# images = [
#     'https://i.etsystatic.com/51098660/r/il/ba0b41/6132615869/il_1588xN.6132615869_jhoi.jpg',
#     'https://i.etsystatic.com/51098660/r/il/ed993c/6132615159/il_1588xN.6132615159_kkof.jpg',
#     'https://i.etsystatic.com/51098660/r/il/ed793c/6132614961/il_1588xN.6132614961_h0z5.jpg',
#     'https://i.etsystatic.com/51098660/r/il/02c610/6468468074/il_1588xN.6468468074_ioad.jpg'
# ]
# for img in images:
#     ListingImage.objects.create(image_url=img, listing=listing)
# images = ['https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im1.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im2.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im3.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im4.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im5.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im6.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im7.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im8.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/im9.webp', 'https://botally.s3.ap-southeast-1.amazonaws.com/ayuree_arts/faceless_illustrations/01.png']
# listing = Listing.objects.create(name='Faceless Illustrations', description="Discover the beauty of minimalist storytelling through our evocative Faceless Illustrations collection. Each piece captures the essence of human emotion and movement without facial features, creating a universal connection that transcends individual identity", price=119)


# images = [
#     'https://i.etsystatic.com/20183842/r/il/ab5dca/2735048961/il_1588xN.2735048961_k9s4.jpg',
#     'https://i.etsystatic.com/20183842/r/il/b6e783/2687365808/il_1588xN.2687365808_3c43.jpg',
#     'https://i.etsystatic.com/20183842/r/il/47cca7/2735049573/il_1588xN.2735049573_7qh6.jpg',
#     'https://i.etsystatic.com/20183842/r/il/450c42/2710231772/il_1588xN.2710231772_fejb.jpg',
# ]