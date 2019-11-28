from django.contrib import admin
from . models import Post, Category,Comment,Subscribe,Contact,Likes
# Register your models here.
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Subscribe)
admin.site.register(Contact)
admin.site.register(Likes)