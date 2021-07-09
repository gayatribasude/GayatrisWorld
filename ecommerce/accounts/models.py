from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.


class UserManager(BaseUserManager):
    # all required fields
    def create_user(self,fullname, email, password= None,is_active=True, is_staff=False, is_admin =False):
        if not fullname:
            raise ValueError("Users must have ")
        if not email:
            raise ValueError("Users must have email address")
        if not password:
            raise ValueError("Users must have password")
        user = self.model(
            email = self.normalize_email(email)
        )
        user.set_password(password)

        user.staff = is_staff
        user.admin = is_admin
        user.save(using =self._db)
        return user

    def create_staffuser(self,fullname, email , password= None):
        user = self.create_user(fullname=fullname,email=email, password=password, is_staff=True)
        return user

    def create_superuser(self,fullname,email , password= None):
        user = self.create_user(fullname=fullname, email=email, password=password,is_staff=True,is_admin=True)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, null=False,blank=False)
    fullname = models.CharField(max_length=30, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)  #employee
    admin = models.BooleanField(default=False)  #admin
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'

#USERNAME_FIELD and password is already default required
    REQUIRED_FIELDS = ['fullname']

    objects = UserManager()

    def __str__(self):
        return self.email

    def __unicorn__(self):
        return self.user

    def get_full_name(self):
        if self.fullname:
            return self.fullname
        return self.email

    def get_short_name(self):
        pass

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self,app_label):
        return True

    @property
    def is_staff(self):

        return self.staff

    @property
    def is_admin(self):
        return self.admin



class VisitorEmail(models.Model):
    email = models.EmailField(null=False,blank=False)
    active = models.BooleanField(default=True)
    update  =models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email


class Contact(models.Model):
    fullname=models.CharField(max_length=30,null=False,blank=False)
    email=models.EmailField(null=False,blank=False)
    content=models.TextField()

    def __str__(self):
        return str(self.fullname)
