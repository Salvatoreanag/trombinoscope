

#from datetime import datetime
#from unittest import result
#import email

from django.shortcuts import render,redirect
from trombinoscope import forms
from trombinoscope.forms import LoginForm , AddFriendForm                    # Intégration du formulaire à la vue 
from trombinoscope.forms import StudentProfileForm,EmployeProfileForm
from trombinoscope.models import Person,Student,Employe,Message
from datetime import date
from django.http import HttpResponse
# from django import forms
# from django.core import exceptions
# from dataclasses import field



# l'objet 'request' est capital comme premier paramètre de toutes les méthodes de views.
# Puisqu'il permet d'accéder à toute les informations encapsulées dans la requête HTTP(ensemble des paramètres passés à la page web)


# On crée une fonction dont le rôle est de récupérer l'utilisateur authentifié de la base de donnée
def get_logged_user_form_request(request):
    if 'logged_user_id' in request.session:                                                                    # Si on a un id utilisateur dans la session
        logged_user_id = request.session['logged_user_id']                                                     #     On récupère l'id
        if len(Student.objects.filter(id=logged_user_id)) == 1:                                                #     Si c'est un étudiant
            return Student.objects.get(id=logged_user_id)                                                      #         On retourne l'objet etudiant qui correspond à l'id récupérer
        elif len(Employe.objects.filter(id=logged_user_id)) == 1:                                              #     Sinon si c'est un employé
            return Employe.objects.get(id=logged_user_id)                                                      #         On retourne l'objet employé qui correspond à l'id récupérer
        else:                                                                                                  #     Sinon 
            return None                                                                                        #         On retourne none
    else:                                                                                                      # Sinon
        return None                                                                                            #     On retourne none


# Connexion d'une personne(On utilisera les sessions et et les cookies lors de la connexion)
def login(request):
    if len(request.POST)>0:                                                                                    # Si le formulaire est envoyé (Si oui taille > 0)
        form = LoginForm(request.POST)                                                                         #      On crée un objet form qui représente un dictionnaire contenant les attributs de la classe LoginForm
        if form.is_valid():                                                                                    #      Si le formulaire est valide( is_valid vérifie surtout si l'email est valide)
            # Enregistrement de l'utlisateur authentifié(Usage des sessions)
            user_email  = form.cleaned_data['email']                                                           #          On récupère à partir du formulaire d'authentification l'email que l'utilisateur à introduite
            logged_user = Person.objects.get(email=user_email)                                                 #          On récupère ensuite dans la bdd l'objet Person dont l'email correspond à l'email récupérer précédemment
            request.session['logged_user_id'] = logged_user.id                                                 #          On sauvergarde ensuite dans la session l'id de cette personne
            # Fin d'enregistrement de l'utlisateur authentifié
            return redirect('/welcome')                                                                        #          On le redirige vers la page d'acceuil
        else:                                                                                                  #      Sinon
            return render(request,'login.html',{'form':form})                                                  #          On renvoie la page de connexion
    else:                                                                                                      # Sinon
        form = LoginForm()                                                                                     #      On crée un objet form
        return render(request,'login.html',{'form':form})                                                      #      Et on renvoie la page de connexion



