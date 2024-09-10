from django.contrib import admin
from authapp.models import Contact,Membership_Plan,Enrollment,Trainer,Attendance
# Register your models here.

admin.site.register(Contact)
admin.site.register(Enrollment)
admin.site.register(Trainer)
admin.site.register(Membership_Plan)
admin.site.register(Attendance)
