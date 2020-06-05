from django.template import RequestContext
from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
import requests
from django.contrib.postgres.search import TrigramSimilarity
from  fuzzywuzzy import fuzz
import difflib
from math import ceil
# from haystack.query import SearchQuerySet
# from.import SearchHaystack
import random
# from haystack import indexes
from bs4 import BeautifulSoup as soup
from.import classtest
from .models import Shopclues,Snapdeal,Shopclue,Amazon
import datetime
from datetime import time
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
import wordpress_api
# Create your views here.

Flipkart_products=Shopclues.objects.all()
Amazon_products=Amazon.objects.all()
Shopclues_products=Shopclue.objects.all()
Snapdeal_products=Snapdeal.objects.all()

all_product_flipkart=[p.prod_name for p in Flipkart_products]
all_products_amazon=[a.prod_name for a in Amazon_products]
all_products_shopclues=[s.prod_name for s in Shopclues_products]
all_products_snapdeal=[n.prod_name for n in Snapdeal_products]

PastProducts=[]

def index(request):

    UserAgents=[
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322",
                  'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)',
                  'Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)',
                  "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
                  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 2.0.50727; .NET CLR 1.1.4322)",
                  "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
                  "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; InfoPath.1; .NET CLR 2.0.50727)",
                  "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.0.7) Gecko/20060909 Firefox/1.5.0.7",
                  "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0)",
                  "Mozilla/4.0 (compatible; MSIE 5.0; Windows 98; DigExt)",
                  "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.2; Win64; x64; Trident/6.0; .NET4.0E; .NET4.0C; Microsoft Outlook 15.0.4763; ms-office; MSOffice 15)",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0"
    ]

    header={"User-Agent":UserAgents[0]}
#     proxy={"http":"170.79.16.19:8080","https":"170.79.16.19:8080"}
    
    
    product_prices=[]
    product_names=[]
    product_mrps=[]
    product_urls=[]
    
    del product_mrps[:]
    del product_names[:]
    del product_urls[:]
    del product_prices[:]
    
    left_col_flipkart=[]
    right_col_flipkart=[]

    left_col_shopclues=[]
    right_col_shopclues=[]
    
    left_col_snapdeal=[]
    right_col_snapdeal=[]
    highlights_snapdeal=[]
    
    related_products_shopclues_urls=[]
    
    related_products_flipkart_urls=[]

    related_products_snapdeal_urls=[]

    related_products_amazon_urls=[]
    related_products_amazon=[]
    
    
    total_flipkart=[]

    total_shopclues=[]

    total_snapdeal=[]
    products_snap=[]         
  
    def search(request):

      link=request.POST.get("search","default")        
      print(link)
      if link[12]=="a":
            return AddToAmazon(link)
      elif "snapdeal" in link:
            return AddToSnapdeal(link)
      elif link[13]=="h":
            return AddToShopclues(link)     
      return render(request,"HTML Files/basic.html")
 
    def AddProductAmazonDatabase(request,productname):

          obj1=classtest.Index()
          obj1.URLforAmazon(productname)
          return HttpResponse("<h2>All Products Added To Amazon DataBase</h2>")

    def AddProductFlipkartDatabase(request,productname):

          obj1=classtest.Index()
          obj1.URLforFlipkart(productname)


          return HttpResponse("<h2>All products Added To Flipkart Database</h2>")

    def AddProductShopcluesDatabase(request,productname):

          obj1=classtest.Index()
          obj1.URLforShopclues(productname)  
          return HttpResponse("<h2>All Products Added To Shopclues Database</h2>")

    def AddProductSnapdealDatabase(request,productname):

          obj1=classtest.Index()
          print(obj1.URLforSnapdeal(productname))
          return HttpResponse("<h2>All Products Added To Snapdeal Database</h2>")   

    def UPDATEFLIPKART(request):
        objf=classtest.Index()
        UpdatingProducts=Shopclues.objects.all();    i=0
        for p in UpdatingProducts[0:]:
                try: 
                  objf.StartAddingProductsFlipkart(p.prod_URL) 
                  p.save()
                except:
                     print("passed"+str(i))
                print(i)
                i+=1 
        print('Total Products :- '+str(len(Shopclues.objects.all())))      
        return HttpResponse("updates")

    def UPDATESNAPDEAL(request):
          
          #obj1=classtest.Index()
          UpdatingProducts=Snapdeal.objects.all()
          print('Total Products to have Update='+str(len(UpdatingProducts)))
          i=0
          obj=classtest.Index()
          for p in UpdatingProducts[0:]:
                try:
                  #   obj=classtest.Index()
                     #print(p.prod_Date)
                     print(i)
                  #   p.prod_top_Category="Men & Women"
                     obj.StartAddingProductsSnapdeal(p.prod_URL)
                     p.save()
                      #print(p.prod_page_URL)
                     print('DATE AFTER UPDATE :-')
        #             print(p.prod_Date)
                except:
                      print("passed"+str(i))
                i=i+1
          print(len(Snapdeal.objects.all()))
          return HttpResponse("Shown")

    def UPDATEAMAZON(request):
          obj1=classtest.Index()
          Amazon_products=Amazon.objects.all()
          all_urls=[]
          for prod in Amazon_products:
                all_urls.append(prod.prod_URL)
          print(len(all_urls)) 
          i=100
          for url in all_urls[100:200]:
                print(i)
                try:
                    print(obj1.StartAddingProductsAmazon(url))
                    
                except:
                      print(str(i)+"Passed")
                i=i+1
          return HttpResponse("Shown")

    def UPDATESHOPCLUESPRODUCTS(request):
    
          obj1=classtest.Index()
          UpdatingProducts=Shopclue.objects.all()
          print('Total Products to have Update='+str(len(UpdatingProducts)))
          i=0
          for p in UpdatingProducts:
                try:
                  #    print(p.prod_Date)
                      print(i)
                     # p.prod_top_Category="Home"
                      #p.save()
                      #ur=str(p.prod_page_URL).replace('/shopclues/shopclues','/shopclues')
                      #p.prod_page_URL=ur
                      obj1.StartAddingProductsShopclues(p.prod_URL)
                      #url=p.prod_page_URL
                      #ur=url.replace('.comshopclues','.com/shopclues')
                     # p.prod_page_URL=ur
                      #p.save()
                      #print(p.prod_page_URL)
                except:
                      print("passed"+str(i))
                i=i+1
          return HttpResponse("Shown")

#    return UPDATESNAPDEAL(request)
#    return UPDATESHOPCLUESPRODUCTS(request)  
    return UPDATEFLIPKART(request)
#   return UPDATEAMAZON(request)
#     return SendData()
#     return search(request)
#    return(StartAddingProductsFlipkart(Flipkart_urls[0]))
#     return(StartAddingProductsShopclues(Shopclues_urls[0]))
#     return(StartAddingProductsSnapdeal(Snapdeal_urls[0]))
#    return AddProductAmazonDatabase(request,"Oppo F11")
#    return AddProductFlipkartDatabase(request,"Multivitamin")
#   return AddProductShopcluesDatabase(request,"Redmi note 9 accessories")
#    return AddProductSnapdealDatabase(request,"adidas drogo ")
#     return searchfuzz(request)
#     return URLforAmazon("Power Bank")
#     return StartAddingProductsAmazon(Amazon_urls[0])
#     return updateamazonproducts(request)
def testingg(request):
  return render (request,"HTML Files/comOnlyFlipkart.html")

def handler404(request):
    print("In handler 404")
    return render(request,'HTML Files/error_500.html')
    
def handler500(request):
    print("in handler 500")
    return render (request,'HTML Files/error_500.html')
    
    

def AddToFlipkart(request,link):

      obj1=classtest.Index()
      new_item_flipkart=obj1.StartAddingProductsFlipkart(link)  
     # related_shopclues=(obj1.URLforShopclues(new_item_flipkart))
      #related_snapdeal=(obj1.URLforSnapdeal(new_item_flipkart))  
     # related_amazon(obj1.URLforAmazon(new_item_flipkart))

     # print(related_shopclues)
     # print(related_snapdeal)
     # print(related_amazon)     
      Product=Shopclues.objects.filter(prod_name=new_item_flipkart)
      for Pd in Product:
            Prd=Pd
     # print("\n\nflipkart Product "+Prd.prod_name+" added to Database")
      return(ProductPageFlipkart(request,Prd.prod_url_title))

def AddToShopclues(request,link):

      obj1=classtest.Index()
      new_product_name=obj1.StartAddingProductsShopclues(link)
      related_snapdeal=obj1.URLforSnapdeal(new_product_name)
      related_flipkart=obj1.URLforFlipkart(new_product_name)
      #related_amazon=obj1.URLforAmazon(new_product_name)
      
      print(related_snapdeal)
      print(related_flipkart)
      #print(related_amazon)

      # Product_Name_Shopclues=StartAddingProductsShopclues(link)
      Product=Shopclue.objects.filter(prod_name=new_product_name)
      for Pd in Product:
            Prd=Pd
      print("Shopclues Product "+new_product_name+" Added To Database")
      return(ProductPageShopclues(request,Prd.prod_url_title))

def AddToSnapdeal(request,link):
      obj1=classtest.Index()
      Product_Name_Snapdeal=obj1.StartAddingProductsSnapdeal(link)
      Product=Snapdeal.objects.filter(prod_name=Product_Name_Snapdeal)
      print("NEW PRODUCT_____>"+Product)
      for prd in Product:
            prd=prd
      print("snapdeal product "+prd.prod_name+" added To snapdeal DATABASE")
      obj=classtest.Index()
     #print(obj.URLforAmazon(prd.prod_name))
      print(obj.URLforFlipkart(prd.prod_name))
      print(obj.URLforShopclues(prd.prod_name))

      return ProductPageSnapdeal(request,prd.prod_url_title)

def AddToAmazon(request,link):

      obj1=classtest.Index()
      new_item_amazon=obj1.StartAddingProductsAmazon(link)  
      related_shopclues=(obj1.URLforShopclues(new_item_amazon))
      related_snapdeal=(obj1.URLforSnapdeal(new_item_amazon))  
      related_flipkart=(obj1.URLforFlipkart(new_item_amazon))

      print(related_shopclues)
      print(related_snapdeal)
      print(related_flipkart)     
      Product=Amazon.objects.filter(prod_name=new_item_amazon)
      for rd in Product:
            Prd=rd
      print("Amazon Product "+Prd.prod_name+" added to Database")
      return(ProductPageAmazon(request,Prd.prod_url_title)) 

def search(request):

      link=request.GET.get("search","default")        
      print("here--------->"+link)
      if "flipkart" in link:
            return AddToFlipkart(request,link)
      if "amazon" in link:
            return AddToAmazon(request,link)
      if "shopclues" in link:
            return AddToShopclues(request,link)
      if "snapdeal" in link:
            return AddToSnapdeal(request,link)
      else:
            return HttpResponse("<h2>Not Found</h2>")

def home(request):

      trendingprods=Shopclues.objects.filter(prod_Second_Category="Mobiles")
      i=int(random.randrange(0,len(trendingprods)-8))
      Trendingprods=trendingprods[i:i+8]
      nAmazon=len(Amazon_products[0:20])
      nSlides=nAmazon//4+ceil((nAmazon/4)-(nAmazon//4))
      i=random.randrange(0,100)
      contex={
            "no_of_slides":nSlides,
            "range":nSlides,
            "AmazonTrending":Amazon_products[i:i+20],
            "ShopcluesTrending":Shopclues_products[i:i+20],
            "SnapdealTrending":Snapdeal_products[i:i+20],
            "FlipkartTrending":Flipkart_products[i:i+20],
            "TrendingProductsFlipkart":Trendingprods[0:4],
            "TrendingProductsitemsFlipkart":Trendingprods[4:8]
      }                     
      return render(request,"HTML Files/HomeProductPage.html",context=contex)

