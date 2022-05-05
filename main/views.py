from dataclasses import field
import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, TemplateView, UpdateView

from .forms import LessonUpdateForm, LoginUserForm, SignUpUserForm, EditProfile, CreateLessonForm, LessonEdit, SponsorShipsFormSet
from .models import Lessons, CustomUser, LessonsDescriptions, Files, Speciality


def page_not_found_view(request, exception):
    print(123)
    return render(request, '404_page.html', status=404)

class AboutPage(TemplateView):
    template_name='about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'О сайте'
        return context

class TopPage(TemplateView):
    template_name='top-page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Прикольчики'
        return context

class HomePage(LoginRequiredMixin,ListView):
    #paginate_by = 3 # Пагинация
    login_url = 'sign-in'
    template_name = 'index.html'
    context_object_name = 'lessons'

    def get_queryset(self):
        return Lessons.objects.filter(speciality=self.request.user.speciality).order_by('name')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class LessonPage(LoginRequiredMixin,DetailView):
    login_url = 'sign-in'
    model = Lessons
    template_name = 'Lessons.html'



    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['object']
        test = {}
        x = [x for x in LessonsDescriptions.objects.filter(lesson_id=context['object'])]
        g = Files.objects.filter(lesDesc_id__in=x)
        for i in x:
            l=[]
            for k in g:
                if k.lesDesc_id == i.id:
                    l.append(k)
            test[i] = l
        context['x'] = test.items()
        return context


def logout_view(request):
    logout(request)
    return redirect('home')

# def lessons(request, lesson_id):
#     lessons = Lessons.objects.get(slug=lesson_id)
#     lessDesc = LessonsDescriptions.objects.filter(lesson_id=lessons.pk)
#     files = Files.objects.filter(lesDesc_id__in=[i.pk for i in lessDesc])
#     context = {
#         'title': lessons.name,
#         'lessDesc': lessDesc,
#         'files': files,
#     }
#     return render(request, 'Lessons.html', context=context)

# def index(request):
#     lessons = Lessons.objects.all()
#     context = {
#         'title': 'Главная страница',
#         'lessons': lessons,
#     }
#     return render(request, 'index.html', context=context)

class SignForm(LoginView):
    template_name = 'sign-in.html'
    form_class = LoginUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Войти'
        context['title'] = 'Вход'
        return context

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == True:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        instance.groups.add(Group.objects.get(name='Студент'))

class SignUp(CreateView):
    template_name = 'sign-up.html'
    form_class = SignUpUserForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['button'] = 'Зарегистрироваться'
        context['title'] = 'Регистрация'
        return context

    def form_valid(self, form):
        user = form.save()
        login(self.request,user)
        return redirect('home')

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated == True:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class ProfilePage(LoginRequiredMixin,TemplateView):
    login_url = 'sign-in'
    template_name='profile-page.html'
    model = CustomUser
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль'
        return context

class EditProfile(LoginRequiredMixin,UpdateView):
    login_url = 'sign-in'
    template_name='edit.html'
    model = CustomUser
    form_class = EditProfile
    success_url = reverse_lazy('profile-page')
    slug_field = 'id'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменить профиль'
        return context

