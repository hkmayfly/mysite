from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models


class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model):
    title = models.CharField(max_length=30)
    # content = models.TextField()
    # content = RichTextField()
    content = RichTextUploadingField()
    blog_type = models.ForeignKey(BlogType, on_delete=models.DO_NOTHING)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    reader_num = models.PositiveIntegerField(default=0)
    pub_time = models.DateTimeField(auto_now=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "<Blog:%s>" % self.title

    class Meta:
        ordering = ['-pub_time']

    def increase_reader_num(self):
        self.reader_num += 1
        # 指定更新reader_num防止全部更新，文章变成最新文章
        self.save(update_fields=['reader_num'])


# class Note(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     pub_date = models.DateTimeField()
#     title = models.CharField(max_length=200)
#     body = models.TextField()
#
#     def __str__(self):
#         return self.title