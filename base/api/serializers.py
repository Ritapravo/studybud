## serializers are classes that takes a certain model that we 
## want to serialize and its going to turn it into json data 
## so it basically gonna take our python object, turn it into json
## object and then we can return that

from rest_framework.serializers import ModelSerializer
from base.models import Room

class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'

