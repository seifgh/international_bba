from django.db import models
from django.db.models import Model, CASCADE, CharField, EmailField, SlugField, IntegerField, PositiveIntegerField, DecimalField, PositiveSmallIntegerField, TextField, ForeignKey, URLField, BooleanField, DateTimeField, DateField, OneToOneField, ManyToManyField, ImageField, FileField
from django.contrib.auth.models import User
from django.db.models import Max, Min, Sum, Avg
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.utils.timezone import localdate
from django.template.defaultfilters import slugify
from django.core.exceptions import ValidationError
from django.conf import settings
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


# --------------------------constants--------------------------------------
modules = (
    ('m-f', 'Module fonctionnel'),
    ('m-t', 'Module technique'),

)

# --------------------------Usefull Models---------------------------------


class File(Model):
    """ Tableau pour facilite l'utilisation """

    url = URLField(blank=True)
    file = FileField(upload_to='files', blank=True)

    def clean(self):
        if (not(self.url or self.file)):
            raise ValidationError("Two fields are emplty, at lease fill one !")

    @property
    def formated_file_url(self):
        if (self.url):
            return self.url
        else:
            return self.file.url

    @property
    def formated_file_name(self):
        if (self.url):
            return self.url
        else:
            return self.file.name

    def __str__(self):
        if (self.url):
            return self.url
        else:
            return self.file.name


class Image(Model):
    """ Tableau pour facilite l'utilisation """

    url = URLField(blank=True)
    image = ImageField(upload_to="images", blank=True)

    def clean(self):
        if (not(self.url or self.image)):
            raise ValidationError("Two fields are emplty, at lease fill one !")

    def __str__(self):
        if (self.image):
            return self.image.url
        else:
            return self.url


class Date(Model):

    start_date = DateField()
    end_date = DateField()

    class Meta:
        ordering = ('start_date',)

    def clean(self):
        if (self.start_date > self.end_date):
            raise ValidationError(
                {'start_date': "Error end date should be less than start date"})

    def __str__(self):
        return "Du ( {}  )  à  ( {} )".format(self.start_date.strftime("%d / %m , %Y"), self.end_date.strftime("%d / %m , %Y"))

# class AplicationStaticData( Model ):


# --------------------------Base Models---------------------------------

class Training(Model):
    """ Tableau d'une formation d'un module """

    title = CharField(max_length=80, unique=True)
    image = ForeignKey(Image, related_name="training_image",
                       on_delete=CASCADE, blank=True)
    slug = SlugField(max_length=80, unique=True)  # Pour assurer le lien ( url)
    description = RichTextUploadingField(null=True)

    # Tarif (prix courants)
    current_price = CharField(max_length=20, blank=True)
    duration = CharField(max_length=10)
    dates = ManyToManyField(Date)

    creation_date = DateTimeField(default=timezone.now)  # for ordering

    class Meta:
        ordering = ('creation_date',)
    # unique_together = (("color","size","brand",'model_ref'),)

    @property
    def formated_image(self):
        if (self.image.url):
            return self.image.url
        else:
            return self.image.image.url

    @property
    def formated_date(self):
        # if ( not self.dates.all().exists() ):
        #     raise ValueError("No Dates")
        now = localdate()
        dates = [d for d in self.dates.all() if d.start_date >= now]
        if (not dates):
            raise ValueError("No Dates")
        # get the minimimun date
        else:
            min_date = dates[0]
            for d in dates:
                if (min_date.start_date > d.start_date):
                    min_date = d
            dates.remove(min_date)
        return {'dates': dates, 'date': min_date}

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # self.title = self.title[0].upper() + self.title[1:].lower()
        super(Training, self).save(*args, **kwargs)

    def __str__(self):
        return self.title


