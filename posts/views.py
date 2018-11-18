from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post
from .forms import BlogPostForm
  
def get_posts(request):
    """
    Create a view that will return a list of posts
    and render it using the blogposts.html template.
    """
    posts = Post.objects.filter(published_date_lt_lte=timezone.now().order_by('-published_date'))
    return render(request, "blogposts.html", {'posts':posts})
    
def post_details(request, pk):
    """
    Create a view of a single post according to an id (pk)
    and render it using the postdetails.html template.
    """
    post = get_object_or_404(Post, pk=pk)
    post.views+=1
    post.save()
    return render(request, "postdetails.html", {'post':post})
    
def create_or_edit_post(request, pk=None):
    """
    A view that allows the creation or edition of a post if id(pk) is not None
    """
    post = get_object_or_404(Post, pk=pk) if pk else None
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post= form.save()
            return redirect(post_details, post.pk)
        else:
            form = BlogPostForm(instance=post)
        return render(request, "blogpostform.html", {'form':form})