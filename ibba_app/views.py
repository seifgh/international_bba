from django.shortcuts import render
from django.http import JsonResponse,Http404
from django.views.generic import View
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from ratelimit.decorators import ratelimit
from ratelimit.mixins import RatelimitMixin
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.core.mail import send_mail,BadHeaderError
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.db import models



import json
from functools import reduce
import operator
import random
import string
import datetime
import requests
import re

from .forms import *

#-------------useful functions------------------

def validate_date( date_text ):

    # if ( re.match("^[0-9]{4}-[0-9]{2}-[0-9]{2}$", date_text ) is None ):
    #     return False

    try:
        datetime.datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except:
        return False

def get_parent_module( code ):
    for i in modules:
        if i[0] == code:
            return i[1]
    return ''

def getObjectOr404( obj, pk = None, slug = None  ):
    if ( not ( pk or slug ) ):
        raise Exception("Wrong params")
    try:
        obj =  obj.objects.get( slug = slug ) if ( slug )  else   obj.objects.get( pk = pk )
        return obj
    except obj.DoesNotExist:
        raise Http404


def Pagination(queryset,paginate_by,page):
	paginator = Paginator(queryset,paginate_by)
	try:
		p = paginator.page( page )

		return {
			'objects': p.object_list.all(),
            'count':  queryset.count(),
            'page' : page,
			'has_next' : {'bool' : p.has_next(), 'page' : page + 1},
			'has_previous' : {'bool' :  p.has_previous(), 'page' : page -1},
            'pages_list':range(1,paginator.num_pages + 1 ),
			'num_pages': paginator.num_pages,
			}
	except (EmptyPage,PageNotAnInteger):
		raise Http404


def captcha_check_or_404( token_key ):
    if ( settings.IS_ON_TEST ):
        return
    if ( token_key ):
        data = {
        'response': token_key,
        'secret': settings.RECAPTCHA_SECRET_KEY,
        }
        resp = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data, timeout = 3000 )
        result_json = resp.json()
        if not result_json.get('success'):
            raise Http404
        return True
    raise Http404

# Create your views here.

#repeated data



class HomeView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request ):

        soon_trainings = Training.objects.filter( dates__start_date__gte = timezone.now() ).annotate(dates__start_date = models.Min('dates__start_date')).order_by('dates__start_date').distinct()[0:4]
        response = {
            "soon_trainings": soon_trainings,
            "testimonials" : Testimonial.objects.filter( is_at_home = True )[0:3],
            "clients" : Client.objects.filter( is_at_home = True ),
            "articles" :Article.objects.filter( is_at_home = True )[0:6],
        }

        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        response.update(base_data)
        return render(request, 'home.html', response)
    #catalogue request
    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post( self, request ):
        captcha_check_or_404(request.POST.get('token_key'))
        form = CatalogEmailForm( request.POST )
        if ( form.is_valid() ):
            form = form.save( commit = False )
        else:
            return JsonResponse( status = 400, data = form.errors )

        subject = 'profitez de notre catalogue ...'
        html_message = render_to_string('emails/catalog.html',{'catalogue_url':settings.CATALOGUE_URL})
        plain_message = strip_tags(html_message)
        from_email = 'internationalbba@topnet.tn'
        to = request.POST.get('email')
        try:
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except BadHeaderError:
            return JsonResponse( status = 500, data = {'message':'There is a technical problem !'})
        form.save()
        return JsonResponse( status = 201, data = {'message':'Thanks for your registration'})

class ServiceView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request, service_slug ):
        if service_slug == "inter-entreprises":
            modules = Module.objects.all()
            response = {
                'modules': modules,
            }

            base_data = {
                "base_modules" : Module.objects.all().order_by("?")[0:6],
                "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
            }
            response.update( base_data )
            return render(request, 'services/inter-entreprises.html', response)
        if service_slug == "consulting":
            base_data = {
                "base_modules" : Module.objects.all().order_by("?")[0:6],
                "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
            }
            return render(request, 'services/consulting.html', base_data)
        if service_slug == "intra-entreprises":
            base_data = {
                "base_modules" : Module.objects.all().order_by("?")[0:6],
                "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
            }
            return render(request, 'services/intra-entreprises.html', base_data)

        raise Http404


class ContactView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request ):
        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        if ( request.GET.get('subject') ):
            base_data['subject'] = request.GET['subject']
        return render(request, "contact_us.html", base_data)

    @ratelimit(key='ip', rate='2/d', method='POST', block=True)
    def post( self , request):
        captcha_check_or_404(request.POST.get('token_key'))
        form =  ContactForm( request.POST )
        if  form.is_valid():
            form.save()
            return JsonResponse( status = 201, data = {'message':'Thanks for your registration'} )
        return JsonResponse( status = 400, data = form.errors )

