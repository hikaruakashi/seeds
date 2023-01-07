from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Post,Topic,User
from django.contrib.auth import authenticate,login,logout
from .forms import PostForm,RegisterUserForm
from django.db.models import Q
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.forms import UserCreationForm


# Create your views here.

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
           user = User.objects.get(username=username)
        except:
            messages.error(request,'ユーザー名が違います')

        user = authenticate(request,username=username,password=password)

        if user  is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'ユーザー名またはパスワードが違います')

    context = {'page':page}
    return render(request,'app/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage (request):
    form = RegisterUserForm()
    
    if request.method == 'POST':
        try:
            form = RegisterUserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect('home')
        except Exception as e:
            print(e)
            raise

    context = {
        'form': form
    }
    return render(request,'app/login_register.html', context)


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    #タグ検索をする
    posts = Post.objects.filter(
        Q(topic__name__icontains=q) |
        Q(description__icontains=q) |
        Q(title__icontains=q)
        )

    topics = Topic.objects.all()
    context = {'posts':posts,'topics':topics}
    return render(request, 'app/home.html',context)


def post(request,pk):
    post = Post.objects.get(id=pk)
    context = {'post':post}
    return render(request,'app/post.html',context)


def userProfile(request,pk):
    user = User.objects.get(id=pk)
    posts = user.post_set.all()
    # topics = Topic.objects.all()
    
    context ={'user':user,'posts':posts,}
    return render(request,'app/profile.html',context)


#ログインしていないとlogin.htmlに飛ばされる
#ポストを制作
@login_required(login_url='login')
def createPost(request):

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            #除外する関数
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'app/create_post.html',context)


@login_required(login_url='login')
def updatePost(request,pk):
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.user != post.author:
        return HttpResponse('あなたは所有者ではありません')

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    context = {'form':form}
    return render(request,'app/create_post.html',context)


@login_required(login_url='login')
def deletePost(request,pk):
    post = Post.objects.get(id=pk)

    if request.user != post.author:
        return HttpResponse('あなたは所有者ではありません')

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request,'app/delete_post.html',{'obj':post})