class LessonEditPage(PermissionRequiredMixin,LoginRequiredMixin,ListView):
    permission_required = 'main.add_lessons'

    #paginate_by = 3 # Пагинация
    template_name = 'lesson-view.html'
    context_object_name = 'lessons'


    def get_queryset(self):
        return Lessons.objects.filter(owner=self.request.user)

    def handle_no_permission(self):
        messages.error(self.request, 'У вас нет прав для просмотра данный страницы')
        return redirect('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        les = Lessons.objects.filter(owner=self.request.user)
        spec_ids = [x.speciality_id for x in les]
        spec = Speciality.objects.filter(id__in=spec_ids)
        test = {}
        for k in spec:
            for o in les:
                if k.id == o.speciality_id:
                    test[o] = k
        context['x'] = test.items()
        context['title'] = 'Ваши предметы'
        return context

class LessonCreate(CreateView):
    template_name = 'lesson-create.html'
    form_class = CreateLessonForm
    success_url = reverse_lazy('lesson-view')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание предмета'
        return context

    def form_valid(self, form):
        form.instance.owner_id = self.request.user.id
        return super().form_valid(form)

# class LessonEditPage(ListView):
#     #paginate_by = 3 # Пагинация
#     template_name = 'lesson-view.html'
#     context_object_name = 'lessons'
#
#     def get_queryset(self):
#         return Lessons.objects.filter(owner=self.request.user)

class LessonChangePage(LoginRequiredMixin,CreateView):
    login_url = 'sign-in'
    template_name='lesson-edit.html'
    model = Lessons
    form_class = LessonEdit
    success_url = reverse_lazy('lesson-view')
    sss = ''

    def get_context_data(self, **kwargs):
        data = super(LessonChangePage, self).get_context_data(**kwargs)
        if self.request.POST:
            data['form_urina_rotina'] = SponsorShipsFormSet(self.request.POST, self.request.FILES)
        else:
            data['form_urina_rotina'] = SponsorShipsFormSet(instance=self.object)
            data['title'] = 'Добавление темы'
        return data

    def dispatch(self, request, *args, **kwargs):
        self.sss = kwargs.get('slug')
        x = Lessons.objects.filter(slug=kwargs.get('slug'), owner=self.request.user)
        if x:
            return super().dispatch(request, *args, **kwargs)
        else:
            messages.error(self.request, 'У вас нет прав для просмотра данный страницы')
            return redirect('home')


    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.lesson_id = self.sss
        context = self.get_context_data()
        sponsorships = context['form_urina_rotina']
        with transaction.atomic():
            form.instance.created_by = self.request.user
            form.instance.updated_by = self.request.user
            if sponsorships.is_valid():
                self.object = form.save()
                sponsorships.instance = self.object
                sponsorships.save()
                return redirect('/lessons/' + form.instance.lesson_id )
            else:
                return self.form_invalid(form)

class LessonUpdate(UpdateView):
    template_name='lesson-update.html'
    model = Lessons
    form_class = LessonUpdateForm
    success_url = reverse_lazy('lesson-view')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение предмета'
        return context


class TopicUpdateForm(UpdateView):
    template_name='topic-update.html'
    model = LessonsDescriptions
    form_class = LessonEdit
    slug_field = 'id'
    slug_url_kwarg = 'id'
    success_url = reverse_lazy('lesson-view')

    def get_context_data(self, **kwargs):
        data = super(TopicUpdateForm, self).get_context_data(**kwargs)
        if self.request.POST:
            data['form_urina_rotina'] = SponsorShipsFormSet(self.request.POST, self.request.FILES, instance=self.object)
        else:
            data['form_urina_rotina'] = SponsorShipsFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        sponsorships = context['form_urina_rotina']
        self.object = form.save()
        print()
        sponsorships.instance = self.object
        with transaction.atomic():
            form.instance.created_by = self.request.user
            form.instance.updated_by = self.request.user
            if sponsorships.is_valid():
                sponsorships.save()
                return redirect('/lessons/' + form.instance.lesson_id )
            else:
                return super().form_invalid(form)
# class LessonChangePage(LoginRequiredMixin,FormView):
#     login_url = 'sign-in'
#     template_name='lesson-edit.html'
#     model = Lessons
#     form_class = formset_factory(LessonEdit)
#     success_url = reverse_lazy('lesson-view')
#
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Редактирование'
#         return context
#
#
#     def post(self, request, *args, **kwargs):
#         form_class = self.get_form_class()
#         form = self.get_form(form_class)
#         files = request.FILES.getlist('topic_content')
#         if form.is_valid():
#             l = LessonsDescriptions.objects.create(topic=form.cleaned_data.get("topic"), lesson_id=22)
#             for f in files:
#                 Files.objects.create(lesDesc_id=l.id, name='123',topic_content=f, file_type='PDF')
#             return self.form_valid(form)
#         else:
#             return self.form_invalid(form)