from django.contrib import admin
from authapp.models import Contact,Membership_Plan,Enrollment,Trainer
# Register your models here.

admin.site.register(Contact)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(Membership_Plan)
