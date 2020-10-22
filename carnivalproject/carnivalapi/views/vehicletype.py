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
        fields = ('id', 'body_type', 'make', 'model')

class VehicleTypes(ViewSet):

    def create(self, request):
    
        new_vehicletype = VehicleType()

        new_vehicletype.body_type = request.data["bodyType"]
        new_vehicletype.make = request.data["make"]
        new_vehicletype.model = request.data["model"]

        # FOR POSTMAN TESTING
        # {
        #     "body_type": "BodyType"
        #     "make": "Make"
        #     "model": "Model"
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

        vehicletype.body_type = request.data["bodyType"]
        vehicletype.make = request.data["make"]
        vehicletype.model = request.data["model"]

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