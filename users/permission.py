from rest_framework.permissions import BasePermission
from rest_framework import views, exceptions, HTTP_HEADER_ENCODING, generics
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_403_FORBIDDEN,
    HTTP_406_NOT_ACCEPTABLE,
    HTTP_200_OK, 
    HTTP_401_UNAUTHORIZED, 
    HTTP_402_PAYMENT_REQUIRED, 
    HTTP_405_METHOD_NOT_ALLOWED, 
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from duties.models import Duty
from .models import Employee


class AddApplicationPermission(BasePermission):
    """
    Return True if employee applicant has Employee role
    Upgrade applications only permitted from Employees witch have Organizations
    """
    
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_superuser:
            return True
        elif request.user.role.role_title == 'Manager':
            return True if obj.organization == request.user.organization else False
        else:
            return False



class ApproveApplicationPermission(BasePermission):
    """
    A class that grants permissions to join to 
    organizations or upgrade from employee to manager
    """
    def has_permission(self, request, view):
        return super().has_permission(request, view)
        
    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user.is_superuser:
            return True
        elif request.user.role.role_title == 'Manager':
            return True if obj.request_type == 1 else False
        else:
            return False


class AddDutyPermission(BasePermission):
    def has_permission(self, request, view):
        """
        Return `False` if registered_by has role Employe and responsible has Manager role!
        Return `True` otherwise.
        """
        registered_by_id = request.data.get('registered_by')
        responsible_id = request.data.get('responsible')

        try:
            registered_by = Employee.objects.get(id=registered_by_id)
        except:
            raise exceptions.NotFound(
            detail='Creator Employee with id {} not found'.format(registered_by_id),
            code=HTTP_404_NOT_FOUND
            )
        
        try:
            responsible = Employee.objects.get(id=responsible_id)
        except:
            raise exceptions.NotFound(
            detail='Responsible Employee with id {} not found'.format(responsible_id),
            code=HTTP_404_NOT_FOUND
            )
        if registered_by.role.role_title == 'Employee' and responsible.role.role_title == 'Manager':
            return False
        return True


class UpdateDeleteDutyPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        """
        Return `False` if registered_by has role Employe and responsible has Manager role!
        Return `True` otherwise.
        """
        
        if request.user.is_superuser:
            return True
        elif request.user.role.role_title == 'Manager':
            return True if obj.registered_by.organization == request.user.organization else False
        else:
            return False