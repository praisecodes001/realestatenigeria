from django.conf import settings
from django.conf.urls.static import static
from .forms import PostForm, CreateUserForm,ProfileUpdateForm, AgentVerificationForm
from django.shortcuts import render,  get_object_or_404 , redirect
from .models import Post, Profile,UserPlan,SubscriptionPlan,Request
from .models import Payment
from .paystack import verify_payment
import uuid
import requests
import json
from django.urls import reverse
from django.db.models import Count
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import timedelta,datetime
from django.contrib.auth import login


PAYSTACK_VERIFY_URL = "https://api.paystack.co/transaction/verify/"
# Create your views here.
def home(request):
    random_posts = Post.objects.order_by('?')[:8]
    return render(request, 'estateapp/home.html', {'random_posts' :random_posts})


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


def success (request):        
    
    return render(request, 'estateapp/success.html')
def House(request):
    
    return render(request, 'estateapp/House.html')

@login_required(login_url='login')
def post_create(request):
   
   if request.method == 'POST':
      form = PostForm(request.POST, request.FILES)

      author = request.user


      title = request.POST.get('title')
      short = request.POST.get('short')
      category = request.POST.get('category')
      building = request.POST.get('building')
      subtype = request.POST.get('subtype', '')
      bedroom = request.POST.get('bedroom', '')
      bathroom = request.POST.get('bathroom', '')
      toilet = request.POST.get('toilet', '')
      area = request.POST.get('area')
      state = request.POST.get('state')
      availability = request.POST.get('availability')
      totalarea = request.POST.get('totalarea')
      coveredarea = request.POST.get('coveredarea')
      description = request.POST.get('description')
      
      thumb = request.FILES.get('thumb')
      secondary = request.FILES.get('image1')
      secondary_2 = request.FILES.get('image2')
      secondary_3 = request.FILES.get('image3')
      secondary_4 = request.FILES.get('image4')
      secondary_5 = request.FILES.get('image5')
      secondary_6 = request.FILES.get('image6')
     
      currencyfield =  request.POST.get('currencyfield')
      url = request.POST.get('url')
      

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
    

    post_count = 0
    if request.user.is_authenticated:
        profile, created = UserPlan.objects.get_or_create(user=request.user)
        post_count = Post.objects.filter(author=request.user).count()

    context = {
        'post_count' : post_count,
        'profile': profile,
        'plan_name': profile.plan.name if profile.plan else "No Plan",
        
    }
    return render(request, 'estateapp/dashboard.html', context)

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
        return redirect('profile_update')  

    return render(request, 'estateapp/profile.html')

def howitworks(request):

    return render(request, 'estateapp/howitworks.html')  



@login_required
def subscription(request):
    if request.user.is_authenticated:
        profile = request.user.userplan
        if profile.is_paid_active and profile.expiry_date and profile.expiry_date <= timezone.now():
            profile.is_paid_active = False
            profile.save()
    
    plans = SubscriptionPlan.objects.all()

    context = {

        'plan_name': profile.plan.name if profile.plan else "No Plan",
        'plans': plans,
        'now': timezone.now(),
        
    }
    return render(request, 'estateapp/subscription.html', context)

@login_required
def initialize_payment(request):
    if request.method == 'POST':
        user = request.user
        profile = user.userplan

      
        if profile.is_paid_active and profile.expiry_date and profile.expiry_date > timezone.now():
            remaining_days = (profile.expiry_date - timezone.now()).days
            messages.warning(request, f"You already have an active subscription  that expires in {remaining_days} day(s).")
            return redirect('dashboard')

       
        plan_id = request.POST.get('plan_id')
        user_email = request.user.email
        plan = SubscriptionPlan.objects.get(id=plan_id)
        amount = int(plan.price) * 100  

        request.session['selected_plan_id'] = plan.id

        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        data = {
            "email": user_email,
            "amount": amount,
            "callback_url": request.build_absolute_uri(reverse('payment_callback')),
            "metadata": {
                "plan_id": plan.id
            }
        }

        response = requests.post('https://api.paystack.co/transaction/initialize', json=data, headers=headers)
        res = response.json()

        if res.get('status'):
            auth_url = res['data']['authorization_url']
            return redirect(auth_url)
        else:
            return JsonResponse({'error': 'Payment initialization failed'}, status=400)  


