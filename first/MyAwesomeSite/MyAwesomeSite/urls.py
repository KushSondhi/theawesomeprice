"""MyAwesomeSite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import path,include
from django.conf.urls import handler404 , handler500
from django.conf import settings
from django.conf.urls.static import static 
#import wordpress_api
from PageScrape.sitemaps import AmazonSitemap,ShopcluesSitemap,FlipkartSitemap,SnapdealSitemap, StaticSitemaps
from PageScrape import views as pviews
#from Blog import views as views
sitemaps={
     'amazon':AmazonSitemap,
     'flipkart':FlipkartSitemap,
     'shopclues':ShopcluesSitemap,
     'Snapdeal':SnapdealSitemap,
     'Static':StaticSitemaps,
}
urlpatterns = [
    path('crazy-admin/', admin.site.urls),
    path('sitemap.xml',sitemap,{'sitemaps':sitemaps}),
   # path('post/<str:page_url>',views.post,name='post'), 
   path("",include("PageScrape.urls")),
   path('AboutUs/',pviews.aboutus,name='AboutUs'),
  path('ContactUs/',pviews.contactus,name='Contactus'),
  path("Terms-And-Conditions",pviews.terms,name="Terms&Conditions"),
  path("flipkart",pviews.OnlyFlipkart,name='flipkart'),
  path("shopclues",pviews.OnlyShopclues,name="Shopclues"),
  path("snapdeal",pviews.OnlySnapdeal,name="Snapdeal"),
  path("amazon",pviews.OnlyAmazon,name="Amazon"),
   path('blog/',include('Blog.urls')),

]

handler404='PageScrape.views.handler404'
handler500='PageScrape.views.handler500'
