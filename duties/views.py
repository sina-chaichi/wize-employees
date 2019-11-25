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

from rest_framework.response import Response
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication
from users.serializers import EmployeeSerializer, ApplicationSerializer
from users.models import Employee, Role, Organization, Token, Application
from users.authentication import TokenAuthentication
from users.permission import AddDutyPermission, UpdateDeleteDutyPermission
from .models import Duty
from .serializers import DutySerializer
        

class AddDuty(generics.CreateAPIView):
    """
    This view creates a duty 

    """
    authentication_classes = [TokenAuthentication,]
    permission_classes = [AddDutyPermission,]
    queryset = Duty.objects.all()
    serializer_class = DutySerializer


class UpdateDeleteDuty(generics.RetrieveUpdateDestroyAPIView):
    """
    this view does a partial update based on two fields:
    'dead_line' and 'responsible' 
    
    """
    authentication_classes = [TokenAuthentication,]
    permission_classes = [UpdateDeleteDutyPermission,]
    queryset = Duty.objects.all()
    serializer_class = DutySerializer
