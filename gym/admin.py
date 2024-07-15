from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import GymUser, MembershipPlan, Member, FitnessClass, Booking, Instructor

class GymUserAdmin(UserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Additional info', {'fields': ('is_staff_member',)}),
    )

admin.site.register(GymUser, GymUserAdmin)
admin.site.register(MembershipPlan)
admin.site.register(Member)
admin.site.register(Instructor)
admin.site.register(FitnessClass)
admin.site.register(Booking)