def OnlyFlipkart(request):


      del PastProducts[:]

      if len(PastProducts)<=30:
         del PastProducts[:]
         SomeItems=Shopclues.objects.filter(prod_top_Category="Men & Women")
         a=random.randint(0,len(SomeItems)-40)
         Si=SomeItems[a:a+35]
         for i in range(35):
             PastProducts.append(Si[i])
         

      # current=datetime.datetime.now().time()

      SecondCats=["Speakers","Gaming Accessories","Laptops","Mobiles","Furniture Accessories","Beauty Accessories","Smart Watches","Strollers & Activity Gear","Men's Footwear","Dining Tables & Sets","PIRASO Sunglasses","Baby Proofing & Safety","Women's Clothing","Books","Health & Nutrition","Makeup","Fragrances","Smart Watches","Headphones","Games","Televisions"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

    #  print(PastProducts)
      #print("Firt Product------->>>>")
      #for i in PastProducts[0]:
      #       print(i.prod_top_Category)
      RecentProducts=Shopclues.objects.filter(prod_Second_Category="Cameras")
      b=random.randint(0,len(RecentProducts)-10)
      Cameras=[i for i in RecentProducts[b:b+10]]
      Mobiles=[]
      M=Shopclues.objects.filter(prod_Second_Category='Mobiles')
      Smartphones=[j for j in M if "Apple" or "Samsung" or "Redmi" in j.prod_name]
      for i in range(3):
            for j in range(1):
                  r=random.randint(0,len(Smartphones)-10)
                  m=(Smartphones[r:r+4])
                  PastProducts.append(Smartphones[0])
            Mobiles.append(m)
      #print(Mobiles[0])
      select_camera=random.randint(0,30)
      #print(PastProducts)
      #print(PastProducts[0:4])
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

      contex={
            "brand":"flipkart",
            "page":"IdPage",
            "Featured":PastProducts[0:4],
            "TopSelling":PastProducts[4:8],
            "NewArrivals":PastProducts[8:12],
            "Cameras":Cameras[0:10],
            "Mobiles_0":Mobiles[0],
            "Mobiles_1":Mobiles[1:],
            "DownCats1":DownCats1,
            "DownCats2":DownCats2,
            'Sl1':PastProducts[12:16],
            'Sl2':PastProducts[16:20],
            'Sl3':PastProducts[20:24],
            'CANONICAL_PATH':CANONICAL_PATH,
            'Flipkart':'Flipkart',
      }
      # now=datetime.datetime.now().time()
      return render(request,'HTML Files/OnlyFlipkart.html',context=contex)

def homecss(request):
   return render (request,"HTML Files/comFiltered.html")

def change_category(request):
      

      def toadd(top_cat):

            all_cats=[]
            all_sub_cats=[]
            All_Prods_Sub_Cats=[]
            all_cats_sub_cats=[]
            for product in top_cat:
                  all_cats.append(product.prod_First_Category)
            all_cats=set(all_cats)
            all_cats=list(all_cats)

            for category in all_cats:
                  products=Shopclues.objects.filter(prod_First_Category=category)
                  all_sub_cats={(product.prod_Second_Category) for product in products}
                  all_sub_cats=list(all_sub_cats)
                  All_Prods_Sub_Cats.append(all_sub_cats)
            all_cats_sub_cats=list(zip(all_cats,All_Prods_Sub_Cats))
            top_cat_section=(all_cats_sub_cats)
            return top_cat_section

      Electronics=[p for p in Shopclues.objects.filter(prod_top_Category="Electronics")]
      elec_section=toadd(Electronics)
      MenWomen=[p for p in Shopclues.objects.filter(prod_top_Category="Men & Women")]
      men_sec=toadd(MenWomen)
      Books=[p for p in Shopclues.objects.filter(prod_top_Category="Books")]
      book_sec=toadd(Books)
      Others=[p for p in Shopclues.objects.filter(prod_top_Category="Others")]
      other_sec=toadd(Others)
      Home=[p for p in Shopclues.objects.filter(prod_top_Category="Home")]
      home_sec=toadd(Home)
      Gym=[p for p in Shopclues.objects.filter(prod_top_Category="Gym")]
      gym_sec=toadd(Gym)

      print(home_sec)
      print(elec_section)
      contex={
       "brand":"flipkart",
       "page":"IdPage",
       "Electronics":elec_section,
       "MenWomen":men_sec,
       "Others":other_sec,
       "Home":home_sec,
       "Books":book_sec,
       "Gym":gym_sec,
      }

                  
      return render(request,"HTML Files/FlipkartNavbar.html",context=contex)

def Check(request):

      products=Shopclues.objects.all()
      i=1
      for n in products:
            url=n.prod_page_URL
            n.prod_page_URL=url.replace("/MyAwesomeSite","")
            n.save()
            print(n.prod_page_URL)
            # p.prod_mrp=p.prod_mrp.replace("MRP","").replace("(Inclusive of all taxes)","").replace("Rs.","").replace("  ","").replace("\n","").strip()
            # print(len(products))
            # print(n.prod_Date[8:10])
            # url="product/shopclues/ID_page="+n.
            # p.prod_page_URL="/MyAwesomeSite/product/snapdeal/page="+p.prod_url_title
            # print(n.prod_url_title)
            
      return render(request,"HTML Files/Checking.html")

# def ChangeId(request,page_id):

      # NewId=hashlib.md5()
      # NewId.update(page_id.encode())
      # NewId.digest()
      # print(NewId)
      # return OnlyShopclues(request,NewId)

def OnlyShopclues(request):


      Shopclues_productS=Shopclue.objects.all()
      Shopclues_products_beg=set(Shopclues_productS)
      Shopclues_products=list(Shopclues_products_beg)
      
      #<-----------------------------Function To add Cat and sub Cat---------------------------->
      
      SecondCats=["Kitchen Appliances","Laptops","Storage Devices","Smartphones","Furniture Accessories","Travel Accessories","Men's Clothing","DSLR Lenses","Camcorder","DSLR Lenses","Women's Clothing","Books","Unboxed Cameras & Accessories","Large Home Appliances","Desktops & Monitors","Kitchen and Dining","Office Electronics","Large Home Appliances","Smartphones","Bike Accessories"]

      if len(PastProducts)<35:
          Past=Shopclue.objects.filter(prod_Second_Category="Women's Clothing")
          for i in range(36):
            PastProducts.append(Past[i])
      print("TOTAL PAST PRODUCTS : "+ str(len(PastProducts)))
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

     # SideBar_Product=[Shopclue.objects.filter(prod_Second_Category="Large Home Appliances")[random.randint(0,10)]]
      
      RecentProducts=Shopclue.objects.filter(prod_Second_Category="DSLR Cameras")
      Cameras=[i for i in RecentProducts]
      random.shuffle(Cameras)
      MobileBrands=["Samsung Mobiles","OPPO Mobiles","Vivo Mobiles","Realme Mobiles","Asus Mobiles"]
      Mobiles=[]
      M=Shopclue.objects.filter(prod_Second_Category='Smartphones')
      Smartphones=[j for j in M if "Apple" or "Samsung" or "Redmi" in j.prod_name]
      for i in range(3):
            for j in range(1):
                  r=random.randint(0,len(Smartphones)-10)
                  m=(Smartphones[r:r+4])
            Mobiles.append(m)
      print(Mobiles[0])
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
      contex={
            "brand":"shopclues",
            "page":"ID_page",
            "Featured":PastProducts[0:4],
            "TopSelling":PastProducts[4:8],
            "NewArrivals":PastProducts[8:12],
            "SideBar_Product":[PastProducts[7]],
            "BestSellers":PastProducts[12:18],
            "Cameras":Cameras[0:10],
            "Mobiles_0":Mobiles[0],
            "Mobiles_1":Mobiles[1:],
            "FeaturedDown":PastProducts[18:22],
            "TopRatedDown":PastProducts[22:26],
            "OnSaleDown":PastProducts[26:30],
            "DownCats1":DownCats1,
            "DownCats2":DownCats2,
            'Sl1':PastProducts[30:34],
            'Sl2':PastProducts[4:8],
            'Sl3':PastProducts[10:14],
            'CANONICAL_PATH':CANONICAL_PATH,
            'Shopclues':'Shopclues',
      }
      
      return render(request,"HTML Files/OnlyFlipkart.html",context=contex)

def OnlySnapdeal(request):
      
      Snapdeal_productS=Snapdeal.objects.all()
      Snapdeal_products_beg=set(Snapdeal_productS)
      Snapdeal_products=list(Snapdeal_products_beg)


      # Function To Add Category And Sub Category In To Category------------------------------------------>

      SecondCats=["Gaming Accessories","Large Appliances","Televisions","Headphones & Earphones","Laptops","Clocks","Sunglasses","Top Wear","Dresses, Gowns & Jumpsuits","Shirts","Fiction Books","Luggage & Suitcases","Mobile Phones","Men's Accessories","Table & Kitchen Linen","Kurtis","Bottom Wear","Computer Components","Kitchen Appliances","Winter Wear"]

      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]
      
     # SideBar_Product=[Snapdeal.objects.filter(prod_Second_Category="Computer Components")[random.randint(0,10)]]

      if len(PastProducts)<=30:
        print("NO PAST PRODUCTS ")
        SomeProducts=Snapdeal.objects.filter(prod_First_Category="Men's Clothing")
        a=random.randint(0,len(SomeProducts)-40)
        for i in range(35):
            PastProducts.append(SomeProducts[i])
        print("LENGTH OF PAST PRODUCTS :-"+str(len(PastProducts))) 

      
      RecentProducts=Snapdeal.objects.filter(prod_Second_Category="Living Room")
      Cameras=[i for i in RecentProducts]
      random.shuffle(Cameras)
      MobileBrands=["Samsung Mobiles","OPPO Mobiles","Vivo Mobiles","Realme Mobiles","Asus Mobiles"]
      Mobiles=[]
      M=Snapdeal.objects.filter(prod_Second_Category='Mobile Phones')
      Smartphones=[j for j in M if "Apple" or "Samsung" or "Redmi" in j.prod_name]
      for i in range(3):
            for j in range(1):
                  r=random.randint(0,len(Smartphones)-10)
                  m=(Smartphones[r:r+4])
            Mobiles.append(m)
      print(Mobiles[0])
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
      contex={
            "brand":"snapdeal",
            "page":"page",
            "Featured":PastProducts[0:4],
            "TopSelling":PastProducts[4:8],
            "NewArrivals":PastProducts[8:12],
            
            
            "Cameras":Cameras[0:10],
            "Mobiles_0":Mobiles[0],
            'Mobiles_1':Mobiles[1:],
            "FeaturedDown":PastProducts[18:22],
            "TopRatedDown":PastProducts[22:26],
            "OnSaleDown":PastProducts[26:30],
            "DownCats1":DownCats1,
            "DownCats2":DownCats2,
            "Sl1":PastProducts[30:34],
            'Sl2':PastProducts[6:10],
            'Sl3':PastProducts[14:18],
            'CANONICAL_PATH':CANONICAL_PATH,
            'Snapdeal':'Snapdeal',
      }
      return render(request,"HTML Files/OnlyFlipkart.html",context=contex)