class TrainingView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request, slug ):
        training = getObjectOr404( obj = Training, slug = slug )
        try:
            dates = training.formated_date
        except ValueError:
            raise Http404
        try:
            related = training.module_training.first().trainings.exclude( Q(id = training.id) | Q( dates__start_date__lt = timezone.now() )  )
        except:
            related = None
        response = {
            "title" : training.title,
            "id":training.id,
            "image" : training.formated_image,
            "description" : training.description,
            "duration" : training.duration,
            "date" : dates['date'],
            "dates" : dates['dates'],
            "modules" : training.module_training.all().values("title","slug"),
            "related":related,
        }

        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        response.update(base_data)
        return render(request, "training.html", response )

    #training registration view
    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post( self, request ):
        captcha_check_or_404(request.POST.get('token_key'))
        form =  RegistrationForm(request.POST)
        if  form.is_valid():
            registration = form.save( commit = False )
        else:
            return JsonResponse( status = 400, data = form.errors )
        str_  = string.digits + string.ascii_letters  + request.POST.get('first_name')
        key = ''.join(random.SystemRandom().choice(str_) for _ in range(20))
        while (  Registration.objects.filter(verification_key=key).exists() ):
	        key = ''.join(random.SystemRandom().choice(str_) for _ in range(20))


        subject = 'Vérifiez votre e-mail'
        html_message = render_to_string('emails/email_verifie.html',{'url':'{}/registration/verifie/{}'.format( settings.NOW_HOST,key ) })
        plain_message = strip_tags(html_message)
        from_email = 'From IBBA@topnet.com'
        to = request.POST.get('email')
        try:
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except BadHeaderError:
            return JsonResponse( status = 500, data = {'message':'There is a technical problem !'})
        registration.verification_key = key
        registration.save()
        return JsonResponse( status = 201, data = {'message':'Thanks for your registration'} )


@ratelimit(key='ip', rate='10/h', method='GET', block=True)
def TrainingRegistrationVerification( request, key ):
    if ( request.method == "GET" ):
        try:
            registration  = Registration.objects.get(verification_key = key, is_verified = False )
        except Registration.DoesNotExist:
            raise Http404
        registration.is_verified = True
        registration.save()
        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        return render(request,'emails/email_verified.html',base_data)
    raise Http404


class ModuleView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request, slug ):
        module = getObjectOr404( Module, slug = slug )
        trainings_not_realized = module.trainings.filter( dates__start_date__gte = timezone.now() ).annotate(dates__start_date = models.Min('dates__start_date')).order_by('dates__start_date').distinct()
        response = {
            'title' : module.title,
            'parent_module': get_parent_module( module.parent_module ),
            'logo'  : module.formated_logo,
            'description' : module.description,
            'count' : trainings_not_realized.count(),
            'trainings_not_realized':trainings_not_realized ,
        }
        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        response.update(base_data)
        return render(request, 'module.html', response)

class TrainingsView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request ):

        search_word = request.GET.get('search_word')
        # filter_by  = request.GET.get('filter_by')
        date_min = request.GET.get('date_from')
        date_max = request.GET.get('date_to')

        queries = []
        if ( not(validate_date(date_min) and validate_date(date_max)) ):
            date_min, date_max = None, None
        if ( (date_min and date_max)  ): #and filter_by != "f-r"
            queries.append(Q(dates__start_date__gte = date_min))
            queries.append(Q(dates__end_date__lte = date_max))

        # filter_by ( formations realizer (en cour ) ou non )
        # if ( filter_by == "f-r" and not ( date_max  or date_min ) ):
        #     queries.append(Q( dates__start_date__lte = timezone.now()))
        # # elif ( filter_by == "f-n-r" and not ( date_max  or date_min ) ):
        # else:
        queries.append(Q( dates__start_date__gte = timezone.now()))


        #filter by search_word
        queries2 = []
        if ( search_word ):
            words = search_word.split(' ')
            for i in words:
                queries2.append( Q( title__icontains = i ) )
            #filter
            if ( date_max and date_min ):
                trainings = Training.objects.filter( reduce( operator.and_, queries ) , reduce( operator.and_, queries2 ) ).order_by('dates__start_date').distinct()
            else:
                trainings = Training.objects.filter( reduce( operator.and_, queries ) , reduce( operator.and_, queries2 ) ).annotate(dates__start_date = models.Min('dates__start_date')).order_by('dates__start_date').distinct()
        else:
            #filter
            if ( date_max and date_min ):
                trainings = Training.objects.filter( reduce( operator.and_, queries ) ).order_by('dates__start_date').distinct()
            else:
                trainings = Training.objects.filter( reduce( operator.or_, queries)  ).annotate(dates__start_date = models.Min('dates__start_date')).order_by('dates__start_date').distinct()
        try:
            page = int(request.GET.get('page')) if request.GET.get('page') else 1
        except ValueError:
            raise Http404
        response = Pagination(trainings, 12,  page)
        if ( search_word ):
            response['search_word'] = search_word
        # if ( filter_by ):
        #     response['filter_by'] = filter_by
        if ( date_min ):
            response['date_from'] = date_min
        if ( date_max ):
            response['date_to'] = date_max
        response["modules"] = Module.objects.all().order_by("?")

        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        response.update(base_data)
        return render( request, "trainings.html", response )

