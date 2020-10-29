from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import VehicleMake

class VehicleMakeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VehicleMake
        url = serializers.HyperlinkedIdentityField(
            view_name='VehicleMakes',
            lookup_field='id'
        )
        fields = ('id', 'name')

class VehicleMakes(ViewSet):

    def create(self, request):
    
        new_vehicle_make = VehicleMake()

        new_vehicle_make.name = request.data["name"]
        
        # FOR POSTMAN TESTING
        # {
        #     "name": "1234VV7JCW910",
        # }


        new_vehicle_make.save()

        serializer = VehicleMakeSerializer(
            new_vehicle_make, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            vehicle_make = VehicleMake.objects.get(pk=pk)

            serializer = VehicleMakeSerializer(
                vehicle_make, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual vehicle
        Returns:
            Response -- Empty body with 204 status code
        """
        vehicle_make = VehicleMake.objects.get(pk=pk)

        vehicle_make.name = request.data["name"]
        
        vehicle_make.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single vehicle
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            vehicle_make = VehicleMake.objects.get(pk=pk)
            vehicle_make.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except vehicle_make.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        vehicle_makes = VehicleMake.objects.all()

        limit = self.request.query_params.get('limit')

        if limit is not None:
            vehicle_makes = VehicleMake.objects.all()[:int(limit)]

        serializer = VehicleMakeSerializer(
            vehicle_makes, many=True, context={'request': request})

        return Response(serializer.data)