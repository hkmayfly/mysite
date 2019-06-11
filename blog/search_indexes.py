# import datetime
# from haystack import indexes
# from blog.models import Blog
#
#
# class NoteIndex(indexes.SearchIndex, indexes.Indexable):
#     text = indexes.CharField(document=True, use_template=True)
#
#     author = indexes.CharField(model_attr='author')
#     pub_date = indexes.DateTimeField(model_attr='pub_time')
#
#     def get_model(self):
#         return Blog
#
#     def index_queryset(self, using=None):
#         """Used when the entire index for model is updated."""
#         return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
