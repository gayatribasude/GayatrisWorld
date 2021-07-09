from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from .models import User, VisitorEmail,Contact

#admin.site.register(get_user_model())

class VisitorEmailModel(admin.ModelAdmin):
    list_display = ('id','active')
admin.site.register(User)
admin.site.register(VisitorEmail,VisitorEmailModel)
admin.site.register(Contact)