# Enrégistrement d'une personne
def register(request):
    if len(request.POST) > 0 and 'profileType' in request.POST:                                                # Si un formulaire est envoyé et que le type du profile est précisé
        studentForm = StudentProfileForm(prefix="st")                                                          #     On crée le modelForm vierge de l'étudiant
        employeForm = EmployeProfileForm(prefix="em")                                                          #     On crée le modelForm vierge de l'employé ( Comme la plupart des champs sont communs aux deux Le prefixage évite à Django de créer des id du même nom(de différencier les champs))
        if request.POST['profileType'] == 'student':                                                           #     Si c'est le formulaire de l'étudiant qui est soumis
            studentForm = StudentProfileForm(request.POST,request.FILES,prefix="st")                           #         On initialise le modelForm de l'étudiant aux données reçues(request.FILES est nécessaire si on récuppère les fichiers)
            if studentForm.is_valid():                                                                         #         Si les données sont valides
                studentForm.save()                                                                             #             On  les sauvegarde 
                return redirect('/login')                                                                      #             On le redirige vers la page de connexion 
        elif request.POST['profileType'] == 'employe':                                                         #     Sinon si c'est le formulaire de l'employé qui est soumis
            employeForm = EmployeProfileForm(request.POST,request.FILES,prefix="em")                           #         On initialise le modelForm de l'employé aux données reçues
            if employeForm.is_valid():                                                                         #         Si les données sont valides
                employeForm.save()                                                                             #              On  les sauvegarde
                return redirect('/login')                                                                      #              On le redirige vers la page de connexion 
        return render(request,'user_profile.html',{'studentForm':studentForm,'employeForm':employeForm})       #     On lui renvoie la page de création de compte 
    else:                                                                                                      # Sinon
        studentForm = StudentProfileForm(prefix="st")                                                          #     On crée le modelForm vierge de l'étudiant
        employeForm = EmployeProfileForm(prefix="em")                                                          #     On crée le modelForm vierge de l'étudiant
        return render(request,'user_profile.html',{'studentForm':studentForm,'employeForm':employeForm})       #     On lui renvoie la page de création de compte 
        

# Page d'acceuil
def welcome(request):
    logged_user = get_logged_user_form_request(request)
    if logged_user:
        if 'newMessage' in request.POST and request.POST['newMessage'] != '':                                               # Si le dictionnaire contient un nouveau message et qu'il st non vide                                                
            newMessage = Message(person=logged_user,content=request.POST['newMessage'],publication_date=date.today())       #     On crée un objet message en initialisant tous ses champs
            newMessage.save()                                                                                               #     On le sauvegarde
        friendMessages = Message.objects.filter(person__friends=logged_user).order_by('-publication_date')                  # On crée un objet message auquel on applique un filtre qui signifie que "tous les messages dont un des amis de l'auteur du message est l'utilisateur authentifié.Les messages seront affichés par ordre décroissant(du plus récent)"
        return render(request,'welcome.html',{'logged_user':logged_user,'friendMessages':friendMessages})
    else:
        return redirect('/login')


# Page d'ajout d'ami
def add_friend(request):
    logged_user = get_logged_user_form_request(request)
    if logged_user:
        if len(request.POST) > 0:
            form = AddFriendForm(request.POST)
            if form.is_valid():
                new_friend_email = form.cleaned_data['email']
                newFriend        = Person.objects.get(email=new_friend_email)
                logged_user.friends.add(newFriend)
                logged_user.save()
                return redirect('/welcome')
            else:
                return render(request,'add_friend.html',{'form':form})
        else:
            form = AddFriendForm()
            return render(request,'add_friend.html',{'form':form})
    else:
        return redirect('/login')


# On consulte un profil
def show_profile(request):
    logged_user = get_logged_user_form_request(request)
    if logged_user:
        if 'userToShow' in request.GET and request.GET['userToShow'] != '':
            user_to_show_id = int(request.GET['userToShow'])
            results         = Person.objects.filter(id=user_to_show_id)
            if len(results) == 1:
                if Student.objects.filter(id=user_to_show_id):
                    user_to_show = Student.objects.filter(id=user_to_show_id)
                else:
                    user_to_show = Employe.objects.filter(id=user_to_show_id)
                return render(request,'show_profile.html',{'user_to_show':user_to_show})
            else:
                return render(request,'show_profile.html',{'user_to_show':logged_user})
        else:
            return render(request,'show_profile.html',{'user_to_show':logged_user})
    else:
        return redirect('/login')



