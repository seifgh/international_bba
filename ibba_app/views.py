from django.shortcuts import render
from django.http import JsonResponse,  Http404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from ratelimit.mixins import RatelimitMixin
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db import models
from django.core.exceptions import SuspiciousOperation


import json
from functools import reduce
import operator
import random
import string
import datetime
import requests
import re

from .forms import *

# -------------useful functions------------------


def validate_date(date_text):

    # if ( re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", date_text ) is None ):
    #     return False

    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except:
        return False


def get_parent_module(code):
    for i in modules:
        if i[0] == code:
            return i[1]
    return ''


def getObjectOr404(obj, pk=None, slug=None):
    if (not (pk or slug)):
        raise Exception("Wrong params")
    try:
        obj = obj.objects.get(slug=slug) if (slug) else obj.objects.get(pk=pk)
        return obj
    except obj.DoesNotExist:
        raise Http404


def Pagination(queryset, paginate_by, page):
    paginator = Paginator(queryset, paginate_by)
    try:
        p = paginator.page(page)

        return {
            'objects': p.object_list.all(),
            # 'count':  queryset.count(),
            'page': page,
            # 'has_next' : {'bool' : p.has_next(), 'page' : page + 1},
            # 'has_previous' : {'bool' :  p.has_previous(), 'page' : page -1},
            'has_next': p.has_next(),
            'has_previous': p.has_previous(),
            'page_range': paginator.page_range,
            'num_pages': paginator.num_pages,
        }
    except (EmptyPage, PageNotAnInteger):
        raise Http404


def captcha_check_or_400(token):
    if (not settings.TEST_MODE):
        if (token):
            data = {
                'response': token,
                'secret': settings.RECAPTCHA_SECRET_KEY,
            }
            resp = requests.post(
                'https://www.google.com/recaptcha/api/siteverify', data=data, timeout=3000)
            result_json = resp.json()
            if not result_json.get('success'):
                raise SuspiciousOperation("invalid captcha")
            return True
        raise SuspiciousOperation("invalid captcha")


def get_base_data():
    # repetitive data for ( footer, header, ...)
    return {
        "base_modules": Module.objects.all().order_by("?")[0:6],
        "reCAPTCHA_site_key": settings.RECAPTCHA_SITE_KEY,
    }


# end

class HomeView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request):

        soon_trainings = Training.objects.filter(dates__start_date__gte=timezone.now()).annotate(
            dates__start_date=models.Min('dates__start_date')).order_by('dates__start_date').distinct()[0:4]
        context = {
            "soon_trainings": soon_trainings,
            "testimonials": Testimonial.objects.filter(is_at_home=True)[0:3],
            "catalogue": Catalogue.objects.last(),
            "clients": Client.objects.filter(is_at_home=True),
            "articles": Article.objects.filter(is_new=True)[0:6],
            **get_base_data()
        }

        return render(request, 'index.html', context)

    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post(self, request):
        captcha_check_or_400(request.POST.get('token'))
        form = CatalogEmailForm(request.POST)
        if (form.is_valid()):
            form = form.save(commit=False)
        else:
            return JsonResponse(status=400, data=form.errors)

        subject = 'profitez de notre catalogue ...'
        html_message = render_to_string(
            'emails/catalog.html', {'catalogue_url': settings.CATALOGUE_URL})
        plain_message = strip_tags(html_message)
        from_email = 'internationalbba@topnet.tn'
        to = request.POST.get('email')
        try:
            send_mail(subject, plain_message, from_email,
                      [to], html_message=html_message)
        except BadHeaderError:
            return JsonResponse(status=500, data={'message': 'There is a technical problem !'})
        form.save()
        return JsonResponse(status=201, data={'message': 'Thanks for your registration'})


class ServiceView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request, service_slug):
        if service_slug == "inter-entreprises":
            modules = Module.objects.all()
            context = {
                'modules': modules,
                **get_base_data()
            }
            return render(request, 'services/inter-entreprises.html', context)
        if service_slug == "consulting":
            return render(request, 'services/consulting.html', get_base_data())
        if service_slug == "intra-entreprises":
            return render(request, 'services/intra-entreprises.html', get_base_data())
        raise Http404


class ContactView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request):
        context = get_base_data()
        # contact from training page
        if (request.GET.get('training_id')):
            trainning = getObjectOr404(
                Training, pk=request.GET.get('training_id'))
            context['subject'] = trainning.title
        elif (request.GET.get('subject')):
            context['subject'] = request.GET.get('subject')
        return render(request, "contact.html", context)

    @ratelimit(key='ip', rate='2/d', method='POST', block=True)
    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            captcha_check_or_400(request.POST.get('token'))
            form.save()
            return JsonResponse(status=201, data={'message': 'Thanks for your registration'})
        return JsonResponse(status=400, data=form.errors)


