from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post
from django.core.files.storage import FileSystemStorage

posts =[ 
    {
    'text' : 'Hi, this is the 1st post',
    'author' : 'Rupok'
    },
    {
    'text' : 'Hi, this is the 2st post',
    'author' : 'Hasibul'
    },
]

# Create your views here.
# login_required is a anotation, and for this, we need to add a LOGIN_URL at the settings.py, if not logged in then where it will redirect 

@login_required
def home(request):
    # return HttpResponse('<h1>Welcome to home page </h1>')
    Context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'html/home.html', Context)

@login_required
def about(request):
    Context = {
        'author' : request.user
    }
    return render(request, 'html/about.html', Context)

def about2(request, name):
    # **************** i can also apply conditional statement here bease on 'name' ***************
    Context = {
        'name' : name
    }
    return render(request, 'html/about2.html', Context)

def singin(request):
    # we use this single function for both GET and POST request
    # GET is when loading the login page, POST is when press the submit button

    if(request.method == 'GET'):
        return render(request, 'html/login.html')
    elif(request.method == 'POST'):
        u = request.POST.get('username', '') #Default Value is ''
        p = request.POST.get('password', '')

        response = authenticate(username=u, password=p)
        if(response is None):
            return HttpResponse("<h1> Wrong Credentials </h1>")
        else:
            login(request, response)
            return redirect('blog-home')
        
def signOut(request):
    logout(request)
    return redirect('blog-login')

@login_required
def post(request):
    if(request.method == 'GET'):
        return render(request, 'html/post.html')
    elif(request.method == 'POST'):
        title = request.POST.get('title', '')
        text = request.POST.get('text', '')
        image = request.FILES.get('post_image', '')

        author = request.user
        post = Post(title = title, text = text, author = author, post_image = image)
        post.save()

        return redirect('blog-home')
    
@login_required
def delete(request, id):
    post = Post.objects.get(id = id)

    # Delete the associated image file
    if post.post_image:
        fs = FileSystemStorage()
        fs.delete(post.post_image.path)

    post.delete()
    return redirect('blog-home')


@login_required
def edit(request, id):
    p = Post.objects.get(id = id)
    if(request.method == 'GET'):
        Context = {
            'post' : p
        }
        return render(request, 'html/edit.html', Context)
    elif(request.method == 'POST'):
        p.title = request.POST.get('title', '')
        p.text = request.POST.get('text', '')

        p.save()

        return redirect('blog-home')
    
# Fetch All Post by API ===> http://127.0.0.1:8000/blog/allPost
def allPost(request):

    posts =  list(Post.objects.all().values())

    # Default safe is True, which expect a Dictionary type data(posts), if safe is False, it works with any datatype
    return JsonResponse(posts, safe=False)
# Here our API is working with the link, so we can use this API to fetch data from django database and we can code on another language to show the data to the on the web-page, we do not need any http response from backend of django, we can use the Django only a backend server now by the help of the API, it ensures LoseCouppling