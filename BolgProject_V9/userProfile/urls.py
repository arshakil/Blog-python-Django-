from django.urls import path,re_path
from . import views
urlpatterns = [
    path('',views.home, name='home'),
    path('signup',views.signup, name='signup'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    # edit user
    path('profile/edit/', views.editUserProfile, name='editProfile'),
    path('user-dashboard', views.userDashboard, name='user_dashboard'),
]
