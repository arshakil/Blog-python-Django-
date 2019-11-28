from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# new
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import SignupForm,UserProfileForm,UserForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.mail import EmailMessage
from blog.models import Post,Comment,Category


# Create your views here.
def home(request):
    return render(request, 'userProfile/home.html')




# For signUp.
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('userProfile/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'userProfile/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def editUserProfile(request):
    if request.method == "POST":
        userform = UserForm(request.POST or None, instance=request.user)
        userProfile = UserProfileForm(request.POST or None, instance=request.user.profile, files=request.FILES)
        if userform.is_valid() and userProfile.is_valid():
            userform.save()
            userProfile.save()
            return redirect("/")
    else:
        userform = UserForm(instance=request.user)
        userProfile = UserProfileForm(instance=request.user.profile, files=request.FILES)
    context = {
        'userform':userform,
        'userProfile':userProfile,
    }
    return render(request, 'userProfile/edituser.html',context)

    
def userDashboard(request):
    posts = Post.objects.filter(author__username=request.user.username)
    # for pagination
    paginator = Paginator(posts, 2)
    page = request.GET.get('page')
    # Handle out of range and invalid page numbers:
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    print('post are',posts)
    context = {
        'posts':posts
    }


    return render(request,'userProfile/dashboard.html',context)