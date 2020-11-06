from django.http import HttpResponseServerError
from django.core import serializers as Serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Vehicle, VehicleType, PopularVehicle
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
        
class PopularVehicleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = PopularVehicle
        url = serializers.HyperlinkedIdentityField(
            view_name='PopularVehicle',
            lookup_field='id'
        )
        fields = ('id', 'vehicles_sold', 'make', 'model')

class Vehicles(ViewSet):

    def create(self, request):
    
        new_vehicle = Vehicle()

        new_vehicle.vin = request.data["vin"]
        new_vehicle.engine_type = request.data["engine_type"]
        new_vehicle.exterior_color = request.data["exterior_color"]
        new_vehicle.interior_color = request.data["interior_color"]
        new_vehicle.floor_price = request.data["floor_price"]
        new_vehicle.msr_price = request.data["msr_price"]
        new_vehicle.miles_count = request.data["miles_count"]
        new_vehicle.year_of_car = request.data["year_of_car"]
        new_vehicle.is_sold = request.data["is_sold"]
        new_vehicle.vehicle_type_id = request.data["vehicle_type_id"]
        
        # FOR POSTMAN TESTING
        # {
        #     "vin": "1234VV7JCW910",
        #     "engine_type": "V6",
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
            
            serializer = PopularVehicleSerializer(
            popular_vehicles, many=True, context={'request': request})

            return Response(serializer.data)

        elif limit is not None:
            vehicles = Vehicle.objects.all().order_by('-id')[:int(limit)]
        

        serializer = VehicleSerializer(
            vehicles, many=True, context={'request': request})


        return Response(serializer.data)
        