# Ce fichier permet à django d'afficher mes modèles

from django.contrib import admin

from trombinoscope.models import Faculty,Campus,Job,Cursus,Employe,Student,Message

#On va lister tous les modèles qui doivent être gérés par le site d'administration
admin.site.register(Faculty)
admin.site.register(Campus)
admin.site.register(Job)
admin.site.register(Cursus)
admin.site.register(Employe)
admin.site.register(Student)
admin.site.register(Message)















# Register your models here.
