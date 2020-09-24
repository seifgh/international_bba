from django.test import TestCase
from django.test import Client as client
from django.urls import reverse
from django.core.files import File
from django.core.files.base import ContentFile





from IBBA_APP.models import *

# Create your tests here.

class TrainingTestCase( TestCase ):

    def setUp( self ):
        self.client = client()
        self.get_list_url = reverse('trainings')
        # self.create_url = reverse('create-training')
        self.get_details_url =  reverse('training',args=['gestion-1'])

        self.training_object = Training.objects.create(
            title = "gestion 1",
            image = Image.objects.create(url = "/fdggfg"),
            description = "simple desc",
            current_price = "20dt",
            duration = "5j"
        )
        self.training_object.dates.add(
         Date.objects.create(
         start_date = datetime.date(2019,12,30)
         , end_date = datetime.date(2020,12,30)
         )
        )
    def test_get_list(self):
        response = self.client.get(self.get_list_url)

        self.assertEquals( response.status_code, 200 )
        self.assertTemplateUsed( response, 'trainings.html')

    def test_get_detail(self):
        response = self.client.get(self.get_details_url)

        self.assertEquals( response.status_code, 200 )

class ModuleTestCase( TestCase ):

    def setUp( self ):
        self.client = client()
        self.get_list_url = reverse('modules')
        self.get_detail_url = reverse('module', args=['module-1'])

        self.module_object = Module.objects.create(
            title = "module 1",
            parent_module = "m-t",
            logo = File.objects.create( url = "/sample_url" ),
            description = "sample description",
        )

    def test_get_list( self ):
        response = self.client.get( self.get_list_url )

        self.assertEquals( response.status_code, 200 )


    def test_get_filter_list( self ):
        #filter list by parent module

        response = self.client.get( self.get_list_url, {'filter_by':'m-f-g'} )


        self.assertEquals( response.status_code, 200 )

    def test_get_detail( self ):
        response = self.client.get( self.get_detail_url )

        self.assertEquals( response.status_code, 200 )

class RegistrationTestCase( TestCase ):

    def setUp( self ):
        self.client = client()
        self.registration_create_url = reverse('register')
        #create training
        self.training_object = Training.objects.create(

            title = "gestion 1",
            image = Image.objects.create(url = "/fdggfg"),
            description = "simple desc",
            current_price = "20dt",
            duration = "5j"
        )
        self.training_object.dates.add(
         Date.objects.create(
         start_date = datetime.date(2019,12,30)
         , end_date = datetime.date(2020,12,30)
         )
        )
        #create registration
        self.registration_object = Registration.objects.create(
            first_name = "seif", last_name='Gharres', email="seifgharrese@gmail.com",
            phone="+216 45 678 789", training = self.training_object, verification_key = "hjgjhgjhgjhkg"
        )

    def test_create_one_with_errors( self ):
        #repeate email and trainging, wrong phone_number format
        response = self.client.post( self.registration_create_url, {
            'first_name'  :  "seif", 'last_name' : 'Gharres', 'email':"seifgharrese@gmail.com",
            'phone' : "dx 45 678 789", 'training'  : self.training_object.id ,'adress':"hhhhh"
        })
        # print(response.content)


        self.assertEquals( response.status_code, 400 )
    def test_create_one_without_errors( self ):
        response = self.client.post( self.registration_create_url, {
            'first_name'  :  "seif", 'last_name' : 'Gharres', 'email':"seifgharrese2@gmail.com",
            'phone' : "+216 45 678 789", 'training'  : self.training_object.id ,'adress':"hhhhh"
        })

        self.assertEquals( response.status_code, 201 )

    def test_verify_registration_with_wrong_key( self ):
        response = self.client.get( reverse( 'verify-registration', args=['kkhjkhjkh'] )  )

        self.assertEquals( response.status_code, 404 )

    def test_verify_registration_with_right_key( self ):
        response = self.client.get( reverse( 'verify-registration', args=[self.registration_object.verification_key] )  )

        self.assertEquals( response.status_code, 200 )


