from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import BlogPostForm
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.functions import Lower
import json



# Create your views here.
def posts_list(request):
    posts = Post.objects.all()
    
    
    posts = paginator(request, posts)
    query_string = request.GET.urlencode()
    
    return render(request, "posts/posts_list.html", {"posts":posts, "query_string": query_string})
    
    
    

def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    posts = Post.objects.all()
    post.views += 1
    post.save()
    
    
    return render(request, "posts/post_detail.html", {"post": post})
    
    
def edit_post(request, id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=id)
        form = BlogPostForm(request.POST, request.FILES, instance=post) 
        
        if form.is_valid():
            form.save()
            
        return redirect("go_to_post", id=id)
        
        
    else:    
        post = get_object_or_404(Post, pk=id)
        form = BlogPostForm(instance=post) 
        return render(request, "posts/post_form.html", {"form":form})
    
    
    
def post_form(request):
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect("home") 
    
    else:
        form = BlogPostForm()
        
    return render(request, "posts/post_form.html", {"form":form})
        
        
def about(request):
    return render(request, "posts/about.html")
    
    
def show_by_tag(request, tag_name):
    posts = Post.objects.filter(tag__contains=tag_name)
    
    posts = paginator(request, posts)
    
    
    return render(request, "posts/posts_list.html", {"posts":posts})


def show_user_profile(request, user):
    user = request.user
    
    return render(request, "posts/user_profile.html")
   
    
def show_by_author(request, author):
    author = get_object_or_404(User, username=author)
    
    posts = author.posts.all()
    posts = paginator(request, posts)
    
    return render(request, "posts/posts_list.html", {"posts": posts})
    

# def author_sorted_by_field(request, author, field):
#     author = get_object_or_404(User, username=author)
#     posts = Post.objects.all().order_by('-likes_count')
    
    
#     posts = paginator(request, posts)
    
#     return render(request, "posts/posts_list.html", {"posts":posts})


    
def search_posts(request):
    query = request.GET['s']
    
    query_by_title = Q(title__contains=query)
    query_by_content = Q(content__contains=query)
    posts = Post.objects.filter(query_by_title | query_by_content)
    
    posts = paginator(request, posts)
    
    return render(request, "posts/posts_list.html", {"posts":posts})
    
    
def show_by_liked(request):
    posts = request.user.liked_posts.all()
   
    return render(request, "posts/posts_list.html", {"posts":posts})  
    
    
    
def search_month(request):
    
    query = request.GET['m']
    posts = Post.objects.filter(published_date__month=query)
    
    posts = paginator(request, posts)
    
    if posts:
        return render(request, "posts/posts_list.html", {"posts":posts})
    else:
        return render(request, "posts/search-no-posts.html")
        
    

def search_year(request):
    
    query = request.GET['y']
    posts = Post.objects.filter(published_date__year=query)
    
    posts = paginator(request, posts)
    
    if posts:
        return render(request, "posts/posts_list.html", {"posts":posts})
    else:
        return render(request, "posts/search-no-posts.html")
        
        
def order_by_title(request):
    posts = Post.objects.all().order_by(Lower('title'))
    
    posts = paginator(request, posts)
    
    return render(request, "posts/posts_list.html", {"posts":posts})
    
    
def order_by_views(request):
    posts = Post.objects.all().order_by('-views')
    
    posts = paginator(request, posts)
    
    return render(request, "posts/posts_list.html", {"posts":posts})
    
    
def order_by_date(request):
    posts = Post.objects.all().order_by('-published_date')

    posts = paginator(request, posts)
    
    return render(request, "posts/posts_list.html", {"posts":posts})
    
    
def order_by_likes(request):
    path = request.path
    
    print("--------------------")
    print(path)
    
    
    posts = Post.objects.all().order_by('-likes_count')
    
    
    posts = paginator(request, posts)
    
    return render(request, "posts/posts_list.html", {"posts":posts})
    
    
def like_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.likes.add(request.user)
    post.likes_count += 1
    post.save()
    
    return redirect('home')
  
    
def liked_post(request, id):
    post = get_object_or_404(Post, pk=id)
    post.likes.remove(request.user)
    post.likes_count -= 1
    post.save()
    # resp = {'id': id}
    # return json.dumps(resp)
    
    return redirect('home')
    
    
def paginator(request, posts):
    paginator = Paginator(posts, 9)
    page = request.GET.get('page')
    
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return posts

    

    