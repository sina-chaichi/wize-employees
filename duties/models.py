from django.db import models
from django.utils import timezone
from safedelete.models import SafeDeleteModel, SOFT_DELETE_CASCADE
import datetime

from users.models import Employee




class Duty(SafeDeleteModel):
    """
    Describes a duty that an employee defines for himself/herself or
    or a duty that a manager assigned to an employee
    
    """
    _safedelete_policy = SOFT_DELETE_CASCADE

    responsible = models.ManyToManyField(Employee, related_name='assigned_duties')
    registered_by = models.ForeignKey(Employee, related_name='registered_duties', on_delete=models.Case, null=True, blank=True)

    duty_title = models.CharField(max_length=50, verbose_name='Role Title')
    description = models.TextField(null=True, blank=True)
    
    registered_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    dead_line = models.DateTimeField(default=timezone.now, null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_at = models.DateTimeField(default=timezone.now, null=True, blank=True)
    deleted_at = models.DateTimeField(default=timezone.now, null=True, blank=True)

    class Meta:
        verbose_name = 'Duty'
        verbose_name_plural = 'Duties'

    def __str__(self):
        return '{} - {}'.format(self.id, self.duty_title)
