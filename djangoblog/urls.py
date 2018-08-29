"""djangoblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path, include
from posts.views import posts_list, post_detail, post_form, about, show_by_tag, search_posts, search_month, search_year, edit_post, show_by_author, order_by_title, order_by_views, order_by_date, order_by_likes, like_post, liked_post, show_by_liked, show_user_profile
from django.views.static import serve
from accounts.views import register
from django.conf import settings
from django.urls import reverse_lazy
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete
from django.conf.urls import url

urlpatterns = [
    
    #----------------- POST APP --------------------------------
    
    path('admin/', admin.site.urls),
    path('', posts_list, name='home'),
    path('', posts_list, name='post_list'),
    path('blog/item/<int:id>', post_detail, name='go_to_post'),
    path('blog/item/<int:id>/edit', edit_post, name='edit_post'),
    path('post/add', post_form, name='add'),
    path('about', about, name='about'),
    path('filter/<tag_name>', show_by_tag, name='show_by_tag'),
    path('search/item', search_posts, name='search'),
    path('media/<path:path>', serve, {'document_root': settings.MEDIA_ROOT}),
    path('search/month', search_month, name='search_month'),
    path('search/year', search_year, name='search_year'),
    # path('author/<author>sorted/<field>', author_sorted_by_field, name="author_sorted_by_field"),
    path('author/<author>', show_by_author, name="show_by_author"),
    path('liked/posts', show_by_liked, name="show_by_liked"),
    path('sorted/title', order_by_title, name="order_by_title"),
    path('sorted/views', order_by_views, name="order_by_views"),
    path('sorted/date', order_by_date, name="order_by_date"),
    path('sorted/likes', order_by_likes, name="order_by_likes"),
    path('like/<int:id>', like_post, name="like"),
    path('liked/<int:id>', liked_post, name="liked"),
    path('profile/<user>', show_user_profile, name='profile'),
    
    
    
    
    #---------------- Accounts App --------------------------------
    
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', register, name='register'),
    path('accounts/password-reset/', password_reset,{'post_reset_redirect': reverse_lazy('password_reset_done')}, name='password_reset'),
    path('accounts/password-reset/done/', password_reset_done, name='password_reset_done'),
    url(r'^(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm,{'post_reset_redirect': reverse_lazy('password_reset_complete')}, name='password_reset_confirm'),
    path('accounts/password-reset/complete/', password_reset_complete, name='password_reset_complete'),
]
