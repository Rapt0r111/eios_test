
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe

from .forms import UserChangeForm, UserCreationForm
from .models import *

User = get_user_model()

class CaseDiscAdmin(admin.StackedInline):
    model = LessonsDescriptions
    extra = 1

class CaseFileAdmin(admin.StackedInline):
    model = Files
    extra = 1
    
class LessonsADmin(admin.ModelAdmin):
    inlines = [CaseDiscAdmin]
    print()
    list_display = ('name', 'photo', 'speciality', 'slug')
    fields = ('slug','name','speciality','photo','owner')
    slugified_string = {'slug': ('name','speciality')}

@admin.register(LessonsDescriptions)
class LessonsDiscrAdmin(admin.ModelAdmin):
    inlines = [CaseFileAdmin]
    list_display = ('lesson', 'topic', 'author_first_name')
    list_display_links = ('lesson', 'topic')
    search_fields=('lesson__name',)


    fieldsets = (
        ('Personal info', {'fields': ('topic', 'lesson')}),

    )

    @admin.display(ordering='lesson__speciality', description='Специальность')
    def author_first_name(self, obj):
        return  obj.lesson.speciality

# class CustomUserAdmin(UserAdmin):
#     add_form = UserChangeForm
#     list_display = ('username', 'email','content')
#     fieldsets = (
#         (None, {'fields': ('email', 'password')}),
#         ('Personal info', {'fields': ('last_name', 'content')}),
#         ('Permissions', {'fields': ('is_superuser',)}),
#     )



class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ( 'get_html_photo', 'email', 'username')
    list_display_links = ('get_html_photo', 'email')
    list_filter = ('is_superuser',)
    fieldsets = []
    fields = ('username', 'password', ('avatar', 'image_tag')  , 'first_name', 'last_name', 'email', 'speciality','content',
    'is_superuser', 'is_staff', 'is_active', 'groups', 'user_permissions', 'last_login', 'date_joined')
    readonly_fields = ['image_tag']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )
    search_fields = ('email','username')
    ordering = ('email',)

    def get_html_photo(self, object):
        if object.avatar:
            return mark_safe(f"<img src='{object.avatar.url}' width=50; style='border-radius:10px;'")

@admin.register(Speciality)
class SpecAdmin(admin.ModelAdmin):
    list_display = ('speciality',)

@admin.register(Files)
class SpecAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(CustomUser, UserAdmin)
admin.site.register(Lessons, LessonsADmin)