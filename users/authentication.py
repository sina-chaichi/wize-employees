from rest_framework import HTTP_HEADER_ENCODING, exceptions
from safedelete.models import SafeDeleteModel
from safedelete.models import SOFT_DELETE_CASCADE
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
    HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE,
)

from .models import Token, Employee
import hashlib


class TokenAuthentication:

    keyword = 'Token'
    model = None

    def get_model(self):
        if self.model is not None:
            return self.model
        from .models import Token
        return Token

    def authenticate(self, request):
        token = request.headers.get('token')
        # username = request.data.get('username')
        if not token:
            return None
        return self.authenticate_credentials(token)



    def authenticate_credentials(self, token):
        model = self.get_model()
        try:
            token_model = model.objects.select_related('user').get(key=token)
        except:
            raise exceptions.NotFound(
                detail="Token for this user doesn't exist!",
                code=HTTP_404_NOT_FOUND)

        if token_model.key == token:
            return (token_model.user, token)
        else:
            raise exceptions.AuthenticationFailed('Invalid token!')

    def authenticate_header(self, request):
        return self.keyword






        
class HashAuthentication:

    def has_permission(self, request, view):

        sent_hash = request.headers.get("hash")
        right_hash = hash_function(request)
        print(sent_hash)
        print(right_hash)
        
        return bool(right_hash == sent_hash)