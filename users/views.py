from rest_framework import views, generics, exceptions, HTTP_HEADER_ENCODING
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

from .serializers import EmployeeSerializer, ApplicationSerializer
from .models import Employee, Role, Organization, Token, Application
from .authentication import TokenAuthentication
from .permission import AddApplicationPermission, ApproveApplicationPermission, UpdateDeleteDutyPermission




class RegisterEmployee(views.APIView):

    """
    This view recieves username and password then creates 
    an Employee associated with these parameters 
    
    """

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            current_employee = Employee.objects.create_user(
                username=username,
                password=password
            )
        except:
            raise exceptions.AuthenticationFailed(
                detail="Username '{}' already exists!".format(username),
                code=HTTP_403_FORBIDDEN
                ) 

        initial_role, _ = Role.objects.get_or_create(role_title='Employee')
        current_employee.role = initial_role
        current_employee.save()

        employee_serializer = EmployeeSerializer(current_employee)
        return Response({"meta": {
                        "error": None,
                        "message": "Employee created successfully"
                             },
                     "body": {
                         "employee": employee_serializer.data,
                             }
                    },
                    status=HTTP_200_OK)



class VerifyEmployee(views.APIView):
    """
    This view assign a unique token to the employee created in the previous step 

    """
    def put(self, request):
        username = request.data.get('username')
        try:
            current_employee = Employee.objects.get_by_natural_key(username=username)
        except:
            raise exceptions.NotFound(
                detail="Employee with username '{}' not found!".format(username),
                code=HTTP_404_NOT_FOUND) 

        token, _ = Token.objects.get_or_create(user=current_employee)
        current_employee.is_staff = True
        current_employee.save()
        employee_serializer = EmployeeSerializer(current_employee)
        return Response({"meta": {
                        "error": None,
                        "message": "Employee upgraded to staff!"
                             },
                     "body": {
                         "employee": employee_serializer.data,
                             }
                    },
                    status=HTTP_200_OK)




 
class ListCreateApplication(generics.ListCreateAPIView):
    """
    This view deals with applications:
    post method: creates an application based on request_type recieved from user
    get method: retrieve a list of applications only to the superuser
    or the manager based on their access permissions
    
    """
    authentication_classes=[TokenAuthentication,]
    permission_classes = [AddApplicationPermission,]
    
    serializer_class = ApplicationSerializer
    def get_queryset(self):
        """
        This view should return a list of all the applications related to
        the user depend on permission level.
        """
        user = self.request.user
        if user.is_superuser:
            return Application.objects.all()
        elif user.role.role_title == 'Manager':
            return Application.objects.filter(organization=user.organization)
        else:
            return None



class ApproveApplication(views.APIView):
    """
    This view approves the applications. Based on the request_type,
    either assign an employee to a specific organization or
    promotes an employee to the manager
 
    """
    authentication_classes=[TokenAuthentication,]
    permission_classes = [ApproveApplicationPermission,] 

    def post(self, request):
            application_id = request.data.get('application_id')
            current_employee = request.user

            try:
                current_application = Application.objects.get(id=application_id)
            except:
                raise exceptions.NotFound(
                    detail="Application with id '{}' not found!".format(application_id),
                    code=HTTP_404_NOT_FOUND)
            applicant = current_application.applicant

            if current_application.request_type == 1:
                applicant.organization = current_application.organization
                applicant.save()
                current_application.accepted = True
                current_application.save()

            elif current_application.request_type == 2:
                applicant.role = Role.objects.get(role_title='Manager')
                applicant.save()
                current_application.accepted = True
                current_application.save()

            else:
                raise exceptions.NotAcceptable(
                    detail="Application with request_type '{}' not acceptable!".format(
                        REQUEST_TYPE[current_application.request_type-1][1]
                        ),
                    code=HTTP_406_NOT_ACCEPTABLE)

            applicant_serializer = EmployeeSerializer(applicant)
            application_serializer = ApplicationSerializer(current_application)
            return Response({"meta": {
                            "error": None,
                            "message": "Request approved!"
                                },
                        "body": {
                            "employee": applicant_serializer.data,
                            "application": application_serializer.data,
                                }
                        },
                        status=HTTP_200_OK)   


class UpdateEmployeeOrganization(generics.RetrieveUpdateAPIView):
    """
    This view removes an employee from an organization or 
    demotes a manger to simple employee

    """
    authentication_classes=[TokenAuthentication,]
    permission_classes = [UpdateDeleteDutyPermission,]

    serializer_class = EmployeeSerializer
    queryset = Employee.objects.all()



