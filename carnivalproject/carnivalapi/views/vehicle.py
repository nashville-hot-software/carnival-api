from django.http import HttpResponseServerError
from django.core import serializers as Serializers
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Vehicle, VehicleType
from .vehicletype import VehicleTypeSerializer
from django.db import connection
import string
import random


class VehicleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Vehicle
        url = serializers.HyperlinkedIdentityField(
            view_name='Vehicles',
            lookup_field='id'
        )
        fields = ('id', 'vin', 'engine_type', 'vehicle_type', 'exterior_color', 'interior_color',
                  'floor_price', 'msr_price', 'miles_count', 'year_of_car', 'is_sold', 'vehicle_type_id')

        depth = 1


# class PopularVehicleSerializer(serializers.HyperlinkedModelSerializer):

#     class Meta:
#         model = PopularVehicle
#         url = serializers.HyperlinkedIdentityField(
#             view_name='PopularVehicle',
#             lookup_field='id'
#         )
#         fields = ('id', 'vehicles_sold', 'make', 'model')


class Vehicles(ViewSet):

    def create(self, request):

        def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        vin = id_generator()

        new_vehicle = Vehicle()

        new_vehicle.vin = vin
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

        vehicle.miles_count = request.data["miles_count"]
        vehicle.exterior_color = request.data["exterior_color"]
        vehicle.interior_color = request.data["interior_color"]
        
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
        limit = self.request.query_params.get('limit')
        popular_models = self.request.query_params.get('popular_models')
        vehicle_query = self.request.query_params.get('vehicle')
        # searchVal_model = self.request.query_params.get('model')
        vehicle_type_id = self.request.query_params.get('vehicle_type')

        
        if popular_models is not None:
            cursor = connection.cursor()
            cursor.execute('select * from popular_vehicles;')

            def dictfetchall(cursor):
                    "Return all rows from a cursor as a dict"
                    columns = [col[0] for col in cursor.description]
                    return [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]

            return Response(dictfetchall(cursor))

        elif vehicle_type_id is not None:
            cursor = connection.cursor()
            cursor.execute('select * from fetch_one_vehicle(%s);', [vehicle_type_id])

            def dictfetchall(cursor):
                    "Return all rows from a cursor as a dict"
                    columns = [col[0] for col in cursor.description]
                    return [
                        dict(zip(columns, row))
                        for row in cursor.fetchall()
                    ]

            return Response(dictfetchall(cursor))

        elif limit is not None:
            vehicles = Vehicle.objects.all().order_by('-id')[:int(limit)]
        
        elif  vehicle_query is not None:

            cursor = connection.cursor()
            cursor.execute("""SELECT v.*,
                                vt.make,
                                vt.model,
                                vt.body_type
                                FROM carnivalapi_vehicle v
                                LEFT JOIN carnivalapi_vehicletype vt ON v.vehicle_type_id = vt.id
                                WHERE (vt.make ILIKE %s OR vt.model ILIKE %s)
                                AND v.is_sold = false;""", [vehicle_query+'%', vehicle_query+'%'])

            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            return Response(dictfetchall(cursor))

        serializer = VehicleSerializer(
            vehicles, many=True, context={'request': request})


        return Response(serializer.data)
        
