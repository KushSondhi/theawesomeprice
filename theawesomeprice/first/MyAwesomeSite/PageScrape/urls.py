from django.urls import path
from .import views
from django.contrib.sitemaps.views import sitemap
from. import classtest
from django.conf.urls import handler404, handler500
urlpatterns=[
    path('testingg',views.homecss,name='testingg'),
    path("update0123",views.index,name="updateproducts"),
    path("Homepage",views.OnlyFlipkart,name="home"),
    path("",views.OnlyFlipkart,name="Flipkart"),
#    path("flipkart",views.OnlyFlipkart,name='flipkart'),
 #   path("shopclues",views.OnlyShopclues,name="Shopclues"),
  #  path("snapdeal",views.OnlySnapdeal,name="Snapdeal"),
   # path("amazon",views.OnlyAmazon,name="Amazon"),
   # path("checking",views.Check,name="Check"),
    path("snapdeal/product=<str:myid>",views.ProductPageSnapdeal,name="ProductPageSnapdeal"),
    path("shopclues/product=<str:myid>",views.ProductPageShopclues,name="ProductPageShopclues"),
    path("flipkart/product=<str:myid>",views.ProductPageFlipkart,name="ProductpageFlipkart"),
    path("Amazon/product=<str:myid>",views.ProductPageAmazon,name="ProductPageAmazon"),
    path("products/snapdeal/filter=<str:SubCat>/page=<int:page_no>",views.FilterByCatSnapdeal,name="FilterProductsSnapdeal"),
    path("products/shopclues/filter=<str:SubCat>/ID_page=<int:page_id>",views.FilterByCatShopclues,name="FilterProductsShopclues"),
    path("products/flipkart/filter=<SubCat>/IdPage=<int:page_no>",views.FilterByCatFlipkart,name="FilterProductsFlipkart"),
    path("products/amazon/filter=<SubCat>/p_no=<int:p_no>",views.FilterByCatAmazon,name="FilterByCatAmazon"),
   path("search/results/page_no=<int:page_no>",views.Checksearch,name="Search"),
  # path("Terms-And-Conditions",views.terms,name="Terms&Conditions"),
  # path("AboutUs",views.aboutus,name="AboutUS"),
 #  path("ContactUs",views.contactus,name="Contactus"),
  path("mobile",views.change_category,name="Mobile"),
 #  path('post/<str:page_url>',views.post,name='all_urls')
   path('ads.txt',views.ads,name='ads'),
]

handler404= views.handler404
#handler500= views.handler500
