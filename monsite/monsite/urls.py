"""monsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include,path
from trombinoscope import views
from trombinoscope.views import welcome,login,register,add_friend,show_profile,modify_profile,ajax_check_email_field
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',welcome,name='welcome'), # Page par défaut du site
    path('welcome/',welcome,name='welcome'),
    path('login/',login,name='login'),
    path('register/',register,name='register'),
    path('add_friend/',add_friend,name='add_friend'),
    path('show_profile/',show_profile,name='show_profile'),
    path('modify_profile/',modify_profile,name='modify_profile'),
    path('ajax/ajax_check_email_field/',ajax_check_email_field,name='ajax_check_email_field')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  # On l'ajoute si on a des fichiers à récupérer
