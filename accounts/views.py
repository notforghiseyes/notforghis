from django.shortcuts import render
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .forms import ProfileRegistrationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        profile_form = ProfileRegistrationForm(request.POST, request.FILES)
        
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            
            print("*****************")
            print(profile.image)
            
            if profile.image == "avatars/if_female1_403023.svg":
                if profile.gender == "M":
                    profile.image = "avatars/if_male3_403019.svg"

            profile.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
        profile_form = ProfileRegistrationForm()
    return render(request, 'accounts/register.html', {'form': form, 'profile_form': profile_form})
    
    
def edit_profile(request, id):
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
