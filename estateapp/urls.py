from django.urls import path
from django.contrib import admin
from .import views
from estateapp.views import post_create
from django.conf import settings
from .views import PostListView, PostDetailView
from django.conf.urls.static import static
from .views import search_results, post_edit
from .views import subscription, process_payment, verify_payment
from django.views.generic import RedirectView

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('pro/', views.post_create),
    path('howitworks/', views.howitworks),
    path('done/', views.save),
    path('contact/',views.contact),
    path('dashboard/profile/',views.profile_update, name="profile_update"),
    path('contact/',views.contact),
    path('contactagent/',views.contact_agent),
    path('results/', search_results, name= "results"),
    path('dashboard/',views.dashboard, name="dashboard"),
    path("sign-up/", views.sign_upPage, name="register"),
    path("login/", views.loginPage, name="login"),
    path("subscription/", views.subscription, name="subscription"),
    path("logout/", views.logoutUser, name="logout"),
    path('registration-path/',views.registration_path),
    path('Listings/',views.PostListView.as_view(), name='Listings'),
    path('personal/',views.personal, name='personal'),
    path('edit/<int:post_id>/',views.post_edit , name='post_edit'),
    path('delete/<int:post_id>/', views.post_delete, name='post_delete'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name="post-detail"),
    path("subscriptions/", subscription, name="subscription_page"),
    path("payment/process/", process_payment, name="process_payment"),
    path("payment/verify/", verify_payment, name="verify_payment"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)