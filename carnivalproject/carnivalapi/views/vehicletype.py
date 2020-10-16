from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import VehicleType

class VehicleTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VehicleType
        url = serializers.HyperlinkedIdentityField(
            view_name='VehicleType',
            lookup_field='id'
        )
        fields = ('id', 'body_type_id', 'make_id', 'model_id')

class VehicleTypes(ViewSet):

    def create(self, request):
    
        new_vehicletype = VehicleType()

        new_vehicletype.body_type_id = request.data["bodyTypeId"]
        new_vehicletype.make_id = request.data["makeId"]
        new_vehicletype.model_id = request.data["modelId"]

        # FOR POSTMAN TESTING
        # {
        #     "body_type_id": "BodyTypeId"
        #     "make_id": "MakeId"
        #     "model_id": "ModelId"
        # }


        new_vehicletype.save()

        serializer = VehicleTypeSerializer(
            new_vehicletype, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            vehicletype = VehicleType.objects.get(pk=pk)

            serializer = VehicleTypeSerializer(
                vehicletype, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual vehicle type
        Returns:
            Response -- Empty body with 204 status code
        """
        vehicletype = VehicleType.objects.get(pk=pk)

        vehicletype.body_type_id = request.data["bodyTypeId"]
        vehicletype.make_id = request.data["makeId"]
        vehicletype.model_id = request.data["modelId"]

        vehicletype.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single vehicletype
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            vehicletype = VehicleType.objects.get(pk=pk)
            vehicletype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except vehicletype.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        vehicletype = VehicleType.objects.all()

        serializer = VehicleTypeSerializer(
            vehicletype, many=True, context={'request': request})

        return Response(serializer.data)