def verify_payment_with_paystack(reference):
    url = f"https://api.paystack.co/transaction/verify/{reference}"
    headers = {
        "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('data', {})
    return None


@login_required
def payment_history(request):

    payments = Payment.objects.filter(user=request.user).order_by("date_created")
    return render(request, "estateapp/payment_history.html", {"payments": payments})   


def payment_callback(request):
    reference = request.GET.get('reference')

    if not reference:
        messages.error(request, "Payment callback missing transaction details.")
        return redirect('dashboard')

    try:
        verification_result = verify_payment_with_paystack(reference)
        print("DEBUG - Paystack verification result:", verification_result)

        if verification_result and verification_result.get('status') == 'success':
            user = request.user

            if user.is_authenticated:
                try:
                    profile = user.userplan # Assuming OneToOne relation

                    metadata = verification_result.get('data', {}).get('metadata', {})
                    plan_id = metadata.get('plan_id') or request.session.get('selected_plan_id')
                    plan = None

                    if plan_id:
                        try:
                            plan = SubscriptionPlan.objects.get(id=plan_id)
                            profile.plan = plan
                        except SubscriptionPlan.DoesNotExist:
                            messages.warning(request, "Payment successful, but the selected plan no longer exists.")

                    profile.is_paid_active = True
                    profile.expiry_date = calculate_expiry_date()
                    profile.paystack_reference = reference
                    profile.save()

                    formatted_expiry = profile.expiry_date.strftime("%B %d, %Y")
                    Payment.objects.create(
                    user=user,
                    price = plan,
                    reference = reference,
                    verified = True,
                    )


                    if profile.plan:
                        messages.success(request, f"Subscription activated! You’re now on the {profile.plan.name} plan. It expires on {formatted_expiry}.")
                    else:
                        messages.success(request, f"Subscription activated! Your plan expires on {formatted_expiry}.")

                except UserPlan.DoesNotExist:
                    messages.error(request, "Payment was successful, but no user profile was found. Please contact support.")
            else:
                messages.warning(request, "Payment successful, but no authenticated user found.")

            return redirect('dashboard')

        else:
            messages.error(request, "Payment verification failed. Please try again or contact support.")
            return redirect('failed')
            
    except Exception as e:
        import traceback
        print("DEBUG - Exception Traceback:")
        traceback.print_exc()
        messages.error(request, f"An error occurred during payment: {e}")
        return render(request, 'estateapp/failed.html')


        
def calculate_expiry_date():
    
    return datetime.now() + timedelta(days=30)    


def failed(request):

    return render(request, 'estateapp/failed.html')

def request_view(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        asking = request.POST.get('asking')
        house = request.POST.get('house')
        describe = request.POST.get('describe')

        new_request = Request(
            name=name,
            email=email,
            phone=phone,
            asking=asking,
            house=house,
            describe=describe
        )
        new_request.save()

        return redirect('success')  

    return render(request, 'estateapp/request.html')


def viewrequest(request):  
    requests_data = []  

    for req in Request.objects.all(): 
        item = {
            'name': req.name,
            'email': req.email,
            'phone': req.phone,
            'asking': req.asking,
            'house': req.house,
            'describe': req.describe,
        }
        requests_data.append(item)

    context = {
        'requests': requests_data,
    }

    return render(request, 'estateapp/viewrequest.html', context)


@login_required
def verify_agent(request):
    profile = request.user.userplan
    if request.method == 'POST':
        form = AgentVerificationForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            profile.verification_status = 'pending'
            form.save()
            messages.success(request, "Your verification request has been submitted.")
            return redirect('dashboard')
    else:
        form = AgentVerificationForm(instance=profile)

    return render(request, 'estateapp/verifyagent.html', {'form': form})