class TrainingView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request, slug):
        training = getObjectOr404(obj=Training, slug=slug)
        try:
            dates = training.formated_date
        except ValueError:
            raise Http404
        try:
            related = training.module_training.first().trainings.exclude(
                id=training.id).filter(dates__start_date__gte=timezone.now()).distinct()
        except:
            related = None
        context = {
            "title": training.title,
            "slug": training.slug,
            "id": training.id,
            "image": training.formated_image,
            "description": training.description,
            "short_description": training.short_description,
            "duration": training.duration,
            "date": dates['date'],
            "dates": dates['dates'],
            "modules": training.module_training.all().values("title", "slug"),
            "related": related,
            **get_base_data()
        }
        return render(request, "trainings/training.html", context)

    # training registration view
    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post(self, request):
        captcha_check_or_400(request.POST.get('token'))
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save(commit=False)
        else:
            return JsonResponse(status=400, data=form.errors)
        str_ = string.digits + string.ascii_letters + \
            request.POST.get('first_name')
        key = ''.join(random.SystemRandom().choice(str_) for _ in range(20))
        while (Registration.objects.filter(verification_key=key).exists()):
            key = ''.join(random.SystemRandom().choice(str_)
                          for _ in range(20))

        subject = 'Vérifiez votre e-mail'
        html_message = render_to_string(
            'emails/email-verification.html', {'url': '{}/registration/verifie/{}'.format(settings.CURRENT_HOST, key)})
        plain_message = strip_tags(html_message)
        from_email = 'From IBBA@topnet.com'
        to = request.POST.get('email')
        try:
            send_mail(subject, plain_message, from_email,
                      [to], html_message=html_message)
        except BadHeaderError:
            return JsonResponse(status=500, data={'message': 'There is a technical problem !'})
        registration.verification_key = key
        registration.save()
        return JsonResponse(status=201, data={'message': 'Thanks for your registration'})


@ratelimit(key='ip', rate='10/h', method='GET', block=True)
def TrainingRegistrationVerification(request, key):
    if (request.method == "GET"):
        try:
            registration = Registration.objects.get(
                verification_key=key, is_verified=False)
        except Registration.DoesNotExist:
            raise Http404
        registration.is_verified = True
        registration.save()
        base_data = {
            "base_modules": Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key": settings.RECAPTCHA_SITE_KEY,
        }
        return render(request, 'emails/email_verified.html', base_data)
    raise Http404


class TrainingRegistrationView(View):

    def get(self, request, slug):
        training = getObjectOr404(obj=Training, slug=slug)
        try:
            dates = training.formated_date
        except ValueError:
            raise Http404

        context = {
            "title": training.title,
            "id": training.id,
            "short_description": training.short_description,
            "duration": training.duration,
            "date": dates['date'],
            **get_base_data()
        }
        return render(request, "trainings/register.html", context)

    def post(self, request):

        form = RegistrationForm(request.POST)
        if form.is_valid():
            captcha_check_or_400(request.POST.get('token'))
            registration = form.save(commit=False)
        else:
            return JsonResponse(status=400, data=form.errors)
        str_ = f"{string.digits}{string.ascii_letters}{request.POST.get('first_name')}"

        key = ''.join(random.SystemRandom().choice(str_) for _ in range(20))
        while (Registration.objects.filter(verification_key=key).exists()):
            key = ''.join(random.SystemRandom().choice(str_)
                          for _ in range(20))

        subject = 'Vérifiez votre e-mail'
        html_message = render_to_string(
            'emails/email-verification.html', {'url': '{}/registration/verifie/{}'.format(settings.CURRENT_HOST, key)})
        plain_message = strip_tags(html_message)
        from_email = 'From IBBA@topnet.com'
        to = request.POST.get('email')
        # try:
        #     send_mail(subject, plain_message, from_email,
        #               [to], html_message=html_message)
        # except BadHeaderError:
        #     return JsonResponse(status=500, data={'message': 'There is a technical problem !'})
        registration.verification_key = key
        registration.save()
        return JsonResponse(status=201, data={'message': 'Thanks for your registration'})


class ModuleView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request, slug):
        module = getObjectOr404(Module, slug=slug)
        trainings_not_realized = module.trainings.filter(dates__start_date__gte=timezone.now()).annotate(
            dates__start_date=models.Min('dates__start_date')).order_by('dates__start_date').distinct()
        context = {
            'title': module.title,
            'logo': module.formated_logo,
            'description': module.description,
            'count': trainings_not_realized.count(),
            'trainings_not_realized': trainings_not_realized,
            **get_base_data()
        }
        return render(request, 'modules/module.html', context)


