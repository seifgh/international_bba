from django.urls import path
from django.conf.urls import url
from .views import *
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('contact', csrf_exempt(ContactView.as_view()) , name="contact" ) ,
    path('registration/create', csrf_exempt(TrainingView.as_view()), name="register"),
    path('registration/verifie/<key>', TrainingRegistrationVerification, name="verify-registration" ),

    path('training/<slug>', TrainingView.as_view(), name="training"),
    path('trainings', TrainingsView.as_view(),  name="trainings"),

    path('module/<slug>', ModuleView.as_view(), name="module"),
    path('modules', ModulesView.as_view(), name="modules"),
    path('presentation', PresentationView.as_view(), name="presentation"),

    path('trainer', csrf_exempt(TrainerView.as_view()), name="trainer" ),
    path('trainer/verifie/<key>', TrainerVerification, name="verify-trainer" ),
    path('', csrf_exempt(HomeView.as_view()), name="home"),
    path('news', ArticleView.as_view(), name="news" ),
    path('news/<slug>', ArticleView.as_view()),
    path('subscribe',csrf_exempt(SubscriberView.as_view()), name="subscribe"),

    path('services/<service_slug>',ServiceView.as_view(), name="services")

]
