from django.urls import path
from django.contrib import admin
from .import views
from estateapp.views import post_create
from django.conf import settings
from .views import PostListView, PostDetailView
from django.conf.urls.static import static
from .views import search_results, post_edit
from .views import verify_payment,initialize_payment,payment_callback
from django.views.generic import RedirectView
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('pro/', views.post_create),
    path('howitworks/', views.howitworks),
    path('done/', views.save, name="done"),
    path('success/', views.success, name="success"),
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
    path('initialize_payment/', views.initialize_payment, name='initialize_payment'),
    path('verify_payment/', views.verify_payment, name='verify_payment'),
    path('payment_history/', views.payment_history, name='payment_history'),
    path('payment_callback/', views.payment_callback, name='payment_callback'),
    path('failed/',views.failed, name="failed"),
    path('viewrequest/',views.viewrequest, name="viewrequest"),
    path('request/',views.request_view, name="request"),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('verifyagent/',views.verify_agent, name="verifyagent"),
    

    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)