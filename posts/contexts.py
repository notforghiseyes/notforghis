from .models import Post


def all_tags(request):
    posts = Post.objects.all()
    
    tags = []
    all_tags = []
    
    for post in posts:
        
        all_tags.append(post.tag)
        
    for tag in all_tags:
       if tag:
           
           tags += tag.split(' ')
            
    
    return {'tags' : set(tags)}
    
    
def all_authors(request):
    posts = Post.objects.all()
    
    authors = set()
    
    for post in posts:
        authors.add(post.author)
    
    return {'authors': authors}
    