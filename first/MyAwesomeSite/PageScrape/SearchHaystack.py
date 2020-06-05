# import datetime
# from PageScrape.models import Amazon,Shopclue,Shopclues,Snapdeal
# from haystack import indexes
# #
# class ArticleIndex(indexes.SearchIndex,indexes.Indexable):

#     p_name=indexes.CharField(document=True,use_templates=True)

#     content_auto=indexes.EdgeNgramField(model_attr='prod_name')

#     def get_model(self):
#         return Amazon

#     def index_queryset(self, using=None):
#         return self.get_model().objects.all()