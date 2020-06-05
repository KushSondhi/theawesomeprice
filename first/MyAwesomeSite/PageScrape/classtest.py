from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
import requests
import time
import random
from bs4 import BeautifulSoup as soup
from .models import Shopclues,Snapdeal,Shopclue,Amazon
from datetime import datetime

class Index():

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
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0",
                  "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246"
                  "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
    
    ]

    header={"User-Agent":UserAgents[0]}
    proxy={'http':'http://200.89.159.240:3128','https':'http://200.89.159.240:3128'}
    Snapdeal_products=Snapdeal.objects.all()
    Flipkart_products=Shopclues.objects.all()
    Amazon_products=Amazon.objects.all()
    Shopclues_products=Shopclue.objects.all()

    left_col_shopclues=[]
    right_col_shopclues=[]  

    left_col_flipkart=[]
    right_col_flipkart=[]

    highlights_snapdeal=[]    

    related_products_shopclues_urls=[]
    related_products_flipkart_urls=[]
    related_products_amazon_urls=[]
    related_products_snapdeal_urls=[]

    Flipkart_URL=None
    Flipkart_page_html=None
    Flipkart_item_name=None
    Flipkart_product_page_html=None
    Flipkart_title=None
    Flipkart_data_set=None

    Amazon_URL=None
    Amazon_page_html=None
    Amazon_item_name=None
    Amazon_data_set=None
    Amazon_product_page_html=None
    Amazon_title=None

    Shopclues_URL=None
    Shopclues_page_html=None
    Shopclues_item_name=None
    Shopclues_data_set=None
    Shopclues_product_page_html=None
    Shopclues_title=None

    Snapdeal_URL=None
    Snapdeal_page_html=None
    Snapdeal_item_name=None
    Snapdeal_data_set=None
    Snapdeal_product_page_html=None
    Snapdeal_title=None

    def StartAddingProductsFlipkart(self,url):

      self.Flipkart_URL=url
      Flipkart_response=requests.get(self.Flipkart_URL)
      self.Flipkart_page_html=soup(Flipkart_response.content,'lxml')
      self.Flipkart_page_html.prettify
      self.Flipkart_item_name=self.Flipkart_page_html.find('span',attrs={'class':'_35KyD6'})
      self.Flipkart_item_name=self.Flipkart_item_name.text.replace('\n','')
      #print(self.Flipkart_item_name)
      return self.CheckProductAvailabilityFlipkart(self.Flipkart_item_name,url)

    def CheckProductAvailabilityFlipkart(self,product_name,url):

      self.Flipkart_data_set=Shopclues()
      
      database_prduct=Shopclues.objects.filter(prod_name=product_name)
      #print(Flipkart_url)
      #spr=Shopclues.objects.filter(prod_name=product_name)
      #print(len(list(Shopclues.objects.all())))
      print(database_prduct)
      #print(spr)
      if database_prduct:
            print('Flipkart Existing Product')
            for dbsprd in database_prduct:
                        return (self.AddProductsFlipkart(dbsprd,url))
      else:
            print('Flipkart New Product')      
            return(self.AddProductsFlipkart(self.Flipkart_data_set,url))


    def AddProductsFlipkart(self,take_item,url_prod):

            # global  Flipkart_product_page_response
            # global  Flipkart_product_page_html
            Flipkart_product_page_response=requests.get(url_prod)
            self.Flipkart_product_page_html=soup(Flipkart_product_page_response.content,'lxml')

            try:
                  item_name=self.Flipkart_product_page_html.find('span',attrs={'class':'_35KyD6'}).text
                  take_item.prod_name=item_name
            except:
                  take_item.prod_name='None'
            temp_name=take_item.prod_name[0:50]+"...."
            take_item.prod_temp_name=temp_name
            
            title=take_item.prod_name.replace("/","-").replace("  ","-").replace("   ","-").replace("    ","-")
            titl=title.replace(" ","-")
            x=[i for i in titl.replace("  ","-").split()]
                  # print(x)
            put=''
            for p in x:
                  if p!=x[-1]:
                        put+=p+'-'
                  else:
                        put+=p
            take_item.prod_url_title=put
            #print(take_item.prod_url_title)
            
            url='/flipkart/product='+take_item.prod_url_title
            take_item.prod_page_URL=url

            try:
                  item_price=self.Flipkart_product_page_html.find('div',attrs={'class':'_1vC4OE _3qQ9m1'})
                  take_item.prod_price=(item_price.text)
                 # print('NEW PRICE :-'+str(take_item.prod_price.encode('utf-8')))
            except:
                  take_item.prod_price=('')

            try:
                  item_mrp=self.Flipkart_product_page_html.find('div',{'class':'_3auQ3N _1POkHg'})
                  take_item.prod_mrp=item_mrp.text
            except:
                  take_item.prod_mrp=('')

            #date=datetime.now().date()
            #take_item.prod_Date=str(date)
            #print(take_item.prod_Date)

            #take_item.save()
 
            