def OnlyAmazon(request):

      all_sub_cats=[]
      All_Sub_cats=[]
      all_prods=[]
      All_Prods=[]
      catwise_prods=[]
      Amazon_products_top_cats=[]

      Amazon_productS=Amazon.objects.all()
      Amazon_products_beg=set(Amazon_productS)
      Amazon_products=list(Amazon_products_beg)

      # Function To Add Category And Sub Category In To Category------------------------------------------>
      def toadd(top_cat):
            
            all_cats=[]
            all_sub_cats=[]
            All_Prods_Sub_Cats=[]
            all_cats_sub_cats=[]
            for product in top_cat:
                  all_cats.append(product.prod_First_Category)
            all_cats=set(all_cats)
            all_cats=list(all_cats)
            
            for category in all_cats:
                  products=Amazon.objects.filter(prod_First_Category=category)
                  all_sub_cats={(product.prod_Second_Category) for product in products}
                  all_sub_cats=list(all_sub_cats)
                  All_Prods_Sub_Cats.append(all_sub_cats)
            all_cats_sub_cats=list(zip(all_cats,All_Prods_Sub_Cats))
            top_cat_section=(all_cats_sub_cats)
            return top_cat_section

      Electronics=[p for p in Amazon.objects.filter(prod_top_Category="Electronics")]
      elec_section=toadd(Electronics)
      MenWomen=[p for p in Amazon.objects.filter(prod_top_Category="Men & Women")]
      men_sec=toadd(MenWomen)
      Books=[p for p in Amazon.objects.filter(prod_top_Category="Books")]
      book_sec=toadd(Books)
      Others=[p for p in Amazon.objects.filter(prod_top_Category="Others")]
      other_sec=toadd(Others)
      Home=[p for p in Amazon.objects.filter(prod_top_Category="Home")]
      home_sec=toadd(Home)
      # Baby=[p for p in Shopclues.objects.filter(prod_top_Category="Baby")]
      # Gym=[]
      # Nonea=[p for p in Amazon.objects.filter(prod_top_Category="None")]
      # none_sec=toadd(Nonea)

      for p in Amazon_products:
            Amazon_products_top_cats.append(p.prod_top_Category)
      Amazon_products_top_cats=set(Amazon_products_top_cats)
      Amazon_products_top_cats=list(Amazon_products_top_cats)
      print(Amazon_products_top_cats)
	
      Featured=[]
      FeaturedDown=[]
      TopSelling=[]
      TopRatedDown=[]
      New_Arrivals=[]
      OnSaleDown=[]

      Sl1=[]
      Sl2=[]
      Sl3=[]

      BestSellers=[]

      SecondCats=['Plants, Seeds & Bulbs',"Home Theater, TV & Video","Biographies, Diaries & True Accounts","Sports Gadgets",'Networking Devices','Printers, Inks & Accessories',"Children's & Young Adult","Handbags","Exercise & Fitness","Computers & Accessories","Wearable Technology","Fragrance","Sexual Wellness & Sensuality","Travel Accessories"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

      items_featured=["Tablets","Mobiles & Accessories","PC Games","Home Theater, TV & Video"]
      items_arrival=["Cameras & Photography","Home Theater, TV & Video",'Tablets',"Shoes"]
      items_top=["Monitors","Football","Desktops","Mobiles & Accessories"]
      
      r=random.randint(0,3)
      print(items_featured[r])
      uids=Amazon.objects.filter(prod_Second_Category=items_featured[r])
      s=random.randint(0,len(uids)-7)
      g=random.randint(0,len(uids)-7)
      Featured=uids[s:s+4]
      FeaturedDown=uids[g:g+4]
      Sl1=uids[s+2:s+6]
      
      uids=Amazon.objects.filter(prod_Second_Category=items_top[r])
      s=random.randint(0,len(uids)-7)
      g=random.randint(0,len(uids)-7)
      Top_Selling=uids[s:s+4]
      TopRatedDown=uids[g:g+4]
      BestSellers=uids[g:g+7]
      Sl2=uids[s+2:s+6]


      uids=Amazon.objects.filter(prod_Second_Category=items_arrival[r])
      s=random.randint(0,len(uids)-6)
      g=random.randint(0,len(uids)-6)
      New_Arrivals=uids[s:s+4]
      OnSaleDown=uids[g:g+4]
      Sl3=uids[s+1:s+5]
      
      SideBar_Product=[Amazon.objects.filter(prod_Second_Category="Monitors")[random.randint(0,10)]]
      
      RecentProducts=Amazon.objects.filter(prod_Second_Category="Cameras & Photography")
      Cameras=[i for i in RecentProducts]
      select_camera=random.randint(0,len(Cameras)-12)
      MobileBrands=["Samsung Mobiles","OPPO Mobiles","Vivo Mobiles","Realme Mobiles","Asus Mobiles"]
      RecentMobiles=Amazon.objects.filter(prod_Second_Category="Mobiles & Accessories")
      Mobiles=[]
      M=Amazon.objects.filter(prod_Second_Category='Mobiles & Accessories')
      Smartphones=[j for j in M if "Apple" or "Samsung" or "Redmi" in j.prod_name]
      for i in range(3):
            for j in range(1):
                  r=random.randint(0,len(Smartphones)-10)
                  m=(Smartphones[r:r+4])
            Mobiles.append(m)
  #    print(Mobiles[0])
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
      contex={
            "brand":"amazon",
            "page":"p_no",
            "Electronics":elec_section,
            "MenWomen":men_sec,
            "Others":other_sec,
            "Home":home_sec,
            "Books":book_sec,
            "Featured":Featured,
            "TopSelling":Top_Selling,
            "NewArrivals":New_Arrivals,
            "SideBar_Product":SideBar_Product,
            "BestSellers":BestSellers[0:6],
            "Cameras":Cameras[select_camera:select_camera+10],
            "Mobiles_0":Mobiles[0],
            'Mobiles_1':Mobiles[1:],
            "FeaturedDown":FeaturedDown,
            "OnSaleDown":OnSaleDown,
            "TopRatedDown":TopRatedDown,
            "DownCats1":DownCats1,
            "DownCats2":DownCats2,
            'Sl1':Sl1,
            'Sl2':Sl2,
            'Sl3':Sl3,
            'CANONICAL_PATH':CANONICAL_PATH
      }

      return render (request,"HTML Files/OnlyFlipkart.html",context=contex)

def ProductPageShopclues(request,myid):

            if len(PastProducts)>36:
               del PastProducts[0]

            left_col=[]
            right_col=[]
            ProductsSnapdeal=[]
            ProductsFlipkart=[]
            ProductsAmazon=[]

            product_shopclues=Shopclue.objects.filter(prod_url_title=str(myid))
                
            print('Total filtered products:'+str(len(product_shopclues)))
            if len(product_shopclues)>1:
                  print('inside if')
                  dates=[]
                  for i in product_shopclues:
                        raw_date=str(i.prod_Date).replace("-","")
                        dates.append(int(str(raw_date)))
                  print(dates)
                  maxdate=max(dates)
                  pos=dates.index(maxdate)
                  print("Newest Product is at index:"+str(pos))
                  for m,j in enumerate(product_shopclues):
                        if m!=int(pos):
                              j.delete()
                  product_shopclues=product_shopclues[pos]
            for x in product_shopclues:
                  it=x

            current_date=int(str(datetime.datetime.now().date())[8:])
            existing_date=int(str(it.prod_Date)[8:])
            diff=int(current_date-existing_date)
            print(current_date)
            print(existing_date)
            print(diff)
            #if int(diff)>8:
            #      print(UpdateProductList(request,it.prod_URL))
            
            SecondCats = ["DSLR Cameras","Smartphones","Gaming","Furniture","Women's Clothing","Fragrances","Backpacks & Laptop Bags","Men's Clothing","DSLR Lenses","Camcorder","Refurbished Mobiles","Unboxed Cameras & Accessories","Large Home Appliances","Desktops & Monitors","Kitchen and Dining","Office Electronics","Large Home Appliances","Smartphones","Bike Accessories"]

            DownCats1=SecondCats[0:6]
            random.shuffle(SecondCats)
            DownCats2=SecondCats[0:6]
            
            FlipkartProducts=[item.prod_name for item in Shopclues.objects.filter(prod_top_Category=it.prod_top_Category)]
            SnapdealProducts=[item.prod_name for item in Snapdeal.objects.filter(prod_top_Category=it.prod_top_Category)]
            AmazonProducts=[items.prod_name for items in Amazon.objects.filter(prod_top_Category=it.prod_top_Category)]
                        
            print(len(AmazonProducts))
            print(len(SnapdealProducts))
            d=random.randrange(0,len(Shopclues_products)-10)

            TopRatedDown=[i for i in Shopclues_products[d:d+3]]
            OnSaleDown=[i for i in Shopclues_products[d+3:d+6]]
            FeaturedDown=[x for x in Shopclues_products[d+6:d+9]]

            try:
                  # print(it.prod_specs_right)
                  lwft=it.prod_specs_left.split(",")
                  it.prod_specs_left=list(lwft)
                  right=it.prod_specs_right.split(",")
                  it.prod_specs_right=list(right)
                  # print(it.prod_specs_right)
            except:
                  it.prod_specs_left=[]
                  it.prod_specs_right=[]
            
            FirstCat=it.prod_First_Category
            SecondCat=it.prod_Second_Category
            
            for key in it.prod_specs_left:
                  key=(key.replace("'","").replace("]","").replace("[",""))  
                  left_col.append(key)
            for value in it.prod_specs_right:
                  value=(value.replace("'","").replace("]","").replace("[",""))
                  right_col.append(value)
            
            Species=list(zip(left_col,right_col))

            max_ratioflip=85
            try:
                  nearbyproducts=difflib.get_close_matches(it.prod_name,FlipkartProducts)
                  print('nearby products flipkart :')
                  print(nearbyproducts)
                  for prod in nearbyproducts:
                        ratio=fuzz.token_set_ratio(prod,it.prod_name)
                        if ratio>max_ratioflip:
                              if ratio>=97:
                                    max_ratioflip=ratio
                                    SameFlipkart=prod
                                    break
                              else:
                                    max_ratioflip=ratio
                                    SameFlipkart=prod

                  SameItemFlipkart=SameFlipkart
                  print(max_ratioflip)
                  print("Same item from Flipkart is :- "+ SameFlipkart)
                  SameProductFlipkar=[i for i in Shopclues.objects.filter(prod_name=SameItemFlipkart)]
                  SameProductFlipkart=[]
                  for i in SameProductFlipkar:
                        SameProductFlipkart.append(i)
                        break
                  print(SameProductFlipkart)
            except:
                  SameProductFlipkart=""
            
            max_ratios=90
            try:
                  nearbyproductssnapdeal=difflib.get_close_matches(it.prod_name,SnapdealProducts)
                  print('nearby products snapdeal :')
                  print(nearbyproductssnapdeal)
                  for prosnap in nearbyproductssnapdeal:
                        Ratio=fuzz.token_set_ratio(prosnap,it.prod_name)
                        if Ratio>=max_ratios:
                              if Ratio>=96:
                                    max_ratios=Ratio
                                    SameSnap=prosnap
                                    break
                              else:
                                    max_ratios=Ratio
                                    SameSnap=prosnap  
                  SameItemSnapdeal=SameSnap
                  print(max_ratios)
                  print("Same item from Snapdeal is :- "+ SameSnap)
                  SameProductSnapdea=[i for i in Snapdeal.objects.filter(prod_name=SameItemSnapdeal)]
                  SameProductSnapdeal=[]
                  for i in SameProductSnapdea:
                              SameProductSnapdeal.append(i)
                              break
                  print(SameProductSnapdeal)
            except:
                  SameProductSnapdeal=""
            max_ratio=85
            try:
                  nearbyproductsamazon=difflib.get_close_matches(it.prod_name,AmazonProducts)
                  print('nearby products amazon :')
                  print(nearbyproductsamazon)
                  for pro in nearbyproductsamazon:
                        ratio=fuzz.token_set_ratio(pro,it.prod_name)
                        if ratio>max_ratio:
                              if ratio>=96:
                                    max_ratio=ratio
                                    SameAmazon=pro
                                    break
                              else:
                                    max_ratio=ratio
                                    SameAmazon=pro
                  SameItemAmazon=SameAmazon
                  print(max_ratio)
                  print("Same item from Amazon is :- "+ SameAmazon)
                  SameProductAmazo=[i for i in Amazon.objects.filter(prod_name=SameItemAmazon)]
                  SameProductAmazon=[]
                  for i in SameProductAmazo:
                              SameProductAmazon.append(i)
                              break
                  print(SameProductAmazon)   
            except:
                  SameProductAmazon=""
            PastProducts.append(it)
            title=""
            name=[i for i in str(it.prod_name).split(" ")]
            if len(name)<10:
                title=str(it.prod_name)
            else:
             i=0
             while(i<10):
                title+=str(name[i])+" "
                i+=1
            CANONICAL_PATH=request.build_absolute_uri(request.path)
            if 'www.' in CANONICAL_PATH :
                CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
            contex={
                  "brand":"shopclues",
                  "imagelogo":"/static/assets/images/shopclues.jpg",
                  "page":"ID_page",
                  "TopCat":it.prod_top_Category,
                  "FirstCat":it.prod_First_Category,
                  "SecondCat":it.prod_Second_Category,
                  "product":[product_shopclues[0]],
                  "Species":Species,
                  "SameProductFlipkart":SameProductFlipkart,
                  "SameProductSnapdeal":SameProductSnapdeal,
                  "SameProductAmazon":SameProductAmazon,
                  "TopRatedDown":TopRatedDown,
                  "FeaturedDown":FeaturedDown,
                  "OnSaleDown":OnSaleDown,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  "title":title,
                  'CANONICAL_PATH':CANONICAL_PATH,
                 'Shopclues':'Shopclues'
            }
            
            return render(request,"HTML Files/ProductpageFlipkart.html",context=contex)

def ProductPageSnapdeal(request,myid):
         
            if len(PastProducts)>36:
               del PastProducts[0]
            left_col=[]
            right_col=[]
            ProductsShopclues=[]
            ProductsFlipkart=[]
            ProductsAmazon=[]
            
            d=random.randrange(0,len(Snapdeal_products)-10)
            TopRatedDown=[i for i in Snapdeal_products[d:d+3]]
            OnSaleDown=[i for i in Snapdeal_products[d+3:d+6]]
            FeaturedDown=[x for x in Snapdeal_products[d+6:d+9]]
            
            SecondCats=["Home Appliances","Televisions","Men's Sports Fashion","Winter Wear","Sunglasses","Shirts","Kurtas, Pyjamas & Sherwanis","Innerwear & Sleepwear","Shawls","Gaming Accessories","Computer Components","Bath","Mobile Phones","Men's Accessories","Table & Kitchen Linen","Kurtis","Table & Kitchen Linen","Computer Components","Kitchen Appliances","Laptops","DSLRs"]

            DownCats1=SecondCats[0:6]
            random.shuffle(SecondCats)
            DownCats2=SecondCats[0:6]

            product_snapdeal=Snapdeal.objects.filter(prod_url_title=str(myid))
            print('Total filtered products:'+str(len(product_snapdeal)))
            if len(product_snapdeal)>1:
                  print('inside if')
                  dates=[]
                  for i in product_snapdeal:
                        raw_date=str(i.prod_Date).replace("-","")
                        dates.append(int(str(raw_date)))
                  print(dates)
                  maxdate=max(dates)
                  pos=dates.index(maxdate)
                  print("Newest Product is at index:"+str(pos))
                  for m,j in enumerate(product_snapdeal):
                        if m!=int(pos):
                              j.delete()
                  product_snapdeal=product_snapdeal[pos]
            for x in product_snapdeal:
                  it=x
            
            current_date=int(str(datetime.datetime.now().date())[8:])
            existing_date=int(str(it.prod_Date)[8:])
            diff=int(current_date-existing_date)
            print(current_date)
            print(existing_date)
            print(diff)
           # if int(diff)>8:
          #        print(UpdateProductList(request,it.prod_URL))
       
            print("HERE---------->")
            ShopcluesProducts=[items.prod_name for items in Shopclue.objects.filter(prod_top_Category=it.prod_top_Category)]
            FlipkartProducts=[items.prod_name for items in Shopclues.objects.filter(prod_top_Category=it.prod_top_Category)]
            AmazonProducts=[items.prod_name for items in Amazon.objects.filter(prod_top_Category=it.prod_top_Category)]

            # print(it.prod_Date)
            try:
                  # print(it.prod_specs_right)
                  lwft=it.prod_specs_left.split(",")
                  it.prod_specs_left=list(lwft)
                  right=it.prod_specs_right.split(",")
                  it.prod_specs_right=list(right)
                  # print(it.prod_specs_right)
            except:
                  it.prod_specs_left=[]
                  it.prod_specs_right=[]

            FirstCat=it.prod_First_Category
            SecondCat=it.prod_Second_Category

            for key in it.prod_specs_left:
                  key=(key.replace("'","").replace("]","").replace("[",""))  
                  left_col.append(key)
            for value in it.prod_specs_right:
                  value=(value.replace("'","").replace("]","").replace("[",""))
                  right_col.append(value)
            Species=list(zip(left_col,right_col))
            # print(Species)  

            Item=it.prod_name              

            max_ratioflip=89
            try:
                  nearbyproductsflipkart=difflib.get_close_matches(Item,FlipkartProducts)
                  print('nearby products flipkart :')
                  print(nearbyproductsflipkart)
                  for prod in nearbyproductsflipkart:
                        ratio=fuzz.token_set_ratio(prod,it.prod_name)
                        if ratio>max_ratioflip:
                              if ratio>=95:
                                    max_ratioflip=ratio
                                    SameFlipkart=prod
                                    break
                              else:
                                    max_ratioflip=ratio
                                    SameFlipkart=prod
                  SameItemFlipkart=SameFlipkart
                  print(max_ratioflip)
                  print("Same item from Flipkart is :- "+ SameFlipkart)
                  SameProductFlipkar=[i for i in Shopclues.objects.filter(prod_name=SameItemFlipkart)]
                  SameProductFlipkart=[]
                  for i in SameProductFlipkar:
                        SameProductFlipkart.append(i)
                        break
                  print(SameProductFlipkart)
            except:
                  SameProductFlipkart=""
            
            max_ratioamz=89
            try:
                  nearbyproductsamazon=difflib.get_close_matches(Item,AmazonProducts)
                  print('nearby products amazon : ')
                  print(nearbyproductsamazon)
                  for pro in nearbyproductsamazon:
                        ratio=fuzz.token_set_ratio(pro,it.prod_name)
                        if ratio>max_ratioamz:
                              if ratio>=95:
                                    max_ratio=ratio
                                    SameAmazon=pro
                                    break
                              else:
                                    max_ratio=ratio
                                    SameAmazon=pro
                  SameItemAmazon=SameAmazon
                  print(max_ratio)
                  print("Same item from Amazon is :- "+ SameAmazon)
                  SameProductAmazo=[i for i in Amazon.objects.filter(prod_name=SameItemAmazon)]
                  SameProductAmazon=[]
                  for i in SameProductAmazo:
                        SameProductAmazon.append(i)
                        break
                  print(SameProductAmazon)
            except: 
                  SameProductAmazon=""           
            
            max_ratioshop=88
            nearbyproductsshopclues=difflib.get_close_matches(Item,ShopcluesProducts)
            print('nearby products shopclues : ')
            print(nearbyproductsshopclues)
            for proshop in nearbyproductsshopclues:
                  ratioshop=fuzz.token_set_ratio(proshop,it.prod_name)
                  if ratioshop>max_ratioshop:
                        if ratioshop>=95:
                              max_ratioshop=ratioshop
                              SameShop=proshop
                              break
                        else:
                              max_ratioshop=ratioshop
                              SameShop=proshop
            try:
                  SameItemShopclue=SameShop               
                  print(max_ratioshop)             
                  print("Same item from Shopclues is :- "+ SameShop)
                  SameProductShopclue=[i for i in Shopclue.objects.filter(prod_name=SameItemShopclue)]
                  SameProductShopclues=[]
                  for i in SameProductShopclue:
                        SameProductShopclues.append(i)
                        break
                  print(SameProductShopclues)
                  # SameProductShopclues=list(SameProductShopclues)
            except:
                  SameProductShopclues=""

            ProductDescription=it.prod_description
            ProductsHighlights=[]
            print(it.prod_highlights)
            for high in it.prod_highlights.split(","):
                  high=high.replace("'","").replace("]","").replace("[","")
                  ProductsHighlights.append(high)
            # print(ProductsHighlights)
            
            PastProducts.append(it)
            title=""
            name=[i for i in str(it.prod_name).split(" ")]
            if len(name)<10:
               title=str(it.prod_name)
            else:
             i=0
             while(i<10):
                title+=str(name[i])+" "
                i+=1
            CANONICAL_PATH=request.build_absolute_uri(request.path)
            if 'www.' in CANONICAL_PATH :
                CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
            contex={
                  "brand":"snapdeal",
                  "imagelogo":"/static/assets/images/snapdeal.jpg",
                  "page":"page",
              
                  "TopCat":it.prod_top_Category,
                  "FirstCat":it.prod_First_Category,
                  "SecondCat":it.prod_Second_Category,
                  "product":[product_snapdeal[0]],
                  "Species":Species,
                  "Descrip":it.prod_description,
                  "Highlights":it.prod_highlights,
                  "SameProductFlipkart":SameProductFlipkart,
                  "SameProductShopclues":SameProductShopclues,
                  "SameProductAmazon":SameProductAmazon,
                  "ProductDescription":ProductDescription,
                  "ProductHighlights":ProductsHighlights,
                  "TopRatedDown":TopRatedDown,
                  "FeaturedDown":FeaturedDown,
                  "OnSaleDown":OnSaleDown,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  "title":title,
                  'CANONICAL_PATH':CANONICAL_PATH,
                  'Snapdeal':'Snapdeal',
            }
            return render(request,"HTML Files/ProductpageFlipkart.html",context=contex)

def UpdateProductList(request,url):

      # database=url[12:14]
      if "amazon" in url:
            print("From Amazon")
            obj1=classtest.Index()
            return(obj1.StartAddingProductsAmazon(url))

      elif "shopclues" in url:
            obj1=classtest.Index()
            print(obj1.StartAddingProductsShopclues(url))
            return("From Shopclues")

      elif "snapdeal" in url:
            obj1=classtest.Index()
            print(obj1.StartAddingProductsSnapdeal(url))
            return("From Snapdeal")

      elif "flipkart" in url: 
            objfl=classtest.Index()
            print(objfl.StartAddingProductsFlipkart(url))   
            return("From Flipkart")
            
def ProductPageFlipkart(request,myid):

            if len(PastProducts)>36:
               del PastProducts[0]

            left_col=[]
            right_col=[]
            ProductsShopclues=[]
            ProductsSnapdeal=[]
            ProductsAmazon=[]
            x=[]
            
            l=random.randrange(0,len(Flipkart_products)-10)
            TopRatedDown=[i for i in Flipkart_products[l:l+3]]
            OnSaleDown=[i for i in Flipkart_products[l+3:l+6]]
            FeaturedDown=[x for x in Flipkart_products[l+6:l+9]]
            
            SecondCats=["Laptops","Tablets","Games","Women's Clothing","Kids' Clothing","Shaving & Beard Care","Bevarages","Video Accessories","Cookware","Utility Lighting","Men's Footwear","Hair Care and Accessory","PIRASO Sunglasses","Smart Watches","Headphones","Beauty Accessories","Televisions","Laptop Accessories","Speakers","Speakers"]
            DownCats1=SecondCats[0:6]
            random.shuffle(SecondCats)
            DownCats2=SecondCats[0:6]

            my=myid.replace("  ","-").replace("%C2%A0%C2%A0","-").replace("\xa0\xa0","-")
            for l in my.split(" "):
                  x.append(l)
            s=""
            for m in x:
                  if m!=x[-1]:
                        s+=m+"-"
                  else:
                        s+=m
            # print("S-------------------------"+s)
            product_flipkart=Shopclues.objects.filter(prod_url_title=str(myid))
            
            print('Total filtered products:'+str(len(product_flipkart)))
            if len(product_flipkart)>1:
                  print('inside if')
                  dates=[]
                  for i in product_flipkart:
                        raw_date=str(i.prod_Date).replace("-","")
                        dates.append(int(str(raw_date)))
                  print(dates)
                  maxdate=max(dates)
                  pos=dates.index(maxdate)
                  print("Newest Product is at index:"+str(pos))
                  for m,j in enumerate(product_flipkart):
                        if m!=int(pos):
                           j.delete()
                  product_flipkart=product_flipkart[pos]
            for x in product_flipkart:
                  item=x
            
            current_date=int(str(datetime.datetime.now().date())[8:])
            existing_date=int(str(item.prod_Date)[8:])
            diff=int(current_date-existing_date)
            print(current_date)
            print(existing_date)
            print(diff)
            #if diff>4:
            #     print(UpdateProductList(request,item.prod_URL))
            print('New date : ')
            print(item.prod_Date)



            item.prod_specs_left=list(item.prod_specs_left.split(",")) 
            item.prod_specs_right=list(item.prod_specs_right.split(","))
            
            FirstCat=item.prod_First_Category
            # print(FirstCat)

            SecondCat=item.prod_Second_Category

            for key in item.prod_specs_left:
                  key=(key.replace("'","").replace("[","").replace("]",""))
                  left_col.append(key)
            # print(item.prod_specs_right)
            for value in item.prod_specs_right:
                  value=(value.replace("'","").replace("[","").replace("]",""))
                  right_col.append(value)

            Species=list(zip(left_col,right_col))
            # print(Species)

            ShopcluesProducts=[item.prod_name for item in Shopclue.objects.filter(prod_top_Category=item.prod_top_Category)]
            SnapdealProducts=[iz.prod_name for iz in Snapdeal.objects.filter(prod_top_Category=item.prod_top_Category)]
            AmazonProducts=[items.prod_name for items in Amazon.objects.filter(prod_top_Category=item.prod_top_Category)]

            max_ratioshop=94
            ShopcluesProductsdifflib=difflib.get_close_matches(item.prod_name,ShopcluesProducts)
            for proshop in ShopcluesProductsdifflib:
                  ratioshop=fuzz.token_set_ratio(proshop,item.prod_name)
                  if ratioshop>max_ratioshop:
                        if ratioshop>=95:
                              max_ratioshop=ratioshop
                              SameShop=proshop
                              break
                        else:
                              max_ratioshop=ratioshop
                              SameShop=proshop

            try:
                  SameItemShopclue=SameShop               
                  print(max_ratioshop)             
                 # print("Same item from Shopclues is :- "+ SameShop)
                  SameProductShopclues=Shopclue.objects.filter(prod_name=SameItemShopclue)
            except:
                  SameProductShopclues=""            

            max_ratios=95
            SnapdealProductsdifflib=difflib.get_close_matches(item.prod_name,SnapdealProducts)
            print("length snapdeal "+str(len(SnapdealProductsdifflib)))
            try:
                        for prosnap in SnapdealProductsdifflib:
                              Ratio=fuzz.token_set_ratio(prosnap,item.prod_name)
                              if Ratio>=max_ratios:
                                    if Ratio>=95:
                                          max_ratios=Ratio
                                          SameSnap=prosnap
                                          break
                                    else:
                                          max_ratios=Ratio
                                          SameSnap=prosnap
                        SameItemSnapdeal=SameSnap
                        print(max_ratios)
               #         print("Same item from Snapdeal is :- "+ SameSnap)
                        SameProductSnapdea=[i for i in Snapdeal.objects.filter(prod_name=SameItemSnapdeal)]
                        SameProductSnapdeal=[]
                        for i in SameProductSnapdea:
                              SameProductSnapdeal.append(i)
                              break
                        print(SameProductSnapdeal)
            except:
                  SameProductSnapdeal=""

            max_ratio=90
            AmazonProductsdifflib=difflib.get_close_matches(item.prod_name,AmazonProducts,2)
            print("length amazon difflib "+str(len(AmazonProductsdifflib)))
            try:
                  print(AmazonProductsdifflib)
                  for pro in AmazonProductsdifflib:
                        ratio=fuzz.token_set_ratio(pro,item.prod_name)
                        print(ratio)
                        if ratio>=max_ratio:
                              if ratio>=96:
                                    max_ratio=ratio
                                    SameAmazon=pro
                                    break
                              else:
                                    max_ratio=ratio
                                    SameAmazon=pro
                  SameItemAmazon=SameAmazon
                  print(max_ratio)
                #  print("Same item from Amazon is :- "+ SameAmazon)
                  SameProductAmazo=[g for g in Amazon.objects.filter(prod_name=SameItemAmazon)]
                  SameProductAmazon=[]
                  for j in SameProductAmazo:
                        SameProductAmazon.append(j)
                        break
            except:
                  SameProductAmazon=""
  
            PastProducts.append(item)
            title=""
            name=[i for i in str(item.prod_name).split(" ")]
            if len(name)<10:
              title=str(item.prod_name)
            else:
              i=0
              while(i<10):
                title+=str(name[i])+" "
                i+=1
            CANONICAL_PATH=request.build_absolute_uri(request.path)
            if 'www.' in CANONICAL_PATH :
                CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
            contex={
                  "brand":"flipkart",
                  "imagelogo":"/static/assets/images/flipkart.jpg",
                  "page":"IdPage",
                 
                  "TopCat":item.prod_top_Category,
                  "FirstCat":item.prod_First_Category,
                  "SecondCat":item.prod_Second_Category,
                  "product":[product_flipkart[0]],
                  "FirstCategory":FirstCat,
                  "SecondCategory":SecondCat,
                  "Species":Species,
                  "SameProductShopclues":SameProductShopclues,
                  "SameProductSnapdeal":SameProductSnapdeal,
                  "SameProductAmazon":SameProductAmazon,
                  "SameProductFlipkart":"",
                  "TopRatedDown":TopRatedDown,
                  "FeaturedDown":FeaturedDown,
                  "OnSaleDown":OnSaleDown,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  "title":title,
                  'CANONICAL_PATH':CANONICAL_PATH,
                  'Flipkart':'Flipkart'
           }
            return render(request,"HTML Files/ProductpageFlipkart.html",context=contex)

def ProductPageAmazon(request,myid):

      if len(PastProducts)>36:
          del PastProducts[0]

      left_col=[]
      right_col=[]
      ProductsShopclues=[]
      ProductsSnapdeal=[]
      ProductsFlipkart=[]

      product_amazon=Amazon.objects.filter(prod_url_title=str(myid))
      
      print('Total filtered products:'+str(len(product_amazon)))
      if len(product_amazon)>1:
                  print('inside if')
                  dates=[]
                  for i in product_amazon:
                        raw_date=str(i.prod_Date).replace("-","")
                        dates.append(int(str(raw_date)))
                  print(dates)
                  maxdate=max(dates)
                  pos=dates.index(maxdate)
                  print("Newest Product is at index:"+str(pos))
                  for m,j in enumerate(product_amazon):
                        if m!=int(pos):
                              j.delete()
                  product_amazon=product_amazon[pos]

      for x in product_amazon:
                  item=x

      print(item.prod_Date)
      current_date=int(str(datetime.datetime.now().date())[8:10])
      existing_date=int(str(item.prod_Date)[8:10])
      diff=int(current_date-existing_date)
      print(current_date)
      print(existing_date)
      print(diff)
      #if diff>2:
      #print(UpdateProductList(request,item.prod_URL))

      g=random.randrange(0,len(Amazon_products)-10)
      TopRatedDown=[i for i in Amazon_products[g:g+3]]
      OnSaleDown=[i for i in  Amazon_products[g+3:g+6]]
      FeaturedDown=[i for i in Amazon_products[g+6:g+9]]
      
      SecondCats=['Plants', 'Seeds & Bulbs',"Home Theater, TV & Video","Biographies, Diaries & True Accounts","Sports Gadgets",'Networking Devices','Printers, Inks & Accessories',"Children's & Young Adult","Handbags","Exercise & Fitness","Computers & Accessories","Wearable Technology","Fragrance","Sexual Wellness & Sensuality","Travel Accessories"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]
      # Function For NavBar-------------------------------------------------------------------------------->

      def toadd(top_cat):
            
                  all_cats=[]
                  all_sub_cats=[]
                  All_Prods_Sub_Cats=[]
                  all_cats_sub_cats=[]
                  for product in top_cat:
                        all_cats.append(product.prod_First_Category)
                  all_cats=set(all_cats)
                  all_cats=list(all_cats)
                  
                  for category in all_cats:
                        products=Amazon.objects.filter(prod_First_Category=category)
                        all_sub_cats={(product.prod_Second_Category) for product in products}
                        all_sub_cats=list(all_sub_cats)
                        All_Prods_Sub_Cats.append(all_sub_cats)
                  all_cats_sub_cats=list(zip(all_cats,All_Prods_Sub_Cats))
                  top_cat_section=(all_cats_sub_cats)
                  return top_cat_section

      Electronics=[p for p in Amazon.objects.filter(prod_top_Category="Electronics")]
      elec_section=toadd(Electronics)
      MenWomen=[p for p in Amazon.objects.filter(prod_top_Category="Men & Women")]
      men_sec=toadd(MenWomen)
      Books=[p for p in Amazon.objects.filter(prod_top_Category="Books")]
      book_sec=toadd(Books)
      print(book_sec)
      Others=[p for p in Amazon.objects.filter(prod_top_Category="Others")]
      other_sec=toadd(Others)
      Home=[p for p in Amazon.objects.filter(prod_top_Category="Home")]
      home_sec=toadd(Home)
      # Baby=[p for p in Shopclues.objects.filter(prod_top_Category="Baby")]
      # Gym=[]
      Nonea=[p for p in Amazon.objects.filter(prod_top_Category="None")]
      none_sec=toadd(Nonea)
      
      Item=item.prod_name
      Availiblity=item.prod_availi

      try:
            item.prod_specs_left=list(item.prod_specs_left.split(",")) 
            item.prod_specs_right=list(item.prod_specs_right.split(","))

            for key in item.prod_specs_left:
                  key=(key.replace("'","").replace("[","").replace("]","")) 
                  left_col.append(key)
                  
            for value in item.prod_specs_right:
                  value=(value.replace("'","").replace("[","").replace("]","")) 
                  right_col.append(value)   

            Species=list(zip(left_col,right_col))

      except:
            Species=[]
      
      ShopcluesProducts=[item.prod_name for item in Shopclue.objects.filter(prod_top_Category=item.prod_top_Category)]
      SnapdealProducts=[item.prod_name for item in Snapdeal.objects.filter(prod_top_Category=item.prod_top_Category)]
      FlipkartProducts=[items.prod_name for items in Shopclues.objects.filter(prod_top_Category=item.prod_top_Category)]

      max_ratioshop=85
      ShopcluesProductsdifflib=difflib.get_close_matches(item.prod_name,ShopcluesProducts)
      print("length difflib shopclues "+str(len(ShopcluesProductsdifflib)))
      try:
                  for proshop in ShopcluesProductsdifflib:
                        ratioshop=fuzz.token_set_ratio(proshop,item.prod_name)
                        if ratioshop>max_ratioshop:
                              if ratioshop>=95:
                                    max_ratioshop=ratioshop
                                    SameShop=proshop
                                    break
                              else:
                                    max_ratioshop=ratioshop
                                    SameShop=proshop
                  SameItemShopclue=SameShop               
                  print(max_ratioshop)        
                  print("Same item from Shopclues is :- "+ SameShop)
                  SameProductShopclue=[i for i in Shopclue.objects.filter(prod_name=SameItemShopclue)]
                  SameProductShopclues=[]
                  for i in SameProductShopclue:
                              SameProductShopclues.append(i)
                              break
                  print(SameProductShopclues)
      except:
            SameProductShopclues=""

      max_ratios=85
      SnapdealProductsdifflib=difflib.get_close_matches(item.prod_name,SnapdealProducts)
      print("length difflib snapdeal "+str(len(SnapdealProductsdifflib)))
      try:
                  for prosnap in SnapdealProductsdifflib:
                              Ratio=fuzz.token_set_ratio(prosnap,item.prod_name)
                              if Ratio>=max_ratios:
                                    if Ratio>=95:
                                          max_ratios=Ratio
                                          SameSnap=prosnap
                                          break
                                    else:
                                          max_ratios=Ratio
                                          SameSnap=prosnap
                  SameItemSnapdeal=SameSnap
                  print(max_ratios)
                  print("Same item from Snapdeal is :- "+ SameSnap)
                  SameProductSnapdea=[i for i in Snapdeal.objects.filter(prod_name=SameItemSnapdeal)]
                  SameProductSnapdeal=[]
                  for i in SameProductSnapdea:
                              SameProductSnapdeal.append(i)
                              break
                  print(SameProductSnapdeal)
      except:
            SameProductSnapdeal=""

      max_ratio=85
      FlipkartProductsdifflib=difflib.get_close_matches(item.prod_name,FlipkartProducts)
      print("length difflib flipkart "+str(len(FlipkartProductsdifflib)))
      try:
                  for pro in FlipkartProductsdifflib:
                        print(pro)
                        ratio=fuzz.token_set_ratio(pro,item.prod_name)
                        print(ratio)
                        if ratio>max_ratio:
                              if ratio>=96:
                                    max_ratio=ratio
                                    SameFlipkart=pro
                                    break
                              else:
                                    max_ratio=ratio
                                    SameFlipkart=pro
                  SameItemFlipkart=SameFlipkart
                  print(max_ratio)
                  print("Same item from Flipkart is :- "+ SameFlipkart)
                  SameProductFlipkar=[i for i in Shopclues.objects.filter(prod_name=SameItemFlipkart)]
                  SameProductFlipkart=[]
                  for i in SameProductFlipkar:
                              SameProductFlipkart.append(i)
                              break
                  print(SameProductFlipkart)
      except:
            SameProductFlipkart=""

      Specs=(item.prod_specifications)
      Features=[]
      for em in Specs.split(","):
            em=em.replace("[","").replace("]","").replace("]","")
            Features.append(em)
      Descrip=(item.prod_description.replace("[","").replace("]","").replace("'",""))

      Ratings=[]
      Ratings.append(int(item.prod_ratings_1start.replace("%","")))
      Ratings.append(int(item.prod_ratings_2start.replace("%","")))
      Ratings.append(int(item.prod_ratings_3start.replace("%","")))
      Ratings.append(int(item.prod_ratings_4start.replace("%","")))
      Ratings.append(int(item.prod_ratings_5start.replace("%","")))
      print(Ratings)
  
      PastProducts.append(item)
      title=""
      name=[i for i in str(item.prod_name).split(" ")]
      if len(name)<10:
         title=str(item.prod_name)
      else:
        i=0
        while(i<10):
         title+=str(name[i])+" "
         i+=1
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
      if Availiblity=="In stock." or Availiblity=="In stock":
            Limited_Stock=""
            print("hello")
            contex={
                  "brand":"amazon",
                  "imagelogo":"/static/assets/images/amazon.jpg",
                  "page":"p_no",
                  "Electronics":elec_section,
                  "MenWomen":men_sec,
                  "Others":other_sec,
                  "Home":home_sec,
                  "Books":book_sec,
                  "TopCat":item.prod_top_Category,
                  "FirstCat":item.prod_First_Category,
                  "SecondCat":item.prod_Second_Category,
                  "Ratings":Ratings,
                  "Specs":Specs,
                  "Descrip":Descrip, 
                  "Availability":Availiblity,
                  "LimitedStock":Limited_Stock,
                  "product":[product_amazon[0]],
                  "Species":Species,
                  "SameProductShopclues":SameProductShopclues,
                  "SameProductSnapdeal":SameProductSnapdeal,
                  "SameProductFlipkart":SameProductFlipkart,
                  "TopRatedDown":TopRatedDown,
                  "FeaturedDown":FeaturedDown,
                  "OnSaleDown":OnSaleDown,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  "title":title,
                  'CANONICAL_PATH':CANONICAL_PATH
                  }
            return render(request,"HTML Files/ProductpageFlipkart.html",context=contex)

      elif Availiblity!="In stock." or Availiblity!="In stock":
            Limited_Stock=Availiblity
            Availiblity=""
            print("hi")
            print(Availiblity)
            contexr={
                  "brand":"amazon",
                  "page":"p_no",
                  "Electronics":elec_section,
                  "MenWomen":men_sec,
                  "Others":other_sec,
                  "Home":home_sec,
                  "Books":book_sec,
                  "TopCat":item.prod_top_Category,
                  "FirstCat":item.prod_First_Category,
                  "SecondCat":item.prod_Second_Category,  
                  "Specs":Specs,
                  "Descrip":Descrip,
                  "Availability":Availiblity,
                  "LimitedStock":Limited_Stock,
                  "product":[product_amazon[0]],
                  "Species":Species,
                  "SameProductShopclues":SameProductShopclues,
                  "SameProductSnapdeal":SameProductSnapdeal,
                  "SameProductFlipkart":SameProductFlipkart,
                  "TopRatedDown":TopRatedDown,
                  "FeaturedDown":FeaturedDown,
                  "OnSaleDown":OnSaleDown,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  "title":title,
                  'CANONICAL_PATH':CANONICAL_PATH
            }
            return render(request,"HTML Files/ProductpageFlipkart.html",context=contexr)

def FilterByCatSnapdeal(request,SubCat,page_no):
    
      Snapdeal_products=Snapdeal.objects.filter(prod_Second_Category=SubCat)[::-1] 
      # print(Flipkart_products)
      first_cat=[]
      top_cat=[]
      for m in Snapdeal_products:
            first_cat.append(m.prod_First_Category)
            top_cat.append(m.prod_top_Category)
            first_cat.append(m.prod_First_Category)
            break
      
      SecondCats=["Gaming Accessories","Lingerie & Sleepwear","Bath","Mobile Phones","Men's Accessories","Table & Kitchen Linen","Kurtis","Bottom Wear","Computer Components","Kitchen Appliances","Winter Wear"]

      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]
      
      print(top_cat)
      department=[a.prod_Second_Category for a in Snapdeal.objects.filter(prod_First_Category=first_cat[0])]
      department=set(department)
      department=list(department)
      print(department)
      All=len(Snapdeal_products)
      PageProducts=[]
      PageItems=[]
      print(len(Snapdeal_products))
      Recommended=Snapdeal.objects.filter(prod_top_Category=top_cat[0])
      x=random.randint(0,len(list(Recommended))-12)
      Featured=list(Recommended[x:x+3])
      x=random.randint(0,len(list(Recommended))-12)
      OnSale=list(Recommended[x:x+3])
      # x=random.randint(0,len(list(Recommended))-12)
      TopRated=list(Recommended[x+4:x+7])
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
      if len(Snapdeal_products)<=30:
            print("less than 30")
            for product in Snapdeal_products:
                  if product.prod_mrp=="Not available":
                        product.prod_mrp=""
                  if product.prod_price=="Not available":
                        product.prod_price=""      
                  PageItems.append(product)
            PageProducts.append(list(PageItems))   
            print(len(PageProducts[page_no-1]))
           # print(PageProducts[page_no-1])
            del PageItems[:]
            L=list(range(1,len(PageProducts)+1))
            contex={
                  "brand":"snapdeal",
                  "page":"page",
                  "Department":department,
                  "AllProducts":PageProducts[page_no-1],
                  "Length":L,
                  "next":page_no,
                  "SubCat":SubCat,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[x:x+10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH     
                  }
            return render(request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)
      else:
            print("more than 30")
            for i in range(All):
                  for j in range(i,i+31):
                        if j%30==0 and j<=All:
                              if All-j<30:
                                    LastNum=j
                              else:
                                    continue      
                        else: 
                              continue
            print(LastNum)
            k=0
            for product in Snapdeal_products:
                  if product.prod_mrp=="Not available":
                        product.prod_mrp=""
                  if product.prod_price=="Not available":
                        product.prod_price=""
                  PageItems.append(product)
                  if len(PageItems)<30:
                        if k>LastNum:
                              for item in Snapdeal_products[k:]:
                                    PageItems.append(item)
                              PageProducts.append(list(PageItems))
                              break
                  elif len(PageItems)==30:
                        PageProducts.append(list(PageItems))
                        del PageItems[:]
                  else:
                        continue
                  k=k+1
            print(len(PageProducts))
            #print(PageProducts[page_no-1])

            if len(PageProducts)>5:
                        if page_no==1:
                              L=list(range(page_no,page_no+5))
                        else:
                              if page_no+5<len(PageProducts):
                                    L=list(range(page_no-1,page_no+5))
                              else:
                                    L=list(range(page_no-1,len(PageProducts)+1))
            else:
                        L=list(range(1,len(PageProducts)+1))
            print(len(PageProducts))
            # print(PageProducts[page_no-1])
            contex={
                  "brand":"snapdeal",
                  "page":"page",
                  "AllProducts":PageProducts[page_no-1],
                  "Length":L,
                  "next":page_no+1,
                  "SubCat":SubCat,
                  "Department":department,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[x:x+10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH
                  }
            return render (request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)

def FilterByCatShopclues(request,SubCat,page_id):

      Shopclues_products=Shopclue.objects.filter(prod_Second_Category=SubCat)[::-1]
      # print(Flipkart_products)
      first_cat=[]
      top_cat=[]
      for m in Shopclues_products:
            first_cat.append(m.prod_First_Category)
            top_cat.append(m.prod_top_Category)
            first_cat.append(m.prod_First_Category)
            break
      
      SecondCats=["TVs & DTH","Laptops","Gaming","Furnitue","Men's Footwear","Women's Clothing","Watches","Travel Accessories","Bathroom & Sanitaryware","Decor","Men's Clothing","DSLR Lenses","Camcorder","Refurbished Mobiles","Unboxed Cameras & Accessories","Large Home Appliances","Desktops & Monitors","Kitchen and Dining","Office Electronics","Large Home Appliances","Smartphones","Bike Accessories"]

      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

      print(top_cat)
      department=[a.prod_Second_Category for a in Shopclue.objects.filter(prod_First_Category=first_cat[0])]
      department=set(department)
      department=list(department)
      print(department)
      All=len(Shopclues_products)
      PageProducts=[]
      PageItems=[]
      print(len(Shopclues_products))
      Recommended=Shopclue.objects.filter(prod_top_Category=top_cat[0])
      x=random.randint(0,len(list(Recommended))-12)
      Featured=list(Recommended[x:x+3])
      x=random.randint(0,len(list(Recommended))-12)
      OnSale=list(Recommended[x:x+3])
      # x=random.randint(0,len(list(Recommended))-12)
      TopRated=list(Recommended[x+4:x+7])
   
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

      if len(Shopclues_products)<=30:
            print("less than 30")
            for product in Shopclues_products:
                  if product.prod_mrp=="Not available":
                        product.prod_mrp=""
                  if product.prod_price=="Not available":
                        product.prod_price=""      
                  PageItems.append(product)
            PageProducts.append(list(PageItems))   
            print(len(PageProducts[page_id-1]))
            print(PageProducts[page_id-1])
            del PageItems[:]
            L=list(range(1,len(PageProducts)+1))
            contex={
                  "brand":"shopclues",
                  "page":"ID_page",
                  "Department":department,
                  "AllProducts":PageProducts[page_id-1],
                  "Length":L,
                  "next":page_id,
                  "SubCat":SubCat,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[x:x+10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH
                  }
            return render(request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)

      else:
            print("more than 30")
            for i in range(All):
                  for j in range(i,i+31):
                        if j%30==0 and j<All:
                              if All-j<=30:
                                    LastNum=j
                              else:
                                    continue      
                        else: 
                              continue
            print(LastNum)
            k=0
            for product in Shopclues_products:
                  if product.prod_mrp=="Not available":
                        product.prod_mrp=""
                  if product.prod_price=="Not available":
                        product.prod_price=""
                  PageItems.append(product)
                  if len(PageItems)<30:
                        if k>LastNum:
                              for item in Shopclues_products[k:]:
                                    PageItems.append(item)
                              PageProducts.append(list(PageItems))
                              break
                  elif len(PageItems)==30:
                        PageProducts.append(list(PageItems))
                        del PageItems[:]
                  else:
                        continue
                  k=k+1
            print(len(PageProducts))
            print(PageProducts[page_id-1])

            if len(PageProducts)>5:
                        if page_id==1:
                              L=list(range(page_id,page_id+5))
                        else:
                              if page_id+5<len(PageProducts):
                                    L=list(range(page_id-1,page_id+5))
                              else:
                                    L=list(range(page_id-1,len(PageProducts)+1))
            else:
                        L=list(range(1,len(PageProducts)+1))
            print(len(PageProducts))
            # print(PageProducts[page_no-1])
            contex={
                  "brand":"shopclues",
                  "page":"ID_page",
                  "AllProducts":PageProducts[page_id-1],
                  "Length":L,
                  "next":page_id+1,
                  "SubCat":SubCat,
                  "Department":department,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[x:x+10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH
                  }
            return render (request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)

def FilterByCatFlipkart(request,SubCat,page_no):

      # print(SubCat)
      Flipkart_products=Shopclues.objects.filter(prod_Second_Category=SubCat)[::-1]
     # print(Flipkart_products)
      first_cat=[]
      top_cat=[]
      for m in Flipkart_products:
            first_cat.append(m.prod_First_Category)
            top_cat.append(m.prod_top_Category)
            first_cat.append(m.prod_First_Category)
            break
      
      SecondCats=["Speakers","Headphones","Puzzles & Board Games","Laptops","Gaming Components","Cameras","Women's Clothing","Women's Footwear","Bath & Shower","Shaving & Beard Care","Fastrack Sunglasses","Health & Nutrition","Video Accessories","Azmani Sunglasses","Strollers & Activity Gear","Men's Footwear","Bathroom Accessories","PIRASO Sunglasses","Smart Watches","Headphones","Beauty Accessories","Televisions"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[1:7]

      print(top_cat)
      department=[a.prod_Second_Category for a in Shopclues.objects.filter(prod_First_Category=first_cat[0])]
      department=set(department)
      department=list(department)
      print(department)
      All=len(Flipkart_products)
      PageProducts=[]
      PageItems=[]
      print(len(Flipkart_products))
      Recommended=Shopclues.objects.filter(prod_top_Category=top_cat[0])
      x=random.randint(0,len(list(Recommended))-12)
      Featured=list(Recommended[x:x+3])
      x=random.randint(0,len(list(Recommended))-12)
      OnSale=list(Recommended[x:x+3])
      # x=random.randint(0,len(list(Recommended))-12)
      TopRated=list(Recommended[x+4:x+7])
     
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

      if len(Flipkart_products)<=30:
            print("less than 30")
            for product in Flipkart_products:
                  if product.prod_mrp=="Not available":
                        product.prod_mrp=""
                  if product.prod_price=="Not available":
                        product.prod_price=""      
                  PageItems.append(product)
            PageProducts.append(list(PageItems))   
            print(len(PageProducts[page_no-1]))
            L=list(range(1,len(PageProducts)+1))
            del PageItems[:]
            # random.shuffle(PageProducts)
            contex={
                  "brand":"flipkart",
                  "page":"IdPage",
                  "Department":department,
                  "AllProducts":PageProducts[page_no-1],
                  "Length":L,
                  "next":page_no,
                  "SubCat":SubCat,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[x:x+10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH
                  }
            # print(list(Length[page_no:page_no+5]))
            return render(request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)
      else:
            print("more than 30")
            for i in range(All):
                  for j in range(i,i+31):
                        if j%30==0 and j<=All:
                              if All-j<30:
                                    LastNum=j
                              else:
                                    continue      
                        else: 
                              continue
            print(LastNum)
            k=0
            for product in Flipkart_products:
                  if product.prod_mrp=="Not available":
                        product.prod_mrp=""
                  if product.prod_price=="Not available":
                        product.prod_price=""
                  PageItems.append(product)
                  if len(PageItems)<30:
                        if k>LastNum:
                              for item in Flipkart_products[k:]:
                                    PageItems.append(item)
                              PageProducts.append(list(PageItems))
                              break
                  elif len(PageItems)==30:
                        PageProducts.append(list(PageItems))
                        del PageItems[:]
                  else:
                        continue
                  k=k+1
            if len(PageProducts)>5:
                        if page_no==1:
                              L=list(range(page_no,page_no+5))
                        else:
                              if page_no+5<len(PageProducts):
                                    L=list(range(page_no-1,page_no+5))
                              else:
                                    L=list(range(page_no-1,len(PageProducts)+1))
            else:
                        L=list(range(1,len(PageProducts)+1))
            print(len(PageProducts))
            # print(PageProducts[page_no-1])
            # random.shuffle(PageProducts)
            contex={
                  "brand":"flipkart",
                  "page":"IdPage",
                  "AllProducts":PageProducts[page_no-1],
                  "Length":L,
                  "next":page_no+1,
                  "SubCat":SubCat,
                  "Department":department,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[x:x+10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH
                  }
            print(list(range(page_no,page_no+5)))
            return render (request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)

def FilterByCatAmazon(request,SubCat,p_no):

      Amazon_products=Amazon.objects.filter(prod_Second_Category=SubCat)[::-1]
      All=len(Amazon_products)
   #   print(Amazon_products)

      first_cat=[]
      top_cat=[]

      SecondCats=['Plants, Seeds & Bulbs',"Home Theater, TV & Video","Biographies, Diaries & True Accounts","Sports Gadgets",'Networking Devices','Printers, Inks & Accessories',"Children's & Young Adult","Handbags","Exercise & Fitness","Computers & Accessories","Wearable Technology","Fragrance","Sexual Wellness & Sensuality","Travel Accessories"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

      for m in Amazon_products:
            first_cat.append(m.prod_First_Category)
            top_cat.append(m.prod_top_Category)
            first_cat.append(m.prod_First_Category)
            break
      print(first_cat)
      department=[a.prod_Second_Category for a in Amazon.objects.filter(prod_First_Category=first_cat[0])]
      department=set(department)
      department=list(department)
      print(department)

      All=len(Amazon_products)
      PageProducts=[]
      PageItems=[]
      print(len(Amazon_products))
      # Length=range(1,len(PageProducts)+1)
      Recommended=Amazon.objects.filter(prod_top_Category="Electronics")
      x=random.randint(0,len(list(Recommended))-12)
      Featured=list(Recommended[x:x+3])
      x=random.randint(0,len(list(Recommended))-12)
      OnSale=list(Recommended[x:x+3])
      # x=random.randint(0,len(list(Recommended))-12)
      TopRated=list(Recommended[x+4:x+7])

      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

      i=0
      if len(Amazon_products)<=30:
            for product in Amazon_products:
                  PageItems.append(product)
            PageProducts.append(list(PageItems))   
            #print(PageProducts[0])
            del PageItems[:]
            L=list(range(1,2))
            # random.shuffle(PageProducts)
            contex={
                  "brand":"amazon",
                  "page":"p_no",
                  "Department":department,
                  "AllProducts":PageProducts[p_no-1],
                  "Length":L,
                  "next":p_no,
                  "SubCat":SubCat,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[0:10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH
            }
            return render(request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)

      else:
            # id_num=id_num+1
            for i in range(All):
                  for j in range(i,i+31):
                        if j%30==0 and j<All:
                              if All-j<=30:
                                    LastNum=j
                              else:
                                    continue      
                        else: 
                              continue
            print(LastNum)
            k=0
            for product in Amazon_products:
                  PageItems.append(product)
                  if len(PageItems)<30:
                        if k>LastNum:
                              for item in Amazon_products[k:]:
                                    PageItems.append(item)
                              PageProducts.append(list(PageItems))
                              break
                  elif len(PageItems)==30:
                        PageProducts.append(list(PageItems))
                        del PageItems[:]
                  else:
                        continue
                  k=k+1
                  if len(PageProducts)>5:
                        if p_no==1:
                              L=list(range(p_no,p_no+5))
                        else:
                              if p_no+4<=len(PageProducts):
                                    L=list(range(p_no-1,p_no+4))
                              else:
                                    if p_no+4<=len(PageProducts):
                                          L=list(range(p_no-1,p_no+4))
                                    else:
                                          L=list(range(p_no-1,len(PageProducts)+2))
                  else:
                        L=list(range(1,len(PageProducts)+2))
            # print((PageProducts[0]))            
            # random.shuffle(PageProducts)
            # print((PageProducts[0]))
            contex={
                  "brand":"amazon",
                  "page":"p_no",
                  "AllProducts":PageProducts[p_no-1],
                  "Length":L,
                  "next":p_no+1,
                  "SubCat":SubCat,
                  "Department":department,
                  "FirstCat":first_cat[0],
                  "TopCat":top_cat[0],
                  "Recommended":list(Recommended[0:10]),
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCats1":DownCats1,
                  "DownCats2":DownCats2,
                  'CANONICAL_PATH':CANONICAL_PATH
            }
            return render(request,"HTML Files/FilteredSecondcatFlipkart.html",context=contex)

def searchfuzz(request,page_no):

      ProductListFlipkart=[]
      ProductListAmazon=[]
      ProductListShopclues=[]
      ProductListSnapdeal=[]
      str1=request.GET.get("search","default")
      print(str1)
      test=str1
      AllProducts=[]
      prod_vector=SearchVector('prod_name')
      Category=''
      query = SearchQuery(test)
      filtere_flip=Shopclues.objects.filter(Q(prod_name__icontains=test)).annotate()         
      if len(filtere_flip)<6:
         filtere_flip= Shopclues.objects.filter(prod_name__icontains=test)
      if len(filtere_flip)<9:
          print("HERE NONE")
          product_names=[i.prod_name.lower() for i in Shopclues.objects.all()]
          for p in product_names:
           ratio=fuzz.token_set_ratio(test.lower(),p)
           if ratio>=26:
              prdct=Shopclues.objects.filter(prod_name=p)
              for r in prdct:
                 Category+=str(r.prod_Top_Category)
                 print(r)
                 AllProducts.append(r)
      print("------------------->"+str(len(AllProducts)))
         
      filtere_amazon=Amazon.objects.filter(Q(prod_name__icontains=test)).annotate()
      if filtere_amazon is None:
         filtere_amazon= Amazon.objects.filter(prod_name__icontains=test)

      filtere_snap=Snapdeal.objects.filter(Q(prod_name__icontains=test)).annotate()
      if filtere_snap is None:
         filtere_snap= Snapdeal.objects.filter(prod_name__icontains=test)
      if filtere_snap is None:
          filtere_snap=[]
          product_names=[i.prod_name for i in Snapdeal.objects.filter(prod_Top_category=Category)]
          for p in product_names:
           ratio=fuzz.token_set_ratio(test.lower(),p.lower())
           if ratio>=25:
              prdct=Snapdeal.objects.filter(prod_name=p)
              for r in prdct:
                filtere_snap.append(r)
     
      filtere_shop=Shopclue.objects.filter(Q(prod_name__icontains=test)).annotate()
      if filtere_shop is None:
         filtere_shop= Shopclue.objects.filter(prod_name__icontains=test)
      if filtere_shop is None:
         filtere_shop=[]
         product_names=[i.prod_name for i in Shopclue.objects.filter(prod_Top_category=Category)]
         for p in product_names:
           ratio=fuzz.token_set_ratio(test.lower(),p.lower())
           if ratio>=25:
              prdct=Shopclue.objects.filter(prod_name=p)
              for r in prdct:
                filtere_shop.append(r)
     
      for p in filtere_flip:
            AllProducts.append(p)
      for p in ProductListAmazon:
            AllProducts.append(p)
      for p in filtere_shop:
            AllProducts.append(p)
      for p in filtere_snap:
            AllProducts.append(p)

      #<--------------------------------------Department Categories--------------------------------------------------->     
      
      FlipSubCats=["Puzzles & Board Games","Video Accessories","Azmani Sunglasses","Strollers & Activity Gear","Men's Footwear","Bathroom Accessories","PIRASO Sunglasses","Smart Watches","Headphones","Beauty Accessories","Televisions"]
      AmazonSubCats=['Plants, Seeds & Bulbs',"Home Theater, TV & Video","Biographies, Diaries & True Accounts","Sports Gadgets",'Networking Devices','Printers, Inks & Accessories',"Children's & Young Adult","Handbags","Exercise & Fitness","Computers & Accessories","Wearable Technology","Fragrance","Sexual Wellness & Sensuality","Travel Accessories"]
      ShopcluesSubCats=["Men's Clothing","DSLR Lenses","Camcorder","Refurbished Mobiles","Unboxed Cameras & Accessories","Large Home Appliances","Desktops & Monitors","Kitchen and Dining","Office Electronics","Large Home Appliances","Smartphones","Bike Accessories"]
      SnapdealSubCats=["Gaming Accessories","Lingerie & Sleepwear","Bath","Mobile Phones","Men's Accessories","Table & Kitchen Linen","Kurtis","Bottom Wear","Computer Components","Kitchen Appliances","Winter Wear"]

      random.shuffle(FlipSubCats)
      random.shuffle(AmazonSubCats)
      random.shuffle(ShopcluesSubCats)
      random.shuffle(SnapdealSubCats)
      
      #<--------------------------------------Recommended Products----------------------------------------------------->
      try:
            Recommended=[]
            s=0
            for j in (Shopclues.objects.filter(prod_Second_Category=random.choice(FlipSubCats))):
                  Recommended.append(j)
                  s+=1
                  if s==2:
                        s=0
                        break
            for k in (Amazon.objects.filter(prod_Second_Category=random.choice(AmazonSubCats))):
                  Recommended.append(k)
                  s+=1
                  if s==2:
                        s=0
                        break
            for l in (Snapdeal.objects.filter(prod_Second_Category=random.choice(SnapdealSubCats))):
                  Recommended.append(l)
                  s+=1
                  if s==2:
                        s=0
                        break
            for m in (Shopclue.objects.filter(prod_Second_Category=random.choice(ShopcluesSubCats))):
                  Recommended.append(m)
                  s+=1
                  if s==2:
                        s=0
                        break
      except:
            i=random.randrange(0,len(AllProducts)-10)
            Recommended=AllProducts[i:i+10]
      # else:
      #       Recommended=[]
      
      # <--------------------------------Featured / Onsale / Top-Rated Products----------------------------->

      f=random.randrange(0,len(AllProducts)-4)
      Featured=AllProducts[f:f+4]
      g=random.randrange(0,len(AllProducts)-4)
      OnSale=AllProducts[g:g+4]
      h=random.randrange(0,len(AllProducts)-4)
      TopRated=AllProducts[h:h+4]

      # <---------------------------------Down Cats1 / Down Cats2--------------------------------------------->

      r=random.randrange(0,8)
      # r=4
      DownCatsAmzn=AmazonSubCats[r:r+3]
      DownCatsFlip=FlipSubCats[r:r+3]
      DownCatsShop=ShopcluesSubCats[r:r+3]
      DownCatsSnap=SnapdealSubCats[r:r+3]
      
      PageItems=[]
      PageProducts=[]

      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

      if len(AllProducts)<=30:
            print("less than 30")
            for product in AllProducts:
                  PageItems.append(product)
            PageProducts.append(list(PageItems))   
            # print(len(PageProducts[page_no-1]))
            L=list(range(1,len(PageProducts)+1))
            del PageItems[:]

            contex={
                  "ProductsFlipkart":ProductListFlipkart,
                  "ProductsAmazon":ProductListAmazon,
                  "ProductsShopclues":ProductListShopclues,
                  "ProductsSnapdeal":ProductListSnapdeal,
                  "AllProducts":PageProducts[page_no-1],
                  "Length":L,
                  "next":page_no,
                  "FlipSubCats":FlipSubCats[0:3],
                  "AmazonSubCats":AmazonSubCats[0:3],
                  "ShopcluesSubCats":ShopcluesSubCats[0:3],
                  "SnapdealSubCats":SnapdealSubCats[0:3],
                  "Recommended":Recommended,
                  "search":str1,
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCatsAmzn":DownCatsAmzn,
                  "DownCatsFlip":DownCatsFlip,
                  "DownCatsShop":DownCatsShop,
                  "DOwnCatsSnap":DownCatsSnap,
                  'CANONICAL_PATH':CANONICAL_PATH
            }
            return render(request,"HTML Files/SearchPage.html",context=contex)           

      else:
            PageItems=[]
            PageProducts=[]
            All=len(AllProducts)
            print(All)
            print("more than 30")
            for i in range(All):
                  for j in range(i,i+31):
                        if j%30==0 and j<All:
                              if All-j<30:
                                    LastNum=j
                              else:
                                    continue    
                        else: 
                              continue
            # print(LastNum)
            k=0
            for product in AllProducts:
                  PageItems.append(product)
                  if len(PageItems)<30:
                        if k>LastNum:
                              for item in AllProducts[k:]:
                                    PageItems.append(item)
                              PageProducts.append(list(PageItems))
                              break
                  elif len(PageItems)==30:
                        PageProducts.append(list(PageItems))
                        del PageItems[:]
                  else:
                        continue
                  k=k+1
            if len(PageProducts)>5:
                        if page_no==1:
                              L=list(range(page_no,page_no+4))
                        else:
                              if page_no+5<len(PageProducts):
                                    L=list(range(page_no-1,page_no+4))
                              else:
                                    L=list(range(page_no-1,len(PageProducts)+1))
            else:
                        L=list(range(1,len(PageProducts)+1))
            # print(len(PageProducts))
            CANONICAL_PATH=request.build_absolute_uri(request.path)
            if 'www.' in CANONICAL_PATH :
               CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

            contex={
                  "ProductsFlipkart":ProductListFlipkart,
                  "ProductsAmazon":ProductListAmazon,
                  "ProductsShopclues":ProductListShopclues,
                  "ProductsSnapdeal":ProductListSnapdeal,
                  "AllProducts":PageProducts[page_no-1],
                  "Length":L,
                  "next":page_no+1,
                  "FlipSubCats":FlipSubCats[0:3],
                  "AmazonSubCats":AmazonSubCats[0:3],
                  "ShopcluesSubCats":ShopcluesSubCats[0:3],
                  "SnapdealSubCats":SnapdealSubCats[0:3],
                  "Recommended":Recommended,
                  "search":str1,
                  "Featured":Featured,
                  "OnSale":OnSale,
                  "TopRated":TopRated,
                  "DownCatsAmzn":DownCatsAmzn,
                  "DownCatsFlip":DownCatsFlip,
                  "DownCatsShop":DownCatsShop,
                  "DOwnCatsSnap":DownCatsSnap,
                  'CANONICAL_PATH':CANONICAL_PATH
            }
            return render(request,"HTML Files/SearchPage.html",context=contex)

# def searchhaystack(request,page_no):

      # articles= SearchQuerySet().autocomplete(content_auto=request.GET.get('search',"default"))
      # return render(request,'HTML Files/SearchPage.html',{"AllProducts":articles})

def updateamazonproducts(request):
      all_urls=[amurl.prod_URL for amurl in Amazon_products]
      print(len(all_urls))
      l=46
      for (l,u) in enumerate(all_urls[46:]):
            print(l)
            try:
                  print(UpdateProductList(request,u))
            except:
                  print(str(l)+" not works")      
      return HttpResponse("<h1>All Products Updated</h1>")

def terms(request):

    
      SecondCats=["Laptops","Headphones","Cameras","Televisions","Furniture Accessories","Beauty Accessories","Smart Watches","Strollers & Activity Gear","Men's Footwear","Dining Tables & Sets","PIRASO Sunglasses","Smart Watches","Headphones","Beauty Accessories","Televisions"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

      r=random.randrange(0,len(SecondCats))
      s=random.randrange(0,len(SecondCats))
      t=random.randrange(0,len(SecondCats))
      Featured=[]
      OnSale=[]
      TopRated=[]
      Featured=(Shopclues.objects.filter(prod_Second_Category=SecondCats[r])[0:3])
      OnSale=(Shopclues.objects.filter(prod_Second_Category=SecondCats[s])[0:3])
      TopRated=(Shopclues.objects.filter(prod_Second_Category=SecondCats[t])[0:3])
      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')
      contex={
            'DownCats1':DownCats1,
            'DownCats2':DownCats2,
            'Featured':Featured,
            'OnSale':OnSale,
            'TopRated':TopRated,
            'CANONICAL_PATH':CANONICAL_PATH
      }


      return render(request,"HTML Files/T&Cs.html",context=contex)

def aboutus(request):


      SecondCats=["Laptops","Headphones","Cameras","Televisions","Furniture Accessories","Beauty Accessories","Smart Watches","Strollers & Activity Gear","Men's Footwear","Dining Tables & Sets","PIRASO Sunglasses","Smart Watches","Headphones","Beauty Accessories","Televisions"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

      r=random.randrange(0,len(SecondCats))
      s=random.randrange(0,len(SecondCats))
      t=random.randrange(0,len(SecondCats))
      Featured=[]
      OnSale=[]
      TopRated=[]
      Featured=(Shopclues.objects.filter(prod_Second_Category=SecondCats[r])[0:3])
      OnSale=(Shopclues.objects.filter(prod_Second_Category=SecondCats[s])[0:3])
      TopRated=(Shopclues.objects.filter(prod_Second_Category=SecondCats[t])[0:3])

      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

      contex={
            'DownCats1':DownCats1,
            'DownCats2':DownCats2,
            'Featured':Featured,
            'OnSale':OnSale,
            'TopRated':TopRated,
            'CANONICAL_PATH':CANONICAL_PATH
      }


      return render(request,"HTML Files/AboutUs.html",context=contex)

def contactus(request):
      

      SecondCats=["Laptops","Headphones","Cameras","Televisions","Furniture Accessories","Beauty Accessories","Smart Watches","Strollers & Activity Gear","Men's Footwear","Dining Tables & Sets","PIRASO Sunglasses","Smart Watches","Headphones","Beauty Accessories","Televisions"]
      DownCats1=SecondCats[0:6]
      random.shuffle(SecondCats)
      DownCats2=SecondCats[0:6]

      r=random.randrange(0,len(SecondCats))
      s=random.randrange(0,len(SecondCats))
      t=random.randrange(0,len(SecondCats))
      Featured=[]
      OnSale=[]
      TopRated=[]
      Featured=(Shopclues.objects.filter(prod_Second_Category=SecondCats[r])[0:3])
      OnSale=(Shopclues.objects.filter(prod_Second_Category=SecondCats[s])[0:3])
      TopRated=(Shopclues.objects.filter(prod_Second_Category=SecondCats[t])[0:3])

      CANONICAL_PATH=request.build_absolute_uri(request.path)
      if 'www.' in CANONICAL_PATH :
             CANONICAL_PATH=CANONICAL_PATH.replace('www.','')

      contex={
            'DownCats1':DownCats1,
            'DownCats2':DownCats2,
            'Featured':Featured,
            'OnSale':OnSale,
            'TopRated':TopRated,
            'CANONICAL_PATH':CANONICAL_PATH
      }


      return render(request,"HTML Files/ContactUs.html",context=contex)

def Checksearch(request,page_no):

      djtext=request.GET.get("search","default")
      if "www" in djtext:
            print(djtext)
            return search(request)
      else:
            print("default here")
            return searchfuzz(request,page_no)

def mobile(request):
      return render(request,"HTML Files/basic_m.html")

def post(request,page_url):
  #  if brand=="Amazon":
       product=Amazon.objects.filter(prod_url_title=str(page_url))
       for i in product:
           item=i
       return render (request,'HTML Files/all_urls.html',{'item':item})
  #  elif brand=="Snapdeal":
      # product=Snapdeal.objects.filter(prod_url_title=str(page_url))
     #  for i in product:
    #       item=i
   #    return render(request,'HTML Files/all_urls.html',{'item':item})
  #  elif brand=="Flipkart":
       #product=Shopclues.objects.filter(prod_url_title=str(page_url))
       #for i in product:
      #     item=i
       #return render(request,'HTML Files/all_urls.html',{'item':item})
  #  elif brand=="Shopclues":
   #    product=Shopclue.objects.filter(prod_url_title=str(page_url))
    #   for i in product:
     #      item=i
      # return render( 'HTML Files/all_urls.html',{'item':item})


def ads(request):

  ad="google.com, pub-1178708164274386, DIRECT, f08c47fec0942fa0"
  return HttpResponse(ad)
