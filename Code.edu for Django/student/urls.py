from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    #Question
    path(
        "",
        views.IndexView.as_view(), 
        name='index'
    ),
    path(
        "questions/<int:question_id>/",
        views.QuestionDetailView.as_view(),
        name="question-detail",
    ),
    path(
        "questions/new/", 
        views.QuestionCreateView.as_view(), 
        name="question-create"),
    path(
        "questions/<int:question_id>/edit/",
        views.QuestionUpdateView.as_view(),
        name="question-update",
    ),
    path(
        "questions/<int:question_id>/delete/",
        views.QuestionDeleteView.as_view(),
        name="question-delete",
    ),

    #Template
    path(
        "submit_problem/", 
        views.SubmitProblemView.as_view(), 
        name="submit-problem"
    ),
    path(
        "user_register/", 
        views.UserRegisterView.as_view(), 
        name="user-register"
    ),
    path(
        "delete_problem/",
        views.DeleteProblemsView.as_view(),
        name="delete-problems"
    ),

    #Profile
    path(
        "users/<int:user_id>/", 
        views.ProfileView.as_view(), 
        name="profile"
    ),
    path(
        "users/<int:user_id>/questions/",
        views.UserQuestionListView.as_view(),
        name="user-question-list",
    ),
    path(
        "set-profile/", 
        views.ProfileSetView.as_view(), 
        name="profile-set"
    ),
    path(
        "edit-profile/", 
        views.ProfileUpdateView.as_view(), 
        name="profile-update"
    ),

    #Group
    path(
        "group-info/",
        views.GroupInfoView.as_view(),
        name="group-info"
    ),
    path(
        "group-set/",
        views.GroupSetView.as_view(),
        name="group-set"
    ),
    path(
        "group-upadte/<int:group_id>/",
        views.GroupUpdateView.as_view(),
        name="group-update"
    ),
]