# <---------------------------------------------------------------------------------------------------------------------------------------------->
            try:
                  image=self.Flipkart_product_page_html.find('div',attrs={'class':'_2_AcLJ'})
                  img=image['style']
                  low_image=img[21:len(img)-1]
                  take_item.prod_display_image_URL=low_image
                  high_imj=low_image.replace('/128/128/','/583/700/')
                  take_item.prod_image_URL=high_imj
            except:
                  take_item.prod_image_URL=''

            try:
                for (i,judge) in  enumerate(self.Flipkart_product_page_html.find_all('div',attrs={'class':'_2yc1Qo'})):
                  if i==0:
                        rating=judge.text.split(' ')
                        take_item.prod_ratings=rating[0]
                  if i==1:
                        review=judge.text.split(' ')
                        take_item.prod_reviews=review[0]
            except:
                  take_item.prod_ratings=''
                  take_item.prod_reviews=''

            try:
                  overall=self.Flipkart_product_page_html.find('div',attrs={'class':'_1i0wk8'})
                  take_item.prod_overall=overall.text
            except:
                  take_item.prod_overall=''

            try:
                  star=self.Flipkart_product_page_html.find('div',attrs={'class':'_2txNna'})
                  take_item.prod_star=star.text
                  # print(take_item.prod_star)
            except:
                  take_item.prod_star=''

            take_item.prod_URL=url_prod           
            #print(take_item.prod_URL)
            #print(url_prod)
            date=datetime.now().date()
            take_item.prod_Date=str(date)
            print(take_item.prod_Date)
           # print(str(take_item.prod_name))

            return self.AddCategoryFlipkart(take_item)

    def AddCategoryFlipkart(self,prdct):
      i=0
      for (i,category) in enumerate(self.Flipkart_product_page_html.find_all('div',{'class':'_1HEvv0'})):
       if i==1:
            prdct.prod_First_Category=category.text
       if i==2:
            prdct.prod_Second_Category=category.text
       if i==3:
            prdct.prod_Third_Category=category.text
 #     print(prdct.prod_name)
      return self.SpecificationsFlipkart(prdct)

    def SpecificationsFlipkart(self,item):

      del self.left_col_flipkart[:]
      del self.right_col_flipkart[:]
      for td in self.Flipkart_product_page_html.find_all('td',attrs={'class':'_3-wDH3 col col-3-12'}):
        self.left_col_flipkart.append(td.text)
      item.prod_specs_left=list(self.left_col_flipkart)
      for td in self.Flipkart_product_page_html.find_all('td',attrs={'class':'_2k4JXJ col col-9-12'}):
            td=td.text.replace(',',' | ')
            td=td.replace(',',' | ')
            self.right_col_flipkart.append(td)
      item.prod_specs_right=list(self.right_col_flipkart)
      if len(self.left_col_flipkart)and len(self.right_col_flipkart)==0 :
        return (self.DetailsFlipkart(item))
      else:
             item.save()
             print('All Details Updated')
             #return '..'
             return(str(item.prod_name.encode('utf-8')))
            # return(items.prod_temp_name)
            # return("Flipkart Product Added")

    def DetailsFlipkart(self,items):

      del self.left_col_flipkart[:]
      del self.right_col_flipkart[:]
      print('Details')
      for col in self.Flipkart_product_page_html.findAll('div',attrs={'class':'col col-3-12 _1kyh2f'}):
         self.left_col_flipkart.append(col.text)
      items.prod_specs_left=self.left_col_flipkart
      for col in self.Flipkart_page_html.findAll('div',attrs={'class':'col col-9-12 _1BMpvA'}):
         self.right_col_flipkart.append(col.text.replace(',',' | '))
      items.prod_specs_right=self.right_col_flipkart
      print('Going to save')
      items.save()
      print('Everything About Product Updated')
      #return '.'
      return(str(items.prod_name.encode('utf-8')))
      # return (items.save())

    def URLforFlipkart(self,productname):

      #     global Flipkart_title
          Flipkart_response=None
      #     global Flipkart_page_html
          self.Flipkart_title=productname
          print(self.Flipkart_title)
          print(productname)
          Flipkart_URL='https://www.flipkart.com/search?q='  
          title_items=[x for x in self.Flipkart_title.split(' ')]
          result_url=''
          for i in title_items:
            if i!=title_items[-1]:
                result_url+=(i+'%20')
            else:
                result_url+=i
          Flipkart_URL+=(result_url)
          print(result_url)
          print(Flipkart_URL)
          Flipkart_response=requests.get(Flipkart_URL)
          self.Flipkart_page_html=soup(Flipkart_response.content,"lxml")
          self.Flipkart_page_html.prettify
          return self.RelatedFlipkart(Flipkart_URL)

    def RelatedFlipkart(self,URL):

          del self.related_products_flipkart_urls[::]
          class_attributes=['_2cLu-l','_2mylT6','_3dqZjq']
          print('Related Flipkart')
          for value in class_attributes:
            if len(self.related_products_flipkart_urls)<=0:
                print(self.inside_edge(value))
            else:
                print('NOO..')
                break
                #del self.related_products_flipkart_urls[::]
      #     if len(self.related_products_flipkart_urls)<=0:
          for j in self.Flipkart_page_html.find_all('a',attrs={'class':'_31qSD5'}):
            self.related_products_flipkart_urls.append('https://www.flipkart.com'+str(j['href']))
          print(len(self.related_products_flipkart_urls))
          for t in range(len(self.related_products_flipkart_urls)):
            if len(self.related_products_flipkart_urls)>=40:
                   print('find more than range')
                   self.related_products_flipkart_urls.pop()
            else:
                  print('inside range') 
                  return(self.VisitProductPageFlipkart(self.related_products_flipkart_urls))
      #     else:
      #           print(len(self.related_products_flipkart_urls))
      #           for h in range(len(self.related_products_flipkart_urls)):
      #             if len(self.related_products_flipkart_urls)>=40:
      #                   self.related_products_flipkart_urls.pop()
      #             else:
      #                   return (self.VisitProductPageFlipkart(self.related_products_flipkart_urls))

    def inside_edge(self,v):
        for i in self.Flipkart_page_html.findAll('a',{'class':v}):
            self.related_products_flipkart_urls.append('https://www.flipkart.com'+i['href'])
        return ''

    def VisitProductPageFlipkart(self,list_of_urls):
      #     global Flipkart_data_set
      #     print(list_of_urls)
          i=0
          for url in list_of_urls:
                self.Flipkart_data_set=Shopclues()
                try:
                  response=requests.get(url)
                  html_prod_page=soup(response.content,'lxml')
                  title=html_prod_page.find('span',attrs={'class':'_35KyD6'})
                  prod_title=(title.text.replace('\n',''))
                except:
                      i=i+1
                      print('down-->'+str(i))
                      continue
                print(self.CheckProductAvailabilityFlipkart(prod_title,url))
          return 'All Flipkart Related Products Added'

    def StartAddingProductsAmazon(self,url):

          self.Amazon_URL=url
          Amazon_response=requests.get(self.Amazon_URL,headers=self.header)
          self.Amazon_page_html=soup(Amazon_response.content,'lxml')
          self.Amazon_page_html.prettify()
          self.Amazon_item_name=self.Amazon_page_html.find('span',attrs={'id':'productTitle'})
          self.Amazon_item_name=self.Amazon_item_name.text.strip().replace('\n','')
          
          return (self.CheckProductAvailibilityAmazon(self.Amazon_item_name,self.Amazon_URL))

    def CheckProductAvailibilityAmazon(self,name,url_of_prod):

      #     global Amazon_data_set
          self.Amazon_data_set=Amazon()

          product_database=Amazon.objects.filter(prod_URL=url_of_prod)
          if product_database:
                print('Amazon Existing Product')
                for dbsprdct in product_database:
                      return (self.AddProductsAmazon(dbsprdct,url_of_prod))
          else:
            print('Amazon New Product')  
            return(self.AddProductsAmazon(self.Amazon_data_set,url_of_prod))            

    def AddProductsAmazon(self,take_item,prod_url):

          print('Adding product to amazon')
          Amazon_product_page_response=requests.get(prod_url,headers=self.header)
          self.Amazon_product_page_html=soup(Amazon_product_page_response.content,'lxml')
          self.Amazon_product_page_html.prettify()

          try:
                ProductName=self.Amazon_product_page_html.find('span',attrs={'id':'productTitle'})
                ProductName=ProductName.text.strip().replace('\n','')
                take_item.prod_name=ProductName
          except:
                take_item.prod_name=('None')
            
          temp_name=take_item.prod_name[0:50]+' ...'
          take_item.prod_temp_name=temp_name              

          title=take_item.prod_name
          title=take_item.prod_name.replace('/','-').replace(' ','-').replace('   ','-').replace('    ','-')
          titl=title.replace(' ','-')
          x=[i for i in titl.replace('  ','-').split()]
          print(x)
          put=''
          for p in x:
                  if p!=x[-1]:
                        put+=p+'-'
                  else:
                        put+=p
          take_item.prod_url_title=put

          url='/Amazon/product='+take_item.prod_url_title
          take_item.prod_page_URL=url
          
          try:
                price=self.Amazon_product_page_html.find('span',attrs={'id':'priceblock_ourprice'})
                price=price.text.strip().replace('\n','')
                take_item.prod_price=str(price)
          except:
                price=self.Amazon_product_page_html.find('span',attrs={'id':'priceblock_dealprice'})
                if price is None:
                      try:
                        sale_price=self.Amazon_product_page_html.find('span',attrs={'id','priceblock_saleprice'})
                        sale_price=sale_price.text.strip().replace('\n','')
                        take_item.prod_price=sale_price
                        print('Sale Price')
                      except:
                            take_item.prod_price=''
                else:
                      price=price.text.strip().replace('\n','')
                      take_item.prod_price=str(price)

          try:
                mrp=self.Amazon_product_page_html.find('span',attrs={'class':'priceBlockStrikePriceString a-text-strike'}).text
                take_item.prod_mrp=str(mrp)
          except:
                mrp=self.Amazon_product_page_html.find('span',attrs={'class':'a-size-medium a-color-price priceBlockDealPriceString'})
                if mrp is not None:
                  mrp=mrp.text
                  take_item.prod_mrp=str(mrp)
                else:
                      take_item.prod_mrp=''

          try:
                j=0
                CatLine=self.Amazon_product_page_html.find('ul',attrs={'class':'a-unordered-list a-horizontal a-size-small'})
                for (j,li) in enumerate(CatLine.findAll("a",attrs={'class':'a-link-normal a-color-tertiary'})):
                      if j==0:
                              # print(li.text.strip())
                              take_item.prod_First_Category=li.text.strip()
                      elif j==1:
                            take_item.prod_Second_Category=li.text.strip()
                      else:
                            print(str(take_item.prod_First_Category.encode('utf-8')))
                            print(str(take_item.prod_Second_Category.encode('utf-8')))
                            break
          except:
                take_item.prod_First_Category=None
                take_item.prod_Second_Category=None

          try:
                availi=self.Amazon_product_page_html.find('span',attrs={'class':'a-size-medium a-color-success'})
                availi=availi.text.strip().replace('\n','')
                take_item.prod_availi=availi
          except:
                take_item.prod_availi=('No Data')

          Image=[]
          try:
            left=self.Amazon_product_page_html.find('div',attrs={'id':'leftCol'})
            for image in left.find_all('img'):
                        Image.append(image['src'])
            # print(Image)
            take_item.prod_image_URL=Image[-1]

          except:
                take_item.prod_image_URL=''
          try:
                reviews=self.Amazon_product_page_html.find('h2',attrs={'data-hook':'total-review-count'})
                reviews=reviews.text.strip().replace('\n','').replace('  ','')
                take_item.prod_reviews=reviews
          except:
                take_item.prod_reviews='Be The First To Review This'

          try:
                rating_1star=self.Amazon_product_page_html.find('a',attrs={'class':'a-size-base a-link-normal 1star histogram-review-count a-color-secondary'})
                take_item.prod_ratings_1start=rating_1star.text.strip().replace('\n','').replace('  ','')
          except:
                take_item.prod_ratings_1start='0%'

          try:
                rating_2star=self.Amazon_product_page_html.find('a',attrs={'class':'a-size-base a-link-normal 2star histogram-review-count a-color-secondary'})
                take_item.prod_ratings_2start=rating_2star.text.strip().replace('\n','').replace('  ','')
          except:
                take_item.prod_ratings_2start='0%'

          try:
                rating_3star=self.Amazon_product_page_html.find('a',attrs={'class':'a-size-base a-link-normal 3star histogram-review-count a-color-secondary'})
                take_item.prod_ratings_3start=rating_3star.text.strip().replace('\n','').replace('  ','')
          except:
                take_item.prod_ratings_3start='0%'

          try:
                rating_4star=self.Amazon_product_page_html.find('a',attrs={'class':'a-size-base a-link-normal 4star histogram-review-count a-color-secondary'})
                take_item.prod_ratings_4start=rating_4star.text.strip().replace('\n','').replace('  ','')
          except:
                take_item.prod_ratings_4start='0%'

          try:
                rating_5star=self.Amazon_product_page_html.find('a',attrs={'class':'a-size-base a-link-normal 5star histogram-review-count a-color-secondary'})
                take_item.prod_ratings_5start=rating_5star.text.strip().replace('\n','').replace('  ','')
          except:
                take_item.prod_ratings_5start='0%'

          try:
            Left=[]
            Right=[]
            Review=self.Amazon_product_page_html.find('div',attrs={'class':'review'})
            for left in Review.find_all('div',attrs={'class':'a-fixed-right-grid-col a-col-left'}):
                  Left.append(left.text.strip().replace('\n',''))
            take_item.prod_ratings_FeatureKey=list(Left)
            for right in Review.find_all('div',attrs={'class':'a-text-right a-fixed-right-grid-col a-col-right'}):
                        Right.append(right.text.strip().replace('\n',''))
            take_item.prod_ratings_FeatureValue=list(Right)
          except:
                take_item.prod_ratings_FeatureKey=[]
                take_item.prod_ratings_FeatureValue=[]

          take_item.prod_URL=prod_url

          date=datetime.now().date()
          take_item.prod_Date=str(date)
          print(take_item.prod_Date)
          print('DATE Upp--')
          take_item.save()
          print("SAVED")
          return str(self.take_item.prod_name.encode('utf-8'))
