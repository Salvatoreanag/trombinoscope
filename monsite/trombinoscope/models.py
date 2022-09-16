#from distutils.command.upload import upload
#import email
#from tkinter import Widget
from django.db import models

class Faculty(models.Model):
    name  = models.CharField(max_length=255)
    color = models.CharField(max_length=10)                                      # On définie la relation pplusieurs à plusieurs entre Internaute et ami 
    
    def __str__(self):
        return self.name


class Person(models.Model):
    registration_number = models.CharField(max_length=10)
    last_name           = models.CharField(max_length=255)
    first_name          = models.CharField(max_length=255)
    birth_date          = models.DateField()
    email               = models.EmailField()
    home_phone_number   = models.CharField(max_length=20)
    cellphone_number    = models.CharField(max_length=20)
    photo               = models.FileField(upload_to='photos')
    password            = models.CharField(max_length=32)
    friends             = models.ManyToManyField('self')
    faculty             = models.ForeignKey('Faculty',null=True,on_delete=models.SET_NULL)    
    person_type         = 'generic' # On ajoute cet attribut pour pouvoir reconnaître sur la page d'acceuil si l'utilisateur connecté est un etudint ou un emplpoyé

    def __str__(self):                                                                                    # Ces méthodes dans chaque classe permettent l'affichage des attributs retounés. Elles sont nécessaires      
        return self.last_name + " " + self.first_name


class Message(models.Model):
    person           = models.ForeignKey('Person',null=True,on_delete=models.SET_NULL)                  # On définie une clé étrangère nommée author qui pointe  vers internaute
    content          = models.TextField()
    publication_date = models.DateField() 

    def __str__(self):
        if len(self.content) > 20:
            return self.content[:19] + "..."
        else:
            return self.content


class Campus(models.Model):
    name    = models.CharField(max_length=100)
    address = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Job(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Cursus(models.Model):
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

class Employe(Person):
    office = models.CharField(max_length=100)
    campus = models.ForeignKey('Campus',null=True,on_delete=models.SET_NULL)
    job    = models.ForeignKey('Job',null=True,on_delete=models.SET_NULL)
    person_type = 'employe'  # Surcharge d'attribut


class Student(Person):
    year   = models.IntegerField()
    cursus = models.ForeignKey('Cursus',null=True,on_delete=models.SET_NULL)
    person_type = 'student'




# Create your models here.
