from rest_framework import serializers
from .models import Duty


class DutySerializer(serializers.ModelSerializer):
    class Meta:
        model = Duty
        fields = '__all__'
        # read_only_fields = ['registered_by', 
        #                     'duty_title', 
        #                     'description', 
        #                     'registered_at', 
        #                     'created_at',
        #                     'updated_at',
        #                     'deleted_at',
        #                     ]
