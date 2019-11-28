from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('/<int:id>/',views.home, name='likes_redirect'),
    path('tag/<str:tag_slug>/',views.home, name='post_list_by_tag'),
    path('post_archive_month_year/<str:get_month>/<str:get_year>/',views.home, name='post_archive_month_year'),
    path('subscribe/', views.subscribe, name='subscribe'),
    
    

    path('about/',views.about, name='about'),
    path('contact/',views.contact, name='contact'),
    path('categories_page/<int:id>/',views.categories_page, name='categories_page'),
    path('detail_page/<int:id>/',views.detail_page, name='detail_page'),

    # post
    path('create_post/', views.create_post, name='create_post'),
    path('update_post/<int:id>/', views.update_post, name='update_post'),
    path('delete_post/<int:id>/', views.delete_post, name='delete_post'),

    #likes
    path('like_post/<int:id>/',views.like_post, name='like_post'),

]