class TrainerTestCase( TestCase ):
    def setUp( self ):
        self.client = client()
        self.trainer_url = reverse('trainer') #create && get
        with open("/home/seif/Desktop/IBBA_Web_Application/IBBA_SERVER/IBBA_APP/tests/cv.png","r") as f:
            self.trainer_object = Trainer.objects.create(
                first_name   =   "seif", last_name  =  'Gharres', email = "seifgharrese2@gmail.com",
                phone  =  "+216 45 678 789",  profession = "hhhhh" , cv  =  ContentFile(f.read()),
                verification_key = "dfgdf_çègdfg"
            )

    def test_create_one_with_errors( self ):
        #repeate email , wrong file format format
        with open("/home/seif/Desktop/IBBA_Web_Application/IBBA_SERVER/IBBA_APP/tests/cv.cv","r") as f:
            response = self.client.post( self.trainer_url, {
                'first_name'  :  "seif", 'last_name' : 'Gharres', 'email':"seifgharrese2@gmail.com",
                'phone' : "dx 45 678 789",'profession':"hhhhh",
                'verification_key':"jkgkhgkhghghkg", 'cv':f
            })
        # print(response.content)


        self.assertEquals( response.status_code, 400 )
    def test_create_one_without_errors( self ):
        with open("/home/seif/Desktop/IBBA_Web_Application/IBBA_SERVER/IBBA_APP/tests/cv.png") as f:
            response = self.client.post( self.trainer_url, {
                'first_name'  :  "seif", 'last_name' : 'Gharres', 'email':"seifgharrese@gmail.com",
                'phone' : "+216 45 678 789",'profession':"hhhhh",
                'cv' : f
            })

        self.assertEquals( response.status_code, 201 )

    def test_verify_registration_with_wrong_key( self ):
        response = self.client.get( reverse( 'verify-trainer', args=['kkhjkhjkh'] )  )

        self.assertEquals( response.status_code, 404 )

    def test_verify_registration_with_right_key( self ):
        response = self.client.get( reverse( 'verify-trainer', args=[self.trainer_object.verification_key] )  )

        self.assertEquals( response.status_code, 200 )

class ContactTestCase( TestCase ):
    def setUp( self ):
        self.client = client()
        self.contact_url = reverse('contact')
        self.contact_object = Contact.objects.create(
            first_name = "seif", last_name = "gharres" , email = "seifgharrese2@gmail.com",
            phone = "+216 45 678 789", subject = "Hidfgfdg", message = "hhhhhhhhhhh",
        )

    def test_create_one_with_errors( self ):
        #repeate email and trainging, wrong phone_number format
        response = self.client.post( self.contact_url, {
            'first_name'  :  "seif", 'last_name' : 'Gharres', 'email':"seifgharrese2@gmail.com",
            'phone' : " 4cf5 678 789",'subject':"hhhhh",
        })
        # print(response.content)
        self.assertEquals( response.status_code, 400 )

    def test_create_one_without_errors( self ):
        response = self.client.post( self.contact_url, {
            'first_name'  :  "seif", 'last_name' : 'Gharres', 'email':"seifgharqrese@gmail.com",
            'phone' : "+216 45 678 789",'subject':"hhhhh",
        })
        self.assertEquals( response.status_code, 201 )

class CatalogueEmailTestCase( TestCase ):
    def setUp( self ):
        self.client = client()
        self.url = reverse('home')

    def test_send__mail_create_with_errors( self ):
        response = self.client.post( self.url, {'email':'seifgarre dse2@gmail.com'}  )

        self.assertEquals( response.status_code, 400 )

    def test_send__mail_create_without_errors( self ):
        response = self.client.post( self.url, {'email':'seifgarrese2@gmail.com'}  )

        self.assertEquals( response.status_code, 201 )



class SubscriberTestCase( TestCase ):

    def setUp( self ):
        self.client = client()
        self.url = reverse('subscribe')

    def test_create_subscribe_with_errors( self ):
        response = self.client.post( self.url, {'email': 'seifg arrese2@gmail.com'} )

        self.assertEquals( response.status_code, 400 )

    def test_create_subscribe_without_errors( self ):
        response = self.client.post( self.url, {'email':'seifgarrese2@gmail.com'}  )

        self.assertEquals( response.status_code, 201 )
