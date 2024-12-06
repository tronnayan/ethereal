from django.contrib.sites.shortcuts import get_current_site
from django.core.management.base import BaseCommand
from django.urls import reverse
from django.utils import timezone
from xml.dom.minidom import Document
from core.models import Listing


class Command(BaseCommand):
    help = 'Generate sitemap.xml for all listings'

    def handle(self, *args, **kwargs):
        # Create the XML document
        doc = Document()

        # Create the urlset element
        urlset = doc.createElement('urlset')
        urlset.setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        doc.appendChild(urlset)

        # Base URL of your site
        base_url = 'https://littleartist.in'

        # Add homepage
        url_element = doc.createElement('url')
        loc = doc.createElement('loc')
        loc_text = doc.createTextNode(base_url)
        loc.appendChild(loc_text)
        url_element.appendChild(loc)

        # Add lastmod for homepage
        lastmod = doc.createElement('lastmod')
        lastmod_text = doc.createTextNode(timezone.now().strftime('%Y-%m-%d'))
        lastmod.appendChild(lastmod_text)
        url_element.appendChild(lastmod)

        urlset.appendChild(url_element)

        # Get all active listings
        listings = Listing.objects.filter(is_deleted=False, is_active=True)

        # Add each listing URL to sitemap
        for listing in listings:
            url_element = doc.createElement('url')

            # Location
            loc = doc.createElement('loc')
            listing_url = f"{base_url}/listing/{listing.slug}/"
            loc_text = doc.createTextNode(listing_url)
            loc.appendChild(loc_text)
            url_element.appendChild(loc)

            # Last modified
            lastmod = doc.createElement('lastmod')
            lastmod_text = doc.createTextNode(listing.modified_at.strftime('%Y-%m-%d'))
            lastmod.appendChild(lastmod_text)
            url_element.appendChild(lastmod)

            # Change frequency
            changefreq = doc.createElement('changefreq')
            changefreq_text = doc.createTextNode('weekly')
            changefreq.appendChild(changefreq_text)
            url_element.appendChild(changefreq)

            # Priority
            priority = doc.createElement('priority')
            priority_value = '0.8'  # High priority for product pages
            if listing.is_featured:
                priority_value = '1.0'  # Highest priority for featured products
            priority_text = doc.createTextNode(priority_value)
            priority.appendChild(priority_text)
            url_element.appendChild(priority)

            urlset.appendChild(url_element)

        # Write the XML file
        with open('sitemap.xml', 'w', encoding='utf-8') as f:
            f.write(doc.toxml())

        self.stdout.write(self.style.SUCCESS('Successfully generated sitemap.xml'))