class TrainingsView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request):
        search_word = request.GET.get("sq")
        trainings = Training.objects.filter(
            dates__start_date__gte=timezone.now()).distinct()
        try:
            page = int(request.GET.get('page', 1))
        except ValueError:
            raise Http404

        context = {**Pagination(trainings, 12,  page), **get_base_data()}
        if (search_word):
            context['search_word'] = search_word

        context["modules"] = Module.objects.exclude(trainings=None).filter(
            trainings__dates__start_date__gte=timezone.now()).distinct().order_by("title")

        return render(request, "trainings/index.html", context)


class ModulesView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request):
        filter_by = request.GET.get('filter_by')
        if filter_by in ['m-f', 'm-t']:
            modules = Module.objects.filter(type=filter_by)

            if (filter_by == 'm-t'):
                context = {
                    'count_t': modules.count(),
                    'modules_t': modules,
                    **get_base_data()
                }
            else:
                context = {
                    'count_f': modules.count(),
                    'modules_f': modules,
                    **get_base_data()
                }
        else:
            modules_f = Module.objects.filter(type='m-f')
            modules_t = Module.objects.filter(type='m-t')

            context = {
                'modules_f': modules_f,
                'modules_t': modules_t,
                'count_f': modules_f.count(),
                'count_t': modules_t.count(),
                **get_base_data()
            }

        return render(request, "modules/index.html", context)


class PresentationView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request):
        context = {
            'modules': Module.objects.all(),
            **get_base_data()
        }
        return render(request, "presentation.html", context)


class TrainerView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request):
        return render(request, 'trainer.html', get_base_data())

    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post(self, request):
        form = TrainerForm(request.POST, request.FILES)
        if form.is_valid():
            captcha_check_or_400(request.POST.get('token'))
            trainer = form.save(commit=False)
        else:
            return JsonResponse(status=400, data=form.errors)
        str_ = f"{string.digits}{string.ascii_letters}{request.POST.get('first_name')}"
        key = ''.join(random.SystemRandom().choice(str_) for _ in range(20))
        while (Trainer.objects.filter(verification_key=key).exists()):
            key = ''.join(random.SystemRandom().choice(str_)
                          for _ in range(20))

        subject = 'Vérifiez votre e-mail'
        html_message = render_to_string(
            'emails/email-verification.html', {'url': '{}/trainer/verifie/{}'.format(settings.CURRENT_HOST, key)})
        plain_message = strip_tags(html_message)
        from_email = 'From IBBA@topnet.com'
        to = request.POST.get('email')
        # try:
        #     send_mail(subject, plain_message, from_email,
        #               [to], html_message=html_message)
        # except BadHeaderError:
        #     return JsonResponse(status=400, data={'message': 'There is a tchnical problem !'})
        trainer.verification_key = key
        trainer.save()
        return JsonResponse(status=201, data={'message': 'Thanks for your registration'})

# verify the trainer email


@ratelimit(key='ip', rate='5/h', method='GET', block=True)
def TrainerVerification(request, key):
    if (request.method == "GET"):
        try:
            trainer = Trainer.objects.get(
                verification_key=key, is_verified=False)
        except Trainer.DoesNotExist:
            raise Http404
        trainer.is_verified = True
        trainer.save()

        return render(request, 'emails/email_verified.html', get_base_data())
    raise Http404


class NewsView(View):
    def get(self, request):
        try:
            page = int(request.GET.get('page')
                       ) if request.GET.get('page') else 1
        except ValueError:
            raise Http404
        context = {
            **Pagination(Article.objects.all(), 12,  page), **get_base_data()}

        return render(request, 'news/index.html', context)


class ArticleView(View):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request, slug):
        article = getObjectOr404(Article, slug=slug)
        context = {
            'article': article,
            **get_base_data()
        }
        return render(request, 'news/article.html', context)


class SubscriberView(View):

    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post(self, request):
        #     send_mail(subject, plain_message, from_email,
        #               [to], html_message=html_message)
        # except BadHeaderError:
        #     return JsonResponse(status=400, data={'message': 'There is a tchnical problem !'})      captcha_check_or_400(request.POST.get('token'))
        form = SubsriberForm(request.POST)
        if form.is_valid():
            captcha_check_or_400(request.POST.get('token'))
            form.save()
            return JsonResponse(status=201, data={'message': 'Thanks for your registration'})
        return JsonResponse(status=400, data=form.errors)
