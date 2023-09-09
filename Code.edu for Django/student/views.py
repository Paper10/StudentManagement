from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.views import View
from django.db import IntegrityError
from braces.views import LoginRequiredMixin, UserPassesTestMixin
from allauth.account.views import PasswordChangeView
from student.models import *
from student.forms import *
# Create your views here.

#Qusetion

class IndexView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "student/index.html"
    context_object_name = "questions"
    ordering = ["-dt_created"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['numbers'] = list(range(1, 31))
        context["problems"] = Problem.objects.all()

        user = self.request.user
        if user.teacher:
            user_groups = Membership.objects.filter(member=user).values_list('group')
            context['questions'] = Question.objects.filter(viewer__in=user_groups).order_by("-dt_created")
        else:
            context['questions'] = Question.objects.filter(viewer=user.group_in).order_by("-dt_created")

        return context


class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "student/question_detail.html"
    pk_url_kwarg = "question_id"

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    form_class = QuestionForm
    template_name = "student/question_form.html"

    redirect_unauthenticated_users = True

    def form_valid(self, form):
        form.instance.author = self.request.user
        viewer = form.cleaned_data.get('viewer') or self.request.user.group_in
        form.instance.viewer = viewer
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("question-detail", kwargs={"question_id": self.object.id})
    
class QuestionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Question
    form_class = QuestionForm
    template_name = "student/question_form.html"
    pk_url_kwarg = "question_id"

    raise_exception = True

    def get_success_url(self):
        return reverse("question-detail", kwargs={"question_id": self.object.id})

    def test_func(self, user):
        question = self.get_object()
        return question.author == user
    
class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = "student/question_confirm_delete.html"
    pk_url_kwarg = "question_id"

    raise_exception = True

    def get_success_url(self):
        return reverse("index")

    def test_func(self, user):
        question = self.get_object()
        return question.author == user

# Template

class SubmitProblemView(LoginRequiredMixin, View):
    template_name = 'index.html'
    success_url = 'index'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        numbers = request.POST.getlist('numbers')
        group_in = request.user.group_in

        for number in numbers:
            try:
                problem = Problem(group=group_in, number=number)
                problem.save()
            except IntegrityError:
                pass

        return redirect(self.success_url)
    
class UserRegisterView(LoginRequiredMixin, View):
    template_name = 'group.html'
    success_url = 'group-info'

    def get(self, request):
        return render(request, self.template_name)
    
    def post(self, request):
        user_id = request.POST.get('user_to_change_group')
        new_group_id = request.POST.get('new_group')
        new_group = Group.objects.get(id=new_group_id)
        User.objects.filter(id=user_id).update(group_in=new_group)
        return redirect(self.success_url)

class DeleteProblemsView(LoginRequiredMixin, View):
    def post(self, request):
        group_id = request.POST.get('group_id')
        Problem.objects.filter(group=group_id).delete()
        return redirect('group-info')

#Profile

class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = "student/profile.html"
    pk_url_kwarg = "user_id"
    context_object_name = "profile_user"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs.get("user_id")
        context["user_questions"] = Question.objects.filter(author__id=user_id).order_by(
            "-dt_created"
        )[:4]
        return context


class UserQuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "student/user_question_list.html"
    context_object_name = "user_questions"
    paginate_by = 4

    def get_queryset(self):
        user_id = self.kwargs.get("user_id")
        return Question.objects.filter(author__id=user_id).order_by("-dt_created")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profile_user"] = get_object_or_404(User, id=self.kwargs.get("user_id"))
        return context


class ProfileSetView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "student/profile_set_form.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("index")
    
    def form_valid(self, form):
        form.instance.group_in = self.request.user.group_in
        return super().form_valid(form)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileForm
    template_name = "student/profile_update_form.html"

    def get_object(self, queryset=None):
        return self.request.user

    def get_success_url(self):
        return reverse("profile", kwargs={"user_id": self.request.user.id})

#Password

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    def get_success_url(self):
        return reverse("profile", kwargs={"user_id": self.request.user.id})
    
#Group

class GroupInfoView(LoginRequiredMixin, ListView):
    template_name = "student/group.html"
    context_object_name = "user_groups"
    paginate_by = 1

    def get_queryset(self):
        user = self.request.user
        user_groups = Membership.objects.filter(member=user).values_list('group')
        return Group.objects.filter(pk__in=user_groups)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["users"] = User.objects.all()
        context["problems"] = Problem.objects.all()
        return context
    
    
class GroupSetView(LoginRequiredMixin, CreateView):
    model = Group
    form_class = GroupForm
    template_name = "student/group_set_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.request.user
        Membership.objects.create(member=user, group=self.object)
        return response

    def get_success_url(self):
        return reverse("group-info")


class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = "student/group_update_form.html"

    def get_object(self, queryset=None):
        group_id = self.kwargs['group_id']
        return get_object_or_404(Group, id=group_id)


    def get_success_url(self):
        return reverse("group-info")
