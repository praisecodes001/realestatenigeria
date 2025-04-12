from django.conf import settings
from django.conf.urls.static import static
from .forms import PostForm, CreateUserForm,ProfileUpdateForm
from django.shortcuts import render,  get_object_or_404 , redirect
from .models import Post, Profile,SubscriptionPlan,UserSubscription
import requests
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .paystack import initialize_payment
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import timedelta,datetime



# Create your views here.
def home(request):
    
    return render(request, 'estateapp/home.html')


paystack_secret_key = settings.PAYSTACK_SECRET_KEY

def sign_upPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)

                return redirect('login')

        context = {'form': form}
        return render(request, 'estateapp/signup.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password =request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.info(request, 'Username OR Password is incorrect')

        context = {}
        return render(request, 'estateapp/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')



def post_create(request):
    if request.method == 'POST':
           
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user
                post.save()
                return redirect('personal')
    else:
        form = PostForm()
    return render(request, 'estateapp/pro.html', {'form': form})




def Listings(request):
    posts = []
    for post in Post.objects.all():  

   
        post = {
            'title': post.title,
            'short': post.short,
            'building': post.building,  
            'category': post.category,
            'bedroom': post.bedroom,
            'bathroom': post.bathroom,
            'toilet': post.toilet,
            'currencyfield': post.currencyfield,
            'totalarea': post.totalarea,
            'coveredarea': post.coveredarea,
            'thumb': post.images.url,
            'author': post.author,
            'contact_methods': [

                {'name': 'Whatsapp', 'icon':'fa-brands fa-whatsapp','link': 'https://wa.me/{profile.phone}'},
                {'name': 'Phone', 'icon':'fa-solid fa-phone','link': 'tel: {profile.phone}' },
                {'name': 'Telegram', 'icon':'fa-brands fa-telegram','link': 'tel: {profile.telegram}' },
                {'name': 'Instagram', 'icon':'fa-brands fa-instagram','link': 'tel: {profile.instagram}' },
                ]
        }
        

    context = {
        'posts': post,  
    }

    return render(request, 'estateapp/Listings.html', context)

def contact(request):

    return render(request, 'estateapp/contact.html')

def contact_agent(request):

    return render(request, 'estateapp/contactagent.html')

def save (request):        
    
    return render(request, 'estateapp/done.htm')


def House(request):
    
    return render(request, 'estateapp/House.html')

@login_required(login_url='login')
def post_create(request):
   
   if request.method == 'POST':
      form = PostForm(request.POST, request.FILES)

      author = request.user


      title = request.POST['title']
      short = request.POST['short']
      category = request.POST['category']
      building = request.POST['building']
      subtype = request.POST['subtype']
      bedroom = request.POST['bedroom']
      bathroom = request.POST['bathroom']
      toilet = request.POST['toilet']
      area = request.POST['area']
      state = request.POST['state']
      availability = request.POST['availability']
      totalarea = request.POST['totalarea']
      coveredarea = request.POST['coveredarea']
      description = request.POST['description']
      
      thumb = request.FILES['thumb']
      secondary = request.FILES['image1']
      secondary_2 = request.FILES['image2']
      secondary_3 = request.FILES['image3']
      secondary_4 = request.FILES['image4']
      secondary_5 = request.FILES['image5']
      secondary_6 = request.FILES['image6']
     
      currencyfield =  request.POST['currencyfield']
      url = request.POST['url']
      

      my= Post(title=title, category=category, building=building,
                           subtype=subtype, bedroom=bedroom, toilet=toilet,
                           area=area, state=state, availability=availability,
                           totalarea=totalarea, coveredarea=coveredarea,
                           description=description,author=author, 
                           thumb=thumb, secondary=secondary, secondary_2=secondary_2, 
                           secondary_3=secondary_3, secondary_4=secondary_4, secondary_5=secondary_5, secondary_6=secondary_6,
                           bathroom=bathroom, short=short,
                           currencyfield=currencyfield, url=url)      
      my.save()

      return render(request,"estateapp/done.htm")
     
   else:

      return render(request,"estateapp/pro.html")


class PostListView(ListView):
    model = Post
    template_name = 'estateapp/Listings.html'
    context_object_name = 'posts'
    ordering = ['?']


class PostDetailView(DetailView):
    model = Post



def registration_path(request):

    return render(request, 'estateapp/registration-path.html')

@login_required(login_url='login')
def dashboard(request):
   
    return render(request, 'estateapp/dashboard.html')

@login_required(login_url='login')
# def profile(request):
   # if request.method == 'POST':
      # form = ProfileUpdateForm(request.POST, request.FILES)

      # fname = request.POST['fname']
      # cname = request.POST['cname']
      # username = request.POST['username']
      # office = request.POST['office']
      # phone = request.POST['phone']
      # email = request.POST['email']
      # insta = request.POST['insta']
      # telegram = request.POST['telegram']
      # profile_picture = request.FILES['profile_picture']
      # my= Profile(fname=fname, cname=cname, username=username, office=office, phone=phone, email=email, insta=insta, telegram=telegram, profile_picture=profile_picture,)      
    
      # my.save()
      
      # return render(request,"estateapp/done.htm")
     
   # else:
    
    # return render(request, 'estateapp/profile.html')


@login_required(login_url='login')
def personal(request):
    posts = Post.objects.filter(author=request.user)

    
    return render(request, 'estateapp/personal.html', {'posts': posts})

def results(request):
    if request.method == "POST":
        subtype = request.POST['subtype']
        area = request.POST['area']
        state = request.POST['state']
        building = request.POST['building']
        currencyfield = request.POST['currencyfield']

        post = Post.objects.filter(building__contains= building)
        return render (request, 'estateapp/results.html')

    else:
        return render (request, 'estateapp/results.html')




def search_results(request):
    subtype = request.GET.get("subtype", "")
    area = request.GET.get("area", "")
    state = request.GET.get("state", "")
    category = request.GET.get("category", "")
    max_budget = request.GET.get("max_budget", "")

    posts = Post.objects.all()

    if subtype:
        posts = posts.filter(subtype__icontains=subtype)

    if area:
        posts = posts.filter(area__icontains=area)

    if state:
        posts = posts.filter(state__icontains=state)

    if category:
        posts = posts.filter(category__icontains=category)

    if max_budget:
        try:
            max_budget = float(max_budget)
            posts = posts.filter(max_budget__lte=max_budget)
        except ValueError:
            pass  # Ignore invalid budget input

    context = {
        "posts": posts,
        "subtype": subtype,
        "area": area,
        "state": state,
        "category": category,
        "max_budget": max_budget,
    }

    return render(request, "estateapp/results.html", context)
@login_required(login_url='login')
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
                post.save()
                return redirect('personal')
    else:
        form = PostForm(instance=post)
    return render(request, "estateapp/post_edit.html", {'form': form})

@login_required(login_url='login')
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('personal')
    return render(request, 'estateapp/post_delete.html', {'post': post})


@login_required(login_url= 'login')
def profile_update(request):
   
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        profile.fname = request.POST.get('fname')
        profile.cname = request.POST.get('cname')
        profile.office = request.POST.get('office')
        profile.phone = request.POST.get('phone')
        profile.insta = request.POST.get('insta')
        profile.telegram = request.POST.get('telegram')

        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']

        profile.save()
        return redirect('profile_update')  # Stay on the same page after saving

    return render(request, 'estateapp/profile.html')

def howitworks(request):

    return render(request, 'estateapp/howitworks.html')  


PLANS = [
    {
        "id": "free",
        "name": "Free",
        "price": 0,
        "duration": "1 month",
        "features": [
            "Post 5 Properties",
            "Get 6hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to different clients and owners",
            "Not allowed to post Sales, short-let listings",
            "Not allowed to post properties above N100,000",
        ],
    },
    {
        "id": "beginner",
        "name": "Beginner",
        "price": 10000,
        "duration": "1 month",
        "features": [
            "Post 15 Properties",
            "Get 8hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to different clients and owners",
            "Not allowed to post Sales, short-let listings",
            "Not allowed to post properties above N500,000",
        ],
    },
    {
        "id": "amateur",
        "name": "Amateur",
        "price": 18500,
        "duration": "1 month",
        "features": [
            "Post 25 Properties",
            "Get 10hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to different clients and owners",
            "Not allowed to post sale listings",
            "Not allowed to post properties above N2,000,000",
        ],
    },
    {
        "id": "advanced",
        "name": "Advanced",
        "price": 25000,
        "duration": "1 month",
        "features": [
            "Post 35 Properties",
            "Get 16hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to different clients and owners",
            "Allowed to post short-let, rent listings",
            "Not allowed to post properties above N5,000,000",
        ],
    },
    {
        "id": "business",
        "name": "Business",
        "price": 32000,
        "duration": "1 month",
        "features": [
            "Post 45 Properties",
            "Get 20hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to different clients and owners",
            "Allowed to post short-let, rent listings",
            "Not allowed to post properties above N10,000,000",
        ],
    },
    {
        "id": "professional",
        "name": "Professional",
        "price": 41500,
        "duration": "1 month",
        "features": [
            "Post 55 Properties",
            "Get 23hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to different clients and owners",
            "Allowed to post Sales, short-let, rent listings",
            "Allowed to post properties above N50,000,000",
        ],
    },
    {
        "id": "top_level",
        "name": "Top Level",
        "price": 55000,
        "duration": "1 month",
        "features": [
            "Post 100 Properties",
            "Get 24hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to different clients and owners",
            "Allowed to post Sales, short-let, rent listings",
            "Allowed to post properties above N100,000,000",
        ],
    },
    {
        "id": "platinum",
        "name": "Platinum",
        "price": 110000,
        "duration": "1 month",
        "features": [
            "Unlimited Posts",
            "Get 24hrs calls from prospective clients",
            "24hrs Customer services",
            "Access to unlimited clients and owners",
            "Allowed to post Sales, short-let, rent listings",
            "Unlimited property prices",
        ],
    },
]


@login_required
def subscription(request):
    user_subscription = UserSubscription.objects.filter(user=request.user).first()
    return render(request, "estateapp/subscription.html", {"user_subscription": user_subscription,"plans": PLANS})


@login_required
def process_payment(request):
    if request.method == "POST":
        plan_id = request.POST.get("plan")
        selected_plan = next((plan for plan in PLANS if plan["id"] == plan_id), None)

        if not selected_plan:
            return redirect("subscription")

        # Handle Paystack payment
        response = initialize_payment(request.user, selected_plan["price"], selected_plan["name"])

        if response["status"]:
            return redirect(response["data"]["authorization_url"])  # Redirect to Paystack payment page

    return redirect("subscription") 

def verify_payment(request):
    reference = request.GET.get("reference")
    url = "https://api.paystack.co/transaction/verify/{reference}"
    headers = {"Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"}

    response = requests.get(url, headers=headers)
    data = response.json()

    if data["status"] and data["data"]["status"] == "success":
        user = request.user
        amount = data["data"]["amount"] / 100  # Convert from kobo
        plan_name = data["data"]["metadata"]["plan"]

        # Save payment record
        UserSubscription.objects.create(
            user=user,
            plan=plan_name,
            amount=amount,
            paystack_reference=reference,
            status="success",
        )

        # Update Subscription
        subscription, _ = SubscriptionPlan.objects.get_or_create(user=user)
        subscription.plan = plan_name
        subscription.start_date = datetime.now()
        subscription.end_date = datetime.now() + timedelta(days=30)
        subscription.is_active = True
        subscription.save()

        return redirect("payment_history")

    return redirect("subscription")


@login_required
def payment_history(request):

    payments = Payment.objects.filter(user=request.user).order_by("-date")
    return render(request, "estateapp/payment_history.html", {"payments": payments})    