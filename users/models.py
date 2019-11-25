from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
import datetime
import binascii
import os




class Role(SafeDeleteModel):
    """
    Describes the role of each employee. The role entity 
    was defined as class so that new roles can be added in the future

    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    role_title = models.CharField(max_length=50, verbose_name='Role Title')

    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'

    def __str__(self):
        return self.role_title



class Organization(SafeDeleteModel):
    """
    Describes the organization each employee belongs to

    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    org_name = models.CharField(max_length=50, verbose_name='Organization Name', null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = 'Organization'
        verbose_name_plural = 'Organizations'

    def __str__(self):
        return self.org_name



class Employee(AbstractUser):
    role = models.ForeignKey(Role, related_name='members', on_delete=models.CASCADE, null=True, blank=True)
    organization = models.ForeignKey(Organization, related_name='employees', on_delete=models.CASCADE, null=True, blank=True)
    
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = 'Employee'
        verbose_name_plural = "Employees"
    
    def __str__(self):
        return "{} - {}".format(self.id, self.username)
    

REQUEST_TYPES = (
    (1, 'apply for organization'),
    (2, 'promote to manager'),
)


class Application(SafeDeleteModel):
    """
    Describes two different types of applications:
    Applications can be either to assign an employee to a specific organization (request_type=1)
    or promote an employee to the manager in the organization he/she works(request_type=2)! 

    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    applicant = models.ForeignKey(Employee, related_name='applicants', on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, related_name='destinations', on_delete=models.CASCADE)
    request_type = models.IntegerField(choices=REQUEST_TYPES, default=1, null=True, blank=True)
    accepted = models.BooleanField(default=False, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    def __str__(self):
        return 'request from: {} to: {}'.format(self.applicant.username, self.organization.org_name)

    class Meta:
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'


class Token(SafeDeleteModel):
    """
    In the verification stage, a unique token key is assigned to an employee
    In the next steps the generated token is used to authenticate Employees  
    
    """
    _safedelete_policy = SOFT_DELETE_CASCADE
    key = models.CharField(max_length=40, primary_key=True)
    user = models.ForeignKey(Employee, related_name='tokens', on_delete=models.CASCADE)

    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    

    def save(self, *args, **kwargs):
        if not self.key:
            self.key = self.generate_key()
        return super().save(*args, **kwargs)

    def generate_key(self):
        return binascii.hexlify(os.urandom(20)).decode()

    def __str__(self):
        return 'user {} - token -{} ...'.format(self.user.username, self.key[:7])

    @property
    def related_user(self):
        return self.user.username

    class Meta:
        verbose_name = 'Token'
        verbose_name_plural = 'Tokens'
    
    