# On modifie le profil
def modify_profile(request):
    logged_user = get_logged_user_form_request(request)
    if logged_user:
        if len(request.POST) > 0:
            if type(logged_user) == Student:
                form = StudentProfileForm(request.POST,instance=logged_user)       # On initialise ici le modelForm aux données reçues et à la personne dont on veut modifier le profil(en l'occurrence , l'utilisateur authentifié)
            else:                                                                  # Si on omet le second paramètre, les modelForm ne sauront pas qu'il faut modifier un objet esxistant dans la bdd et en ajouteront un nouveau,créant ainsi un doublon altéré
                form = EmployeProfileForm(request.POST,instance=logged_user)
            if form.is_valid:
                form.save()
                return redirect('/welcome')
            else:
                return render(request,'modify_profile.html',{'form':form})
        else:
            if type(logged_user) == Student:
                form = StudentProfileForm(instance=logged_user)
            else:
                form = EmployeProfileForm(instance=logged_user)
            return render(request,'modify_profile.html',{'form':form})
    else:
        return redirect('/login')




# On utilise Ajax pour vérifier la validation de l'email
def ajax_check_email_field(request):
    html_to_return = ''                                                                 # On crée cette variable pour retourner le message d'erreur mais on l'initialise à vide en indiquant qu'il n'y a aucune erreur au départ
    if 'value' in request.POST:                                                         # Si le dictionnaire contient la valeur
        field = forms.EmailField()                                                      #     On crée un objet field de type email puisse que cette classe de Django implemente déjà la vallidationde l'email
        try:                                                                            #     On essaie:
            field.clean(request.POST['value'])                                          #         d'appeler la méthode clean() de la classe EmailField en lui passant en paramètre la valeur à valider
        except forms.ValidationError as ve:                                             #     On lève une exception si la validation est erronée
            html_to_return = '<ul class="errorlist">'                                   #         On crée une liste HTML
            for message in ve.messages:                                                 #         On parcourt tous les messages d'erreur
                html_to_return += '<li>' + message + '</li>'                            #              puis on prend ce qui convient
                html_to_return += '</ul>'
        if len(html_to_return) == 0:                                                    #      Si la validation s'est bien passé
            if len(Person.objects.filter(email=request.POST['value'])) >= 1:            #          On filtre la table person pour voir si l'email existe déjà
                html_to_return = '<ul class="errorlist">'                               #               Si oui on ecrit un message d'erreur
                html_to_return += '<li> Cette adresse email est déjà utilisée! </li>'
                html_to_return += '</ul>'                                               # On retourne le message
    return HttpResponse(html_to_return)












"""
#Enrégistrement d'une personne
def register(request):
    if len(request.POST) > 0:
        form = StudentProfileForm(request.POST)
        if form.is_valid():
            form.save()                                         # On sauvegarde les données
            return redirect('/login')
        else:
            return render(request,'user_profile.html',{'form':form})
    else:
        form = StudentProfileForm()
        return render(request,'user_profile.html',{'form':form})

"""




"""
def login(request): 
    if len(request.POST) > 0:                                                       # Si le formulaire est envoyé(Si oui taille >0)
            # à revoir
        if 'email' not in request.POST or 'password' not in request.POST:           #     Si l'email et le mot de passe ne sont pas dans le dictionnaire
            error = "Veuillez entrez une adresse de courriel et un mot de passe"    #         On écrit ce message d'erreur    
            return render(request,'login.html',{'error':error})                     #         Qu'on lui retourne sur la page de connexion
        else:                                                                       #     Sinon 
            email    = request.POST.get('email')                                        #         On prend l'email dans la variable email
            password = request.POST.get('password')                                    #         On prend le mot de passe dans la varible password
            if email != 'comlan@gmail.com' or password != '123456':                 #         Si l'email et le mot de passe ne correspondent pas à ces valeurs
                error = "Adresse de courriel ou Mot de passe invalide"              #             On écrit un message d'erreur 
                return render(request,'login.html',{'error':error})                 #             Qu'on lui renvoie sur la page de connexion
            else:                                                                   #         Sinon
                return redirect('/welcome')                                         #             On le redirige sur la page d'acceuil
    else:                                                                           # Sinon
        return render(request,'login.html')                                         #     On renvoie la page de conexion
    
"""

# Create your views here.