#          return self.TechDetailsAmazon(take_item)

    def TechDetailsAmazon(self,prdct):

          print('Technical Details')
          left_col_amazon=[]
          right_col_amazon=[]

          del left_col_amazon[:]
          del right_col_amazon[:]

          try:
            # if len(left_col_amazon) or len(right_col_amazon)<=0:
                    for key in self.Amazon_product_page_html.find_all('td',attrs={'class':'label'}):
                            key=key.text
                            left_col_amazon.append(key)
                    time.sleep(0.5)
                    for value in self.Amazon_product_page_html.find_all('td',attrs={'class':'value'}):
                            value=value.text.strip().replace('\n','').replace(',','|')
                            right_col_amazon.append(value)
                    if len(left_col_amazon)>0:
                            prdct.prod_specs_left=list(left_col_amazon)
                            prdct.prod_specs_right=list(right_col_amazon)
                            prdct.save()
                            return self.SpecificationsAmazon(prdct)
          except:

                if len(left_col_amazon)<=0 or len(right_col_amazon)<=0:

                        del left_col_amazon[:]
                        del right_col_amazon[:]
                        for key in self.Amazon_product_page_html.find_all('th',attrs={'class':'a-span5 a-size-base'}):
                              key=key.text.strip().replace('\n','')
                              left_col_amazon.append(key)
                        time.sleep(0.8)
                        for value in self.Amazon_product_page_html.find_all('td',attrs={'class':'a-span7 a-size-base'}):
                              value=value.text.strip().replace('\n','').replace(',','|')
                              right_col_amazon.append(value)
                        if len(left_col_amazon)>0:
                              prdct.prod_specs_left=list(left_col_amazon)
                              prdct.prod_specs_right=list(right_col_amazon)
                              prdct.save()
                              return self.SpecificationsAmazon(prdct)

          try:

                  if len(left_col_amazon) or len(right_col_amazon)<=0:

                        del left_col_amazon[:]
                        del right_col_amazon[:]

                        for table in self.Amazon_product_page_html.findAll('table',attrs={'id':'tech-specs-table-left'}):
                              for key in table.findAll('td'):
                                    if key.has_attr('class'):
                                          key=key.text.strip().replace('\n','').replace(' ','')
                                          left_col_amazon.append(key)
                                    else:
                                          key=key.text.strip().replace('\n','').replace(' ','').replace(',','|')
                                          right_col_amazon.append(key)
                        if len(left_col_amazon)>0:
                              prdct.prod_specs_left=list(left_col_amazon)
                              prdct.prod_specs_right=list(right_col_amazon)
                              prdct.save()
                              return self.SpecificationsAmazon(prdct)

          except:
                  if len(left_col_amazon) or len(right_col_amazon)<=0:

                        return self.SpecificationsAmazon(prdct)

          else:
                return self.SpecificationsAmazon(prdct)

    def SpecificationsAmazon(self,prdct):

          print('Specifications Amazon')
          p_specs_amazon=[]
          del p_specs_amazon[:]

          try:
            ul=self.Amazon_product_page_html.find('ul',attrs={'class':'a-unordered-list a-vertical a-spacing-none'})
            for li in ul.find_all('span',attrs={'class':'a-list-item'}):
                  p_specs_amazon.append(li.text.strip().replace('\n','').replace('  ',''))
            if len(p_specs_amazon)>0:
                  # print(p_specs_amazon)
                  prdct.prod_specifications=list(p_specs_amazon)
                  return self.DescriptionAmazon(prdct)

          except:
            # print("then")
            prdct.prod_specifications='No specifications'
            return self.DescriptionAmazon(prdct)

    def DescriptionAmazon(self,prdct):

      print('Description Amazon')
      prod_description_amazon=[]
      del prod_description_amazon[:]

      try:
            prod_description=self.Amazon_product_page_html.find('div',attrs={'id':'productDescription'})
            prod_description=prod_description.text.strip().replace('\n','')
            prod_description_amazon.append(prod_description)
            prdct.prod_description=prod_description_amazon
            prdct.save()
            return (str(prdct.prod_name))
      except:
            prdct.prod_description=('No Description Available')
            print(prdct.prod_temp_name)
            prdct.save()
            return(str(prdct.prod_name))

    def URLforAmazon(self,productname):

          print(productname)
          self.Amazon_title=productname
          print("NAME+++++++"+self.Amazon_title)
          self.Amazon_URL='https://www.amazon.in/s?k='
          title_items=[items for items in self.Amazon_title.split(' ')]
          result_url=''
          for i in title_items:
            if i!=title_items[-1]:
                result_url+=(i+'+')
            else:
                result_url+=i
          self.Amazon_URL+=result_url
          Amazon_response=requests.get(self.Amazon_URL,headers=self.header)
          self.Amazon_page_html=soup(Amazon_response.content,'lxml')
          self.Amazon_page_html.prettify()

          return self.RelatedAmazon(self.Amazon_URL)

    def RelatedAmazon(self,URL):

      del self.related_products_amazon_urls[:]

      for link in self.Amazon_page_html.find_all('a',attrs={'class':'a-link-normal a-text-normal'}):
                link_url='https://www.amazon.in'+str(link['href'])
                self.related_products_amazon_urls.append(link_url)
      for o in range(len(self.related_products_amazon_urls)):
            if len(self.related_products_amazon_urls)>20:
                  self.related_products_amazon_urls.pop()
            else:
                  print("IM HERE")
                  print(len(self.related_products_amazon_urls))
                  return self.VisitProductPageAmazon(self.related_products_amazon_urls)

    def VisitProductPageAmazon(self,list_of_urls):
          i=0
          for url in list_of_urls:
                self.Amazon_data_set=Amazon()
                response=requests.get(url,headers=self.header)
                html_prod_page=soup(response.content,'lxml')
                try:
                  prod_title=html_prod_page.find('span',attrs={'id':'productTitle'})
                  prod_title=prod_title.text.strip().replace('\n','')
                except:
                      continue
                print(i)
                print(self.CheckProductAvailibilityAmazon(prod_title,url))
                i=i+1
          return 'Amazon Related Products Added'

    def StartAddingProductsShopclues(self,url):

          self.Shopclues_URL=url
          Shopclues_response=requests.get(self.Shopclues_URL,headers=self.header)
          self.Shopclues_page_html=soup(Shopclues_response.content,'lxml')
          self.Shopclues_page_html.prettify
          self.Shopclues_item_name=self.Shopclues_page_html.find('h1',attrs={'itemprop':'name'})
          self.Shopclues_item_name=self.Shopclues_item_name.text.strip().replace('\n','')
          print('AAAYA')
         # print(self.Shopclues_item_name)

          return self.CheckProductAvailabilityShopclues(self.Shopclues_item_name,self.Shopclues_URL)

    def CheckProductAvailabilityShopclues(self,name,url_of_prod):

          self.Shopclues_data_set=Shopclue()
          product_database=Shopclue.objects.filter(prod_URL=url_of_prod)
          if product_database:
            print('Shopclues Existing product')    
            for dbsprdct in product_database:
                  return self.AddProductsShopclues(dbsprdct,url_of_prod)
          else:
                print('Shopclues New Product')
                return(self.AddProductsShopclues(self.Shopclues_data_set,url_of_prod))

    def AddProductsShopclues(self,take_item,prod_url):

      Shopclues_product_page_response=requests.get(prod_url,headers=self.header)
      self.Shopclues_product_page_html=soup(Shopclues_product_page_response.content,'lxml')

      try:
          item_name=self.Shopclues_product_page_html.find('h1',attrs={'itemprop':'name'})
          take_item.prod_name=item_name.text.strip().replace('\n','')
      except:
          take_item.prod_name=('..')

      temp_name=take_item.prod_name[0:50]+' ...'
      take_item.prod_temp_name=temp_name          

      title=take_item.prod_name.replace('/','-').replace('  ','-').replace('   ','-').replace('    ','-')
      titl=title.replace(' ','-')
      x=[i for i in titl.replace('  ','-').split()]
