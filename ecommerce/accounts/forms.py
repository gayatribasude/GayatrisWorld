from django import forms

from .models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class VisitorForm(forms.Form):
    email = forms.EmailField()


class RegistrationForm(forms.ModelForm):
    #fullname = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control", "id": "fullname", "placeholder": "Enter Full Name"}))
    #email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control", "id": "email", "placeholder": "Enter Email Address"}))
    password1 = forms.CharField(widget=forms.PasswordInput,label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ('fullname', 'email')


    def clean_password2(self):
        password1 =self.cleaned_data.get('password1')
        password2 =self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password must match")
        return password2

    def save(self,commit=True):
        user =super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        #user.active =False
        if commit:
            user.save()
        return user

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control","id":"fullname","placeholder":"Enter Full Name"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control","id":"email","placeholder":"Enter Email Address"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control","id":"content","placeholder":"Enter your Content"}))

    def clean_email(self):
        email =self.cleaned_data.get("email")
        if not "gmail.com" in email:
            raise forms.ValidationError("Email has to be gmail.com")
        return email