class ModulesView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request ):
        filter_by = request.GET.get('filter_by')
        if ( filter_by == 'm-f' or filter_by == 'm-t' ):
            modules = Module.objects.filter( parent_module = filter_by )

            if ( filter_by == 'm-t' ):
                response = {
                    'count_t':modules.count(),
                    'modules_t': modules
                }
            else:
                response = {
                    'count_f':modules.count(),
                    'modules_f': modules
                }
        else:
            modules_f = Module.objects.filter( parent_module = 'm-f' )
            modules_t = Module.objects.filter( parent_module = 'm-t' )

            response = {
                'modules_f': modules_f,
                'modules_t':modules_t,
                'count_f':modules_f.count(),
                'count_t':modules_t.count()
            }


        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        response.update( base_data )
        return render( request, "modules.html", response )

class PresentationView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request ):
        response = {
            'modules': Module.objects.all(),
        }

        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        response.update( base_data )
        return render( request, "presentation.html", response )

class TrainerView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get(self, request):

        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        return render(request,'trainer.html',base_data)

    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post( self, request ):
        captcha_check_or_404(request.POST.get('token_key'))
        form =  TrainerForm(request.POST, request.FILES)
        if  form.is_valid():
            trainer = form.save( commit = False )
        else:
            return JsonResponse( status = 400, data = form.errors )
        str_  = string.digits + string.ascii_letters  + request.POST.get('first_name')
        key = ''.join(random.SystemRandom().choice(str_) for _ in range(20))
        while (  Trainer.objects.filter(verification_key=key).exists() ):
	        key = ''.join(random.SystemRandom().choice(str_) for _ in range(20))


        subject = 'Vérifiez votre e-mail'
        html_message = render_to_string('emails/email_verifie.html',{'url':'{}/trainer/verifie/{}'.format( settings.NOW_HOST,key, key ) })
        plain_message = strip_tags(html_message)
        from_email = 'From IBBA@topnet.com'
        to = request.POST.get('email')
        try:
            send_mail(subject, plain_message, from_email, [to], html_message=html_message)
        except BadHeaderError:
            return JsonResponse( status = 400, data = {'message':'There is a tchnical problem !'})
        trainer.verification_key = key
        trainer.save()
        return JsonResponse( status = 201, data = {'message':'Thanks for your registration'} )


#verifie the trainer email
@ratelimit(key='ip', rate='5/h', method='GET', block=True)
def TrainerVerification( request, key ):
    if ( request.method == "GET" ):
        try:
            trainer  = Trainer.objects.get(verification_key = key, is_verified = False )
        except Trainer.DoesNotExist:
            raise Http404
        trainer.is_verified = True
        trainer.save()

        base_data = {
            "base_modules" : Module.objects.all().order_by("?")[0:6],
            "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
        }
        return render(request,'emails/email_verified.html',base_data)
    raise Http404

class ArticleView( View ):

    @ratelimit(key='ip', rate='20/h', method='GET', block=True)
    def get( self, request, slug = None ):
        if ( slug ):
            article = getObjectOr404(Article, slug = slug)
            response = {
                'article' : article,
            }

            base_data = {
                "base_modules" : Module.objects.all().order_by("?")[0:6],
                "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
            }
            response.update( base_data )
            return render( request, 'article.html', response )
        else:
            try:
                page = int(request.GET.get('page')) if request.GET.get('page') else 1
            except ValueError:
                raise Http404
            response = Pagination( Article.objects.all() , 12,  page)

            base_data = {
                "base_modules" : Module.objects.all().order_by("?")[0:6],
                "reCAPTCHA_site_key" : settings.RECAPTCHA_SITE_KEY,
            }
            response.update( base_data )
            return render( request, 'news.html', response )

class SubscriberView( View ):

    @ratelimit(key='ip', rate='10/d', method='POST', block=True)
    def post( self, request ):
        captcha_check_or_404(request.POST.get('token_key'))
        form = SubsriberForm(request.POST)
        if  form.is_valid() :
            form.save()
            return JsonResponse( status = 201, data = {'message':'Thanks for your registration'} )
        return JsonResponse( status = 400, data = form.errors )
