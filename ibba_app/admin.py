from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import *

#actions
def delete_old_dates(modeladmin, request, queryset):
    queryset.filter( start_date__lte = timezone.now() ).delete()
delete_old_dates.short_description = "Delete passed dates"


# Register your models here.



@admin.register(Date)
class DateAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    actions = (delete_old_dates,)

@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    pass
@admin.register(File)
class FileAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    pass


@admin.register(Training)
class TrainingAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( "title" ,"dates__start_date")
    exclude = ("slug","creation_date")
    filter_horizontal = ('dates',)
    list_filter = ('dates__start_date',)
    list_display = ("title", "id", "creation_date"  )

@admin.register(Module)
class ModuleAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( 'title','parent_module', )
    exclude = ("slug","creation_date",)
    filter_horizontal = ('trainings',)
    list_display = ("title", "id","creation_date"  )

@admin.register(Registration)
class RegistrationAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    list_filter = ('is_viewed', 'creation_date','is_verified',)
    search_fields = ( 'creation_date','email','training__title' )
    list_display = ("email","id","training" ,"creation_date"  )
    exclude = ("creation_date",)


@admin.register(Trainer)
class TrainerAdmin( ImportExportModelAdmin, admin.ModelAdmin ):
    list_filter = ('is_viewed', 'creation_date', 'is_verified')
    search_fields = ( 'creation_date','email' )
    list_display = ("email","id", "creation_date"  )
    exclude = ("creation_date",)

@admin.register(Contact)
class ContactAdmin( ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( 'creation_date','email' )
    list_filter = ('is_viewed','creation_date')
    list_display = ("email","id", "creation_date"  )
    exclude = ("creation_date",)


@admin.register(CatalogEmail)
class CatalogEmailAdmin( ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( 'email','creation_date' )
    list_filter = ('is_viewed','creation_date')
    exclude = ("creation_date",)
@admin.register(Subscriber)
class SubscriberAdmin( ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( 'email','creation_date' )
    list_display = ('email','id','creation_date',)
    list_filter = ('creation_date',)
    exclude = ("creation_date",)

@admin.register(Article)
class ArticleAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( 'title','creation_date' )
    list_filter = ('creation_date',)
    list_display = ("title","id", "creation_date"  )
    exclude = ("creation_date","slug")

@admin.register(Client)
class ClientAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( 'title','creation_date' )
    list_filter = ('creation_date',)
    list_display = ("title","id", "creation_date"  )
    exclude = ("creation_date",)
@admin.register(Testimonial)
class TestimonialAdmin(ImportExportModelAdmin, admin.ModelAdmin ):
    search_fields = ( 'full_name','creation_date' )
    list_filter = ('creation_date',)
    list_display = ("full_name","id", "creation_date"  )
    exclude = ("creation_date",)