#      print(x)
      put=''
      for p in x:
                  if p!=x[-1]:
                        put+=p+'-'
                  else:
                        put+=p
      take_item.prod_url_title=put
#      print(take_item.prod_url_title)

      url='/shopclues/product='+take_item.prod_url_title
      take_item.prod_page_URL=url

      # take_item.save()
      try:
          item_price=self.Shopclues_product_page_html.find('span',attrs={'class':'f_price'})
          item_price=str(item_price.text.strip().replace('\n','').replace('Rs.',''))
          if len(item_price)<1:
                para=self.Shopclues_product_page_html.find('div',attrs={'class':'soldout_content'})
                for price in para.find('h4'):
                  take_item.prod_price=str(price.text)
                  break
          else:
                take_item.prod_price=(item_price)
      except:
          take_item.prod_price=None
      try:
          item_mrp=self.Shopclues_product_page_html.find('span',attrs={'class':'o_price'})
          mr_p=item_mrp.text.strip().replace('\n','').replace('Rs.','')
          take_item.prod_mrp=str(mr_p)
      except:
            try:
                item_mrp=self.Shopclues_product_page_html.find('span',attrs={'class':'o_price1'})
                mr_p=item_mrp.text.strip().replace('\n','').replace('Rs.','')
                take_item.prod_mrp=str(mr_p)
            except:
                  take_item.prod_mrp=''    
      
      try:
            overall=self.Shopclues_product_page_html.find('span',attrs={'class':'val'})
            take_item.prod_overall=str(overall.text.replace('"','').replace('\n',''))
      except:
            take_item.prod_overall=None            

      try:
          image=self.Shopclues_product_page_html.find('img',attrs={'class':'img'})
          take_item.prod_image_URL=image['src']
      except:
          take_item.prod_image_URL=''

      try:
            rate=self.Shopclues_product_page_html.find('span',attrs={'itemprop':'ratingValue'})
            if rate=='None':
                  take_item.prod_ratings=''
            else:
                  take_item.prod_ratings=str(rate)
      except:
            take_item.prod_ratings='Be The First To Rate This'

      try:
            rev=self.Shopclues_product_page_html.find('span',attrs={'class':'rating_num'})
            take_item.prod_reviews=str(rev.text.replace(')','').replace('(',''))
      except:
            take_item.prod_reviews=None

      take_item.prod_URL=str(prod_url)
      date=datetime.now().date()
      take_item.prod_Date=date
      # take_item.save()
      print("adding done")
      return self.SpecificationsShopclues(take_item)

    def SpecificationsShopclues(self,items):

          del self.left_col_shopclues[:]
          del self.right_col_shopclues[:]
          try:
            for key in self.Shopclues_product_page_html.find_all('td',attrs={'width':'30%'}):
                  self.left_col_shopclues.append(str(key.text.strip().replace('\n','')))
            items.prod_specs_left=list(self.left_col_shopclues)
            for value in self.Shopclues_product_page_html.find_all('td',attrs={'width':'70%'}):
                  val=value.text.strip()
                  vall=val.replace(',','|').replace('\n','')
                  va=vall.replace(':','')
                  vaa=va.replace('\xa0','').replace(',','|')
                  self.right_col_shopclues.append(str(vaa))
            items.prod_specs_right=list(self.right_col_shopclues)
            print('Speci Done')
         #   print(items.prod_specs_right)
            #items.save()
          except:
            print('speci not done')
      #     items.save()
          return self.DescriptionShopclues(items)

    def DescriptionShopclues(self,prdct):
    
            for label in self.Shopclues_product_page_html.find_all('td',attrs={'class':'label'}):
                  self.left_col_shopclues.append(str(label.text.strip().replace(",","|").replace("\n","")))
            prdct.prod_specs_left=list(self.left_col_shopclues)            
            for value in self.Shopclues_product_page_html.find_all('td',attrs={'class':'value'}):
                  self.right_col_shopclues.append(str(value.text.strip().replace(',','|').replace('\n','')))
            prdct.prod_specs_right=list(self.right_col_shopclues)        
            if len(self.right_col_shopclues)<=0 or len(self.left_col_shopclues)<=0:
                  prdct.prod_specs_left=['-']
                  prdct.prod_specs_right=['-']
                  # print("Desc not found")
                  # prdc.save()
                  return self.AddCategoryShopclues(prdct)
            # prdc.save()
            return self.AddCategoryShopclues(prdct)

    def AddCategoryShopclues(self,prdct):
          print("adding cat")  
          try:
            im=0
            for (im,category) in enumerate(self.Shopclues_product_page_html.find_all('span',attrs={'itemprop':'title'})):
                  if im==1:
                        prdct.prod_First_Category=str(category.text.replace('\n',''))
                  elif im==2:
                        prdct.prod_Second_Category=str(category.text.replace('\n',''))
                  elif im==3:
                        prdct.prod_Third_Category=str(category.text.replace('\n',''))
            prdct.save()
            print('Cat Adding')
            # print(prdct.prod_First_Category)
            # print(prdct.prod_Second_Category)
            return (str(prdct.prod_name))
          except:
                prdct.prod_First_Category=''
                prdct.prod_Second_Category=''
                prdct.prod_Third_Category=''   
                prdct.save()
                print('cat not adding')
                return (prdct.prod_name.encode('utf-8'))     
          prdct.save()    
          print('Outside function')
          return (str(prdct.prod_name)) 

    def URLforShopclues(self,productname):

        self.Shopclues_title=productname
        self.Shopclues_URL='https://www.shopclues.com/search?q='
        title_items=[x for x in self.Shopclues_title.split(' ')]
        result_url=''
        for i in title_items:
            if i!=title_items[-1]:
                result_url+=(i+'%20')
            else:
                result_url+=i
        self.Shopclues_URL+=result_url
        Shopclues_response=requests.get(self.Shopclues_URL)
        self.Shopclues_page_html=soup(Shopclues_response.content,'lxml')
        self.Shopclues_page_html.prettify
        return self.RelatedShopclues(self.Shopclues_URL)

    def RelatedShopclues(self,URL):

          del self.related_products_shopclues_urls[:]
          for i in self.Shopclues_page_html.find_all('div',attrs={'class':'column col3 search_blocks'}):
                p_url=i.find('a')
                self.related_products_shopclues_urls.append('https:'+p_url['href'])

          if len(self.related_products_shopclues_urls)<=0:
            for i in self.Shopclues_page_html.findAll('div',attrs={'class':'column col3'}):
                p_url=i.find("a")
                self.related_products_shopclues_urls.append('https:'+p_url['href'])
          print('Total Products Related from shopclues= '+ str(len(self.related_products_shopclues_urls)))
      #     print(self.related_products_shopclues_urls)
          for j in range(len(self.related_products_shopclues_urls)):
                if len(self.related_products_shopclues_urls)>=40:
                    self.related_products_shopclues_urls.pop()
                else:
                      return (self.VisitProductPageShopclues(self.related_products_shopclues_urls))

    def VisitProductPageShopclues(self,list_of_urls):  
          ut=0
          for url in list_of_urls:
                try:
                  self.Shopclues_data_set=Shopclue()
                  response=requests.get(url)
                  html_prod_page=soup(response.content,'lxml')
                  title=html_prod_page.find('h1',attrs={'itemprop':'name'})
                  prod_title=title.text.strip().replace('\n','')
                  print('up') 
                  print(self.CheckProductAvailabilityShopclues(prod_title,url)) 
                except:
                      ut=ut+1
                      print('down-->'+str(ut))
                      continue       
          return ('All Shopclues related products added')

    def StartAddingProductsSnapdeal(self,url):
          
          self.Snapdeal_URL=url
          #print(self.Snapdeal_URL)
          Snapdeal_response=requests.get(self.Snapdeal_URL)
          self.Snapdeal_page_html=soup(Snapdeal_response.content,'lxml')
          self.Snapdeal_page_html.prettify()
          try:
                self.Snapdeal_item_name=self.Snapdeal_page_html.find('h1',attrs={'itemprop':'name'})
                self.Snapdeal_item_name=self.Snapdeal_item_name.text.strip().replace('\n',"")
          except:
                print("Name of the product is not found . ")
                name=self.Snapdeal_page_html.find('span',attrs={'class':'active-bread'})
           #     print(name.text)
                self.Snapdeal_item_name=name.text
          #print(str(self.Snapdeal_item_name.encode('utf-8')))

          return self.CheckProductAvailabilitySnapdeal(self.Snapdeal_item_name,self.Snapdeal_URL)

    def CheckProductAvailabilitySnapdeal(self,product_name,url_of_product):

      #     global Snapdeal_data_set
          self.Snapdeal_data_set=Snapdeal()
          database_product=Snapdeal.objects.filter(prod_URL=url_of_product)
          if database_product:
                print("Snapdeal Existing Product")
                for dbsprdct in database_product:
                      return self.AddProductsSnapdeal(dbsprdct,url_of_product)
          else:
                print("Snapdeal New Product")
                return self.AddProductsSnapdeal(self.Snapdeal_data_set,url_of_product)

    def AddProductsSnapdeal(self,take_item,prod_url):
     
            Snapdeal_product_page_response=requests.get(prod_url)
            self.Snapdeal_product_page_html=soup(Snapdeal_product_page_response.content,"lxml")

            try:
                ProductName=self.Snapdeal_product_page_html.find('h1',attrs={'itemprop':'name'})
                take_item.prod_name=(ProductName.text.strip().replace('\n',""))
            except:
                take_item.prod_name=("Not available")

            temp_name=take_item.prod_name[0:50]+" ..."
            take_item.prod_temp_name=temp_name    

            title=take_item.prod_name
            title=take_item.prod_name.replace("/","-").replace("  ","-").replace("   ","-").replace("    ","-")
            titl=title.replace(" ","-")
            x=[i for i in titl.replace("  ","-").split()]
            put=""
            for p in x:
                        if p!=x[-1]:
                              put+=p+"-"
                        else:
                              put+=p
            take_item.prod_url_title=put

            url="/snapdeal/product="+take_item.prod_url_title
            take_item.prod_page_URL=url

            try:
                price=self.Snapdeal_product_page_html.find("span",attrs={"class":"payBlkBig"})
                pr=price.text.strip().replace('\n',"").replace(" ","").replace("Rs.","")
                take_item.prod_price="Rs."+pr
            except:
                take_item.prod_price=("")

            try:
                mrp=self.Snapdeal_product_page_html.find("div",attrs={"class":"pdpCutPrice"})
                take_item.prod_mrp=mrp.text.replace("MRP","").replace("(Inclusive of all taxes)","").replace("Rs.","").replace("  ","").strip()
            #     take_item.prod_mrp=take_item.prod_mrp
            except:
                take_item.prod_mrp=("")

            try:
                image=self.Snapdeal_product_page_html.find("img",attrs={"class":"cloudzoom"})
                take_item.prod_image_URL=(image["src"])
            except:
                take_item.prod_image_URL=("")

            try:
                rating=self.Snapdeal_product_page_html.find("span",attrs={"class":"total-rating showRatingTooltip"})
                take_item.prod_ratings=rating.text.strip().replace("\n","")
            except:
                  take_item.prod_ratings=""

            try:
                 review=self.Snapdeal_product_page_html.find("span",attrs={"class":"numbr-review"})
                 take_item.prod_reviews=review.text
            except:
                  take_item.prod_reviews=""
            try:
                  overall=self.Snapdeal_product_page_html.find("span",attrs={"class":"avrg-rating"})
                  take_item.prod_overall=overall.text.replace("(","").replace(")","")
            except:
                  take_item.prod_overall=""      
            take_item.prod_URL=prod_url

            date=datetime.now().date()
            take_item.prod_Date=str(date)
            print('TODAY"S DATE :-')
            print(take_item.prod_Date)
           
            return self.SpecificationsSnapdeal(take_item)

    def SpecificationsSnapdeal(self,prdct):

            left_col_snapdeal=[]
            right_col_snapdeal=[]
            for table in self.Snapdeal_product_page_html.findAll('table',attrs={'class':'product-spec'}):
                for keys in table.findAll('td'):
                 if keys.has_attr('width'):
                     left_col_snapdeal.append(keys.text.strip().replace("\n",""))
                 else:
                        d=keys.text.strip()
                        k=d.replace(","," | ")
                        k=k.replace("\n","")
                        if k!=" ":
                              right_col_snapdeal.append(k)
            prdct.prod_specs_right=list(right_col_snapdeal)
            prdct.prod_specs_left=list(left_col_snapdeal)
           # print("RIGHT++++++>")
            # print(prdct.prod_specs_right)
            return (self.SnapdealDescription(prdct))

    def SnapdealDescription(self,prdct):

          try:
            descrip=self.Snapdeal_product_page_html.find('div',attrs={'itemprop':'description'})
            prdct.prod_description=descrip.text.strip().replace('\n','')
            return self.SnapdealHighlights(prdct)
          except:
            prdct.prod_description=''
            return self.SnapdealHighlights(prdct)

    def SnapdealHighlights(self,prdct):
          del self.highlights_snapdeal[:]
          try:
            for li in self.Snapdeal_product_page_html.findAll('li',attrs={'class':'col-xs-8 dtls-li'}):
                highlights_snapdeal.append(li.text.strip().replace('\n',''))
            prdct.prod_highlights=list(self.highlights_snapdeal)
            return self.AddCategorySnapdeal(prdct)

          except:
            prdct.prod_highlights='No Data Available'
            return self.AddCategorySnapdeal(prdct)

    def AddCategorySnapdeal(self,prdct):

          iq=0
          for (iq,category)in enumerate(self.Snapdeal_product_page_html.find_all('div',attrs={'class':'containerBreadcrumb'})):
                if(iq==1):
                      prdct.prod_First_Category=category.text.replace("\n","")
                elif(iq==2):
                      prdct.prod_Second_Category=category.text.replace("\n","")
                elif(iq==3):
                      prdct.prod_Third_Category=category.text.replace("\n","")
          print('Saving..')
          prdct.save()
          #return('Everything about new product added to database .')
          
          return (str(prdct.prod_name.encode("utf-8")))

    def URLforSnapdeal(self,productname):

          self.Snapdeal_title=productname
          self.Snapdeal_URL="https://www.snapdeal.com/search?keyword="
          title_items=[x for x in self.Snapdeal_title.split(" ")]
          result_url=""
          for i in title_items:
            if i!=title_items[-1]:
              if i=="(" or i==")":
                 continue
              else:
                 result_url+=(i+"%20")
            else:
                result_url+=i
          self.Snapdeal_URL+=result_url
          self.Snapdeal_URL+="&santizedKeyword=&catId=&categoryId=0"
          Snapdeal_response=requests.get(self.Snapdeal_URL)
          self.Snapdeal_page_html=soup(Snapdeal_response.content,"lxml")
          self.Snapdeal_page_html.prettify
          return self.RelatedSnapdeal(self.Snapdeal_URL)

    def RelatedSnapdeal(self,URL):

        del self.related_products_snapdeal_urls[:]
        for items in self.Snapdeal_page_html.find_all('div',attrs={'class':'product-desc-rating'}):
          item_url=items.find('a')
          self.related_products_snapdeal_urls.append(item_url['href'])
        print('Total Products Related To Snapdeal are= '+str(len(self.related_products_snapdeal_urls)))
        for j in range(len(self.related_products_snapdeal_urls)):
              if len(self.related_products_snapdeal_urls)>=40:
                  self.related_products_snapdeal_urls.pop()
              else:
                  return self.VisitProductPageSnapdeal(self.related_products_snapdeal_urls)

    def VisitProductPageSnapdeal(self,list_of_urls):

          n=0
          for url in list_of_urls:
                self.Snapdeal_data_set=Snapdeal()
                try:
                  response=requests.get(url)
                  html_prod_page=soup(response.content,'lxml')
                  prod_title=html_prod_page.find('h1',attrs={'itemprop':'name'})
                  prod_title=(prod_title.text.strip().replace('\n',''))
                  print(n)
                  n=n+1
                except:
                  continue
                print(self.CheckProductAvailabilitySnapdeal(prod_title,url))
          return 'All Snapdeal Related Products added'

    def UPDATESHOPCLUESPRODUCTS(self):
      #     Shopclues_products=Shopclue.objects.all()
          all_urls=[product.prod_URL for product in self.Shopclues_products]
          i=0
          del all_urls[0]
          for url in all_urls[0::]:
                print(i)
                print(self.StartAddingProductsShopclues(url))
                i=i+1
          return "All Added"

    def UPDATEAMAZONPRODUCTS(self):

          all_urls=[product.prod_URL for product in self.Amazon_products]
          i=0
          for url in all_urls[0::]:
                print(i)
                print(self.StartAddingProductsAmazon(url))
                print("Amazon Product Updated")
                i=i+1
          print("All Amazon Products Updated")
          return HttpResponse("<h1 Amazon products Updated </h1>")

# obj1=Index()

# print(obj1.URLforSnapdeal("bags"))
# www.flipkart.com/kuber-industries-stainless-steel-tea-kettle-hot-water-kettle-capacity-upto-16-cups-silver-jug/p/itmfa9awfvzhm9yz?pid=JUGFA98997D7YZFG&lid=LSTJUGFA98997D7YZFG0CNAZP&marketplace=FLIPKART&srno=s_1_2&otracker=search&otracker1=search&fm=SEARCH&iid=2282f374-0e8e-461a-b808-148fc32a9fcb.JUGFA98997D7YZFG.SEARCH&ppt=sp&ppn=sp&ssid=pkftffs37k0000001562999241090&qH=4b56240622699097"))
