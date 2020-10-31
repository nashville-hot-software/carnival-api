from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Vehicle, VehicleType
from .vehicletype import VehicleTypeSerializer

class VehicleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vehicle
        url = serializers.HyperlinkedIdentityField(
            view_name='Vehicles',
            lookup_field='id'
        )
        fields = ('id', 'vin', 'engine_type', 'vehicle_type', 'exterior_color', 'interior_color', 'floor_price', 'msr_price', 'miles_count', 'year_of_car', 'is_sold', 'vehicle_type_id')

        depth = 1

class VehicleTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VehicleType
        url = serializers.HyperlinkedIdentityField(
            view_name='VehicleType',
            lookup_field='id'
        )
        fields = ('id', 'body_type', 'make', 'model')

class Vehicles(ViewSet):

    def create(self, request):
    
        new_vehicle = Vehicle()

        new_vehicle.name = request.data["name"]
        
        # FOR POSTMAN TESTING
        # {
        #     "vin": "1234VV7JCW910",
        #     "enginge_type": "V6",
        #     "exterior_color": "Blue",
        #     "interior_color": "Black",
        #     "floor_price": 25000,
        #     "msr_price": 22000,
        #     "miles_count": 45,
        #     "year_of_car": 2020,
        #     "is_sold": false,
        #     "vehicle_type_id": 1,
        # }


        new_vehicle.save()

        serializer = VehicleSerializer(
            new_vehicle, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            vehicle = Vehicle.objects.get(pk=pk)

            serializer = VehicleSerializer(
                vehicle, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual vehicle
        Returns:
            Response -- Empty body with 204 status code
        """
        vehicle = Vehicle.objects.get(pk=pk)

        vehicle.name = request.data["name"]
        
        vehicle.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single vehicle
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            vehicle = Vehicle.objects.get(pk=pk)
            vehicle.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except vehicle.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        vehicles = Vehicle.objects.all()
        popular_vehicles = Vehicle.objects.raw('select * from popular_vehicles;')

        limit = self.request.query_params.get('limit')
        popular_models = self.request.query_params.get('popular_models')
        

        if popular_models is not None:
            popular_vehicles = Vehicle.objects.raw('select * from popular_vehicles;')
            
            serializer = VehicleTypeSerializer(
            popular_vehicles, many=True, context={'request': request})

            return Response(serializer.data)

        elif limit is not None:
            vehicles = Vehicle.objects.all().order_by('-id')[:int(limit)]
        

        serializer = VehicleSerializer(
            vehicles, many=True, context={'request': request})


        return Response(serializer.data)
        