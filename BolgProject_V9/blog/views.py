from django.shortcuts import render, get_object_or_404,redirect
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from . models import Post,Category,Comment,Subscribe,Contact,Likes
from .forms import CommentForm,PostCreateForm
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from taggit.models import Tag

# Create your views here.
def home(request,tag_slug=None, get_month=None, get_year=None, id=None):
    categories = Category.objects.all().annotate(posts_count=Count('post'))
    latest_posts = Post.objects.order_by('-post_uploaded')[:4]
    posts = Post.objects.all()


    # print('All tags are ::: ', list(Tag.objects.all().values()))
    unique_tag = [] 
    for x in list(Tag.objects.all().values()[:20]):
        if x not in unique_tag: 
            unique_tag.append(x)



    # user_posts = Post.objects.filter(author=request.user)
    # user_commented = Comment.objects.filter(user=request.user).count()
    # print('user posted',user_posts)
    # print('user Commented',user_commented)
   
    # for search
    qs = request.POST.get('q',)
    if qs:
        posts = Post.objects.filter(title__icontains=qs)

    if get_month and get_year:
        posts = Post.objects.filter(post_uploaded__month=get_month,post_uploaded__year=get_year)
    
# for tags
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
# for pagination
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')
    # Handle out of range and invalid page numbers:
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {
        'categories':categories,
        'posts':posts,
        'all_posts': Post.objects.order_by('post_uploaded'),
        'latest_posts':latest_posts,
        'tag': tag,
        'unique_tag':unique_tag
        # 'user_posts':user_posts
    }
    return render(request, 'blog/index.html',context)

def about(request): 
    categories = Category.objects.all()
    context = { 
        'categories':categories,
    }
    return render(request, 'blog/about.html',context)
def contact(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        name = request.POST.get('name',)
        email = request.POST.get('email',)
        subject = request.POST.get('subject',)
        message = request.POST.get('message',)
        contact = Contact(name=name, email=email, subject=subject, message=message)
        contact.save()
        return redirect('home')

    context = {  
        'categories':categories, 
    }
    return render(request, 'blog/contact.html',context)



def categories_page(request,id):
    categories = Category.objects.all()

    # cat = get_object_or_404(Category, id=id)
    # posts = Post.objects.filter(category=cat)

# or
    posts = Post.objects.filter(category__id=id)
    cat_name = get_object_or_404(Category, id=id)
    print('category name is :',cat_name)
    
    paginator = Paginator(posts, 5)
    page = request.GET.get('page')

    # Handle out of range and invalid page numbers:
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {  
        'posts':posts,
        'categories':categories,
        'active':cat_name,
    }
    return render(request, 'blog/categories.html',context)

def detail_page(request, id):
    post = get_object_or_404(Post, id=id)
    categories = Category.objects.all().annotate(posts_count=Count('post'))
    latest_posts = Post.objects.order_by('-post_uploaded')[:4]
    all_posts_month_year = Post.objects.order_by('post_uploaded')[:12]

   
    # for tags
    unique_tag = [] 
    for x in list(Tag.objects.all().values()[:20]):
        if x not in unique_tag: 
            unique_tag.append(x)


# for comments
    comments = Comment.objects.filter(post=post, reply=None)
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.user = request.user

            reply_id =request.POST.get('comment_id')
            comment_qs = None
            if reply_id:
                comment_qs = Comment.objects.get(id=reply_id)
                comment.reply = comment_qs
            comment.save()
            return redirect('detail_page', post.id)
    else:
        form = CommentForm()

    context = {  
        'categories':categories,
        'post':post,
        'latest_posts':latest_posts,
        'form':form,
        'comments':comments,
        'all_posts_month_year': all_posts_month_year,
        'unique_tag':unique_tag,
    }
    return render(request, 'blog/single.html',context)

def subscribe(request):
    qs = request.POST.get('q')
    subscribe = Subscribe(email=qs)
    subscribe.save()
    return redirect('home')

def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, files=request.FILES)
        if form.is_valid():
            post_form=form.save(commit=False)
            post_form.author = request.user
            post_form.save()

            #for tag save
            form.save_m2m()
            return redirect('home')
    else:
        form = PostCreateForm()
    context={
        'form':form
    }
    return render(request,'blog/create_post.html',context)
#delete 
def delete_post(request, id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    #tags delete
    Tag.objects.filter(post=None).delete()
    return redirect('home')
    
def update_post(request, id):
    instance = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostCreateForm(request.POST, instance=instance)
        if form.is_valid():
            tag_data = form.cleaned_data["tags"]
            post_form=form.save(commit=False)
            post_form.author = request.user
            instance.tags.clear()
            for x in tag_data:
                post_form.tags.add(x)
            post_form.save();
            return redirect('home')
    else:
        form = PostCreateForm(instance=instance)
    context={
        'form':form
    }
    return render(request,'blog/create_post.html',context)





#like posts 
def like_post(request,id):
    user = []
    post = get_object_or_404(Post, id=id)
    if Likes.objects.filter(post__id=id).exists():
        user = request.user
        all_likes = Likes.objects.get(post__id=id)
        all_likes.like_status = True
    else:
        like_title = Likes(post=post)
        like_title.save()
    if user.is_authenticated:
            if user in all_likes.user_likes.all():
                all_likes.user_likes.remove(user)
                all_likes.like_status = False
                all_likes.save()
                return redirect('detail_page', post.id)
            else:
                all_likes.user_likes.add(user)
                all_likes.like_status = True
                all_likes.save()
                return redirect('detail_page', post.id)
    return redirect('detail_page')

def remove_all_tags_without_objects():
    for tag in Tag.objects.all():
        if tag.taggit_taggeditem_items.count() == 0:
            print('Removing: {}'.format(tag))
            tag.delete()
        else:
            print('Keeping: {}'.format(tag))