from django.shortcuts import reverse
from django.contrib.sitemaps import Sitemap
from .models import Amazon,Shopclue,Shopclues,Snapdeal
from. import urls 

class AmazonSitemap(Sitemap):

    def items(self):
     
       return (Amazon.objects.all())
     
class FlipkartSitemap(Sitemap):

    def items(self):
       
       return Shopclues.objects.all()

class SnapdealSitemap(Sitemap):

    def items(self):

       return Snapdeal.objects.all()

class ShopcluesSitemap(Sitemap):

    def items(self):

       return Shopclue.objects.all()

class StaticSitemaps(Sitemap):
  
    def items(self):
       
       return ['AboutUs','Contactus','Terms&Conditions','flipkart','Amazon','Shopclues','Snapdeal']

    def location(self,item):

       return reverse(item)
