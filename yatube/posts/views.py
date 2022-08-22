#from xml.etree.ElementTree import Comment
import re
from tkinter.messagebox import NO
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponse

from .models import Post, Group, User, Comment, Follow

from django.shortcuts import redirect
from .forms import PostForm, CommentForm

from django.contrib.auth.decorators import login_required

from django.views.decorators.cache import cache_page

# @cache_page(20, key_prefix='index_page')
def index(request):
    post_list = Post.objects.order_by('-pub_date').all()
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    
    return render(
        request, 
        "index.html", 
        {'page': page, 'paginator': paginator} 
    )   



# view-функция для страницы сообщества
def group_posts(request, slug):

    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by("-pub_date").all()
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, "group.html", {"group": group, "page": page, 'paginator': paginator})

# view-функция для добавления новой записи 
@login_required
def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, files=request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("index")
        return render(request,"new_post.html", {"form":form})
    form = PostForm(files=request.FILES or None)
    return render(request, 'new_post.html', {'form':form})

@login_required
def post_edit(request, username, post_id):
        # тут тело функции.
        # текущий пользователь — это автор записи.
       
        if username != request.user.username:
            return redirect('post', username = username, post_id = post_id)
        post = get_object_or_404(Post, author__username = username, id = post_id )
        form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
        if request.method == 'POST':
            if form.is_valid():
                form.save()
                return redirect('post', username = username, post_id = post_id)
        return render(request, 'new_post.html', {'form':form, 'post':post})


def profile(request, username):
        # тут тело функции
        following = None
        user = User.objects.get(username=username)
        post_list = user.posts.all()
        paginator = Paginator(post_list, 10) 
        page_number = request.GET.get('page')  
        page = paginator.get_page(page_number) 
        if request.user.is_authenticated == True:
            if user.following.filter(user = request.user):
                following = True
            else:
                following = False

        return render(request, 'profile.html', {'current_user':user, "page": page, 'paginator': paginator, 'following':following})
 
 
def post_view(request, username, post_id):
        # тут тело функции
        post = get_object_or_404(Post, author__username = username, id = post_id)
        form = CommentForm()
        return render(request, 'post.html', {'post':post,  'form': form})

def add_comment(request, username, post_id):
    post = get_object_or_404(Post, author__username = username, id = post_id)
    user = User.objects.get(username=username)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
        return redirect('post', username = username, post_id = post_id)
    return render(request, 'post.html', {'current_user':user,'form': form, 'post': post} )

@login_required
def profile_follow(request, username):
    author = User.objects.get(username = username)    
    Follow.objects.create(user = request.user, author = author)
    return redirect('profile', username = username)

@login_required
def profile_unfollow(request, username):
    author = User.objects.get(username = username)
    Follow.objects.filter(user = request.user, author = author).delete()
    return redirect('profile', username = username)

@login_required
def follow_index(request):
    following = request.user.follower.all().values_list('author')
    post_list = Post.objects.filter(author__in=following)
    
    paginator = Paginator(post_list, 10)  # показывать по 10 записей на странице.
    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением
    
    return render(
        request, 
        "follow.html", 
        {'page': page, 'paginator': paginator} 
    )   


def page_not_found(request, exception):
    # Переменная exception содержит отладочную информацию, 
    # выводить её в шаблон пользователской страницы 404 мы не станем
    return render(
        request, 
        "misc/404.html", 
        {"path": request.path}, 
        status=404
    )


def server_error(request):
    return render(request, "misc/500.html", status=500)