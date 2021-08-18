from django.contrib.sitemaps import Sitemap
from django.urls import reverse

class Static_Sitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return ['index','about','contact']

    def location(self, item):
        return reverse(item)