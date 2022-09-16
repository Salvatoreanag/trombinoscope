# On crée ici les formulaires puis on les traite

from cProfile import label
import email
#from pyexpat import model

from django import forms

from trombinoscope.models import Person,Student,Employe                                                  # On l'importe puisqu'il va se connecter avec ses paramètres 


# On crée le formulaire de connexion
class LoginForm(forms.Form):  
    
    # On crée les champs                                                                       
    email    = forms.EmailField(label='Adresse email')
    password = forms.CharField(label='Mot de passe',widget=forms.PasswordInput)

    # On passe maintenant à la validation de l'email et du mot de passe
    def clean(self):                                                                           # clean() sert à retourner les champs néttoyés,c'est à dire les champs valides et convertis dant un format de donnée python
        cleaned_data = super(LoginForm,self).clean()                                           # On appelle cette même méthode au niveau de la classe parente
        email        = cleaned_data.get("email")                                               # On récupère l'email nétttoyé
        password     = cleaned_data.get("password")                                            # On récupère le mot de pase néttoyé ( Si les champs n'étaient pas valides, cleaned_data.get() retouneraient None)
        if email and password:                                                                 # Si les deux champs sont valides (différents de none)  
            result = Person.objects.filter(email=email,password=password)                      #    On filtre la base avec l'email et le password reçu
            if len(result) != 1:                                                               #    Si le résultat n'est pas unique
                raise forms.ValidationError("Adresse email ou Mot de passe invalide")    #        On retourne une erreur grâce à la méthode raise 
        return cleaned_data                                                                    # On retoune les données néttoyées


# On crée le formulaire de l'Etudiant
class StudentProfileForm(forms.ModelForm):                                                     # La class ModelForm permet d'automatiser la création du formulaire sur la base d'un modèle
    class Meta:                                                                                # Cette classe permet de configurer notre furmulaire
        model   = Student                                                                   # On doit préciser sur quel modèle il doit se baser
        exclude = ('friends',)                                                                # On exclut un champ si nécéssaire(n'oubliez jamais la virgule)
        
        

# On crée le formulaire de l'employé
class EmployeProfileForm(forms.ModelForm):
    class Meta:
        model   = Employe
        exclude = ('friends',)
        


# On crée le formulaire d'ajout d'ami
class AddFriendForm(forms.Form):
    email = forms.EmailField(label='Adresse email')
    def clean(self):
        clean_data = super(AddFriendForm,self).clean()
        email      = clean_data.get("email")
        if email:
            result = Person.objects.filter(email=email)
            if len(result) != 1:
                raise forms.ValidationError("Adresse email incorrecte")
        return clean_data











