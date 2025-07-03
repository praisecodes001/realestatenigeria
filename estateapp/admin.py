from django.contrib import admin
from .models import Post
from .models import SubscriptionPlan,Request,UserPlan,Profile,Payment
from .forms import PostForm

class PostAdmin(admin.ModelAdmin):
    form= PostForm

admin.site.register(Post, PostAdmin)
admin.site.register(SubscriptionPlan)
admin.site.register(Request)
admin.site.register(UserPlan)
admin.site.register(Profile)
admin.site.register(Payment)

