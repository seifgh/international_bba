from django.urls import path
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('', csrf_exempt(HomeView.as_view()), name="home"),

    path('presentation', PresentationView.as_view(), name="presentation"),

    path('services/<slug:service_slug>', ServiceView.as_view(), name="services"),

    path('modules', ModulesView.as_view(), name="modules"),
    path('modules/<slug:slug>', ModuleView.as_view(), name="module"),

    path('trainings', TrainingsView.as_view(),  name="trainings"),
    path('trainings/<slug:slug>', TrainingView.as_view(), name="training"),
    path('trainings/register/<slug:slug>', TrainingRegistrationView.as_view(),
         name="training-registration"),
    path('training/register', csrf_exempt(TrainingRegistrationView.as_view()),
         name="training-registration-post"),

    path('trainer', csrf_exempt(TrainerView.as_view()), name="trainer"),

    path('news', NewsView.as_view(), name="news"),
    path('news/<slug:slug>', ArticleView.as_view(), name="article"),

    path('contact', csrf_exempt(ContactView.as_view()), name="contact"),
    path('subscribe', csrf_exempt(SubscriberView.as_view()), name="subscribe"),

    path('registration/verifie/<key>',
         TrainingRegistrationVerification, name="verify-registration"),
    path('trainer/verifie/<key>', TrainerVerification, name="verify-trainer"),
]