class Module(Model):
    """ Tableau d'un module d'un module parent """

    title = CharField(max_length=80, unique=True)
    parent_module = CharField(max_length=10, choices=modules)
    slug = SlugField(max_length=80, unique=True)  # Pour assurer le lien ( url)
    description = TextField(max_length=200, blank=True)
    logo = ForeignKey(File, related_name="module_logo",
                      on_delete=CASCADE, blank=True)
    # Un Module admet plusieurs formations
    trainings = ManyToManyField(
        Training, related_name="module_training", blank=True)

    creation_date = DateTimeField(default=timezone.now)  # for ordering

    class Meta:
        ordering = ('creation_date', )

    @property
    def formated_logo(self):
        if (self.logo.url):
            return self.logo.url
        else:
            return self.logo.file.url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        # self.title = self.title[0].upper() + self.title[1:].lower()
        super(Module, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

# Inscription Model


class Registration(Model):
    """ Tableau d'inscription a une formation """

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = EmailField()
    phone = CharField(max_length=20)
    # relation avec tableau des formation
    training = ForeignKey(Training, related_name="training", on_delete=CASCADE)
    adress = CharField(max_length=50)
    message = TextField(max_length=300, blank=True)
    price_demanded = BooleanField(default=False)

    verification_key = CharField(max_length=20, blank=True)
    is_verified = BooleanField(default=False)
    # Pour assurer le filtrage des données
    is_viewed = BooleanField(default=False)

    creation_date = DateTimeField(default=timezone.now)  # for ordering

    class Meta:
        ordering = ('creation_date', )
        unique_together = (('email', 'training'),)

    def clean(self):
        phone = self.phone[1:].replace(' ', '')
        try:
            int(phone)
            if (len(phone) < 7 or len(phone) > 14):
                raise ValidationError({'phone': "Invalid phone number"})
        except ValueError:
            raise ValidationError({'phone': "Invalid phone number"})

    def __str__(self):
        return self.first_name + " " + self.last_name


# Formateur model
class Trainer(Model):
    """ Tableau d'inscription d'un formateur """

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = EmailField(unique=True)
    phone = CharField(max_length=20)
    cv = FileField(upload_to="cvs")
    profession = CharField(max_length=50)
    message = TextField(max_length=300, blank=True)

    verification_key = CharField(max_length=20, blank=True, unique=True)
    is_verified = BooleanField(default=False)
    # Pour assurer le filtrage des données
    is_viewed = BooleanField(default=False)

    creation_date = DateTimeField(default=timezone.now)  # for ordering

    class Meta:
        ordering = ('creation_date', )

    def clean(self):
        errors = {}
        phone = self.phone[1:].replace(' ', '')
        try:
            int(phone)
            if (len(phone) < 7 or len(phone) > 14):
                errors['phone'] = "Invalid phone number"
        except ValueError:
            errors['phone'] = "Invalid phone number"

        if (self.cv):
            if (self.cv.size > settings.MAX_FILE_SIZE or self.cv.name[-3:] not in settings.AUTORIZED_TYPES):
                errors['cv'] = "Invalid file"
        if (errors):
            raise ValidationError(errors)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Contact(Model):
    """ Tableau des contact entre les clients et l'entreprise  """

    first_name = CharField(max_length=50)
    last_name = CharField(max_length=50)
    email = EmailField(unique=True)
    phone = CharField(max_length=20)
    subject = CharField(max_length=50)
    message = TextField(max_length=200, blank=True)

    # Pour assurer le filtrage des données
    is_viewed = BooleanField(default=False)

    creation_date = DateTimeField(default=timezone.now)  # for ordering

    class Meta:
        ordering = ('creation_date', )

    def clean(self):
        phone = self.phone[1:].replace(' ', '')
        try:
            int(phone)
            if (len(phone) < 7 or len(phone) > 14):
                raise ValidationError({'phone': "Invalid phone number"})
        except ValueError:
            raise ValidationError({'phone': "Invalid phone number"})

    def __str__(self):
        return self.first_name + self.last_name


class CatalogEmail(Model):
    email = EmailField()

    is_viewed = BooleanField(default=False)

    creation_date = DateTimeField(default=timezone.now)  # for ordering

    class Meta:
        ordering = ('creation_date', )

    def __str__(self):
        return self.email


class Subscriber(Model):
    email = EmailField(unique=True)
    creation_date = DateTimeField(default=timezone.now)  # for ordering

    class Meta:
        ordering = ('creation_date', )

    def __str__(self):
        return self.email


class Article(Model):
    title = CharField(max_length=50, unique=True)
    slug = SlugField(max_length=50, unique=True)
    description = RichTextUploadingField()
    main_image = ForeignKey(
        Image, related_name="image_article", on_delete=CASCADE)
    creation_date = DateTimeField(default=timezone.now)  # for ordering
    is_at_home = BooleanField(default=False)

    class Meta:
        ordering = ('creation_date', )

    @property
    def formated_image(self):
        if (self.main_image.url):
            return self.main_image.url
        else:
            return self.main_image.image.url

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        self.title = self.title[0].upper() + self.title[1:].lower()
        super(Article, self).save(*args, **kwargs)


class Client(Model):
    title = CharField(max_length=50)
    logo = ForeignKey(File, related_name="client_logo", on_delete=CASCADE)
    email = EmailField(unique=True)
    is_at_home = BooleanField()

    creation_date = DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('creation_date', )

    @property
    def formated_logo(self):
        if (self.logo.url):
            return self.logo.url
        else:
            return self.logo.file.url

    def __str__(self):
        return self.title


class Testimonial(Model):
    full_name = CharField(max_length=50)
    email = EmailField(unique=True)
    profession = CharField(max_length=50)
    image = ForeignKey(Image, related_name="testimonial_image",
                       on_delete=CASCADE, blank=True)
    message = TextField()
    is_at_home = BooleanField()

    creation_date = DateTimeField(default=timezone.now)

    class Meta:
        ordering = ('creation_date', )

    @property
    def formated_image(self):
        if (self.image.url):
            return self.image.url
        else:
            return self.image.image.url

    def __str__(self):
        return self.full_name
