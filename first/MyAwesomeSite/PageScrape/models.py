from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
import django.contrib.postgres.search

class Shopclues(models.Model):
    prod_id=models.AutoField
    prod_name=models.CharField(max_length=1000,default=None,null=True)
    prod_temp_name=models.CharField(max_length=60,default=None,null=True)
    prod_url_title=models.CharField(max_length=10000,default="")
    prod_image_URL=models.CharField(max_length=10000,default=None,null=True)
    prod_display_image_URL=models.CharField(max_length=10000,default=None,null=True)
    prod_price=models.CharField(max_length=50,default="")
    prod_mrp=models.CharField(max_length=50,default="")
    prod_URL=models.CharField(max_length=800,null=True,default=None)
    prod_page_URL=models.CharField(max_length=2000,null=True,default=None)
    prod_ratings=models.CharField(max_length=50,null=True,default=None)
    prod_reviews=models.CharField(max_length=50,null=True,default=None)
    prod_overall=models.CharField(max_length=50,null=True,default=None)
    prod_star=models.CharField(max_length=50,null=True,default=None)
    prod_specs_left=models.CharField(max_length=8000,default=None,null=True)
    prod_specs_right=models.CharField(max_length=8000,default=None,null=True)
    prod_top_Category=models.CharField(max_length=40,default=None,null=True)
    prod_First_Category=models.CharField(max_length=100,default=None,null=True)
    prod_Second_Category=models.CharField(max_length=100,default=None,null=True)
    prod_Third_Category=models.CharField(max_length=100,default=None,null=True)
    prod_Date=models.CharField(max_length=20,default=str(datetime.now().date()),null=True)
 #   prod_offer=models.TextField()
    def __str__(self):
        return (self.prod_name)
    def get_absolute_url(self):
       return (''+str(self.prod_page_URL))


class Snapdeal(models.Model):
    prod_id=models.AutoField
    prod_name=models.CharField(max_length=1000,default=None,null=True)
    prod_temp_name=models.CharField(max_length=60,default=None,null=True)
    prod_page_URL=models.CharField(max_length=2000,default=None,null=True)
    prod_url_title=models.CharField(max_length=10000,default=None,null=True)
    prod_price=models.CharField(max_length=50,default=None,null=True)
    prod_mrp=models.CharField(max_length=50,default=None,null=True) 
    prod_URL=models.CharField(max_length=600,null=True,default=None)
    prod_ratings=models.CharField(max_length=200,null=True,default=None)
    prod_reviews=models.CharField(max_length=300,null=True,default=None)
    prod_overall=models.CharField(max_length=20,null=True,default=None)
    prod_image_URL=models.CharField(max_length=400,null=True,default=None)
    prod_top_Category=models.CharField(max_length=40,null=True,default=None)    
    prod_First_Category=models.CharField(max_length=100,default=None,null=True)
    prod_Second_Category=models.CharField(max_length=100,default=None,null=True)
    prod_Third_Category=models.CharField(max_length=100,default=None,null=True)
    prod_specs_left=models.CharField(max_length=1000,default=None,null=True)
    prod_specs_right=models.CharField(max_length=1000,default=None,null=True)
    prod_description=models.CharField(max_length=5000,default=None,null=True)
    prod_highlights=models.CharField(max_length=2000,default=None,null=True)
    prod_Date=models.CharField(max_length=20,default=str(datetime.now().date()),null=True)

    def __str__(self):
        return (self.prod_name)

    def get_absolute_url(self):
       return (''+str(self.prod_page_URL))


class Shopclue(models.Model):

    prod_id=models.AutoField
    prod_name=models.CharField(max_length=10000,default=None,null=True)
    prod_temp_name=models.CharField(max_length=60,default=None,null=True)
    prod_url_title=models.CharField(max_length=10000,default="")
    prod_price=models.CharField(max_length=50,default=None,null=True)
    prod_mrp=models.CharField(max_length=50,default=None,null=True)
    prod_page_URL=models.CharField(max_length=2000,default=None,null=True)
    prod_URL=models.CharField(max_length=800,null=True,default=None)
    prod_ratings=models.CharField(max_length=10000,null=True,default=None)
    prod_reviews=models.CharField(max_length=2000,null=True,default=None)
    prod_overall=models.CharField(max_length=2000,null=True,default=None)
    prod_image_URL=models.CharField(max_length=400,null=True,default=None)
    prod_top_Category=models.CharField(max_length=40,null=True,default=None)
    prod_First_Category=models.CharField(max_length=100,default=None,null=True)
    prod_Second_Category=models.CharField(max_length=100,default=None,null=True)
    prod_Third_Category=models.CharField(max_length=100,default=None,null=True)
    prod_specs_left=models.CharField(max_length=1000,default=None,null=True)
    prod_specs_right=models.CharField(max_length=1000,default=None,null=True)
#    prod_Offers=models.TextField(null=True)
    prod_Date=models.CharField(max_length=20,default=str(datetime.now().date()),null=True)
   

    def __str__(self):
        return (self.prod_name)
    
    def get_absolute_url(self):
       return (''+str(self.prod_page_URL))


class Amazon(models.Model):
    prod_id=models.AutoField
    prod_name=models.CharField(max_length=1000,default=None,null=True)
    prod_temp_name=models.CharField(max_length=60,default=None,null=True)
    prod_page_URL=models.CharField(max_length=2000,null=True,default=None)
    prod_url_title=models.CharField(max_length=10000,default=None,null=True)
    prod_price=models.CharField(max_length=50,default=None,null=True)
    prod_mrp=models.CharField(max_length=50,default=None,null=True)
    prod_availi=models.CharField(max_length=10000,default=None,null=True)
    prod_image_URL=models.CharField(max_length=90000,default=None,null=True)
    prod_URL=models.CharField(max_length=80000,null=True,default=None)
    prod_specs_left=models.CharField(max_length=80000,default=None,null=True)
    prod_specs_right=models.CharField(max_length=80000,default=None,null=True)
    prod_specifications=models.CharField(max_length=10000,default=None,null=True)
    prod_description=models.CharField(max_length=10000,default=None,null=True)
    prod_top_Category=models.CharField(max_length=40,default=None,null=True)    
    prod_First_Category=models.CharField(max_length=40,default=None,null=True)
    prod_Second_Category=models.CharField(max_length=40,default=None,null=True)
    prod_reviews=models.CharField(max_length=1000,default=None,null=True)
    prod_ratings_1start=models.CharField(max_length=10,default=None,null=True)
    prod_ratings_2start=models.CharField(max_length=10,default=None,null=True)
    prod_ratings_3start=models.CharField(max_length=10,default=None,null=True)
    prod_ratings_4start=models.CharField(max_length=10,default=None,null=True)
    prod_ratings_5start=models.CharField(max_length=10,default=None,null=True)
    prod_ratings_FeatureKey=models.CharField(max_length=10000,default=None,null=True)
    prod_ratings_FeatureValue=models.CharField(max_length=10000,default=None,null=True)
    prod_Date=models.CharField(max_length=20,default=str(datetime.now().date()),null=True)
    prod_affiliate_URL=models.CharField(max_length=500,default=None,null=True)

    def __str__(self):
        return (self.prod_name)        
    def get_absolute_url(self):
       return (''+str(self.prod_page_URL))
       # return reverse('post',args=[str(self.prod_url_title)])

