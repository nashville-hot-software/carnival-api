from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import CarRepairType

class CarRepairTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = CarRepairType
        url = serializers.HyperlinkedIdentityField(
            view_name='CarRepairTypes',
            lookup_field='id'
        )
        fields = ('id', 'name', 'date_occured', 'repair_type', 'vehicle')
        depth = 2

class CarRepairTypes(ViewSet):

    def create(self, request):
    
        new_car_repair = CarRepairType()

        new_car_repair.name = request.data["name"]
        new_car_repair.date_occured = request.data["dateOccured"]
        new_car_repair.repair_type_id = request.data["repairTypeId"]
        new_car_repair.vehicle_id = request.data["vehicleId"]

        # FOR POSTMAN TESTING
        # {
        #     "name": "Engine tune-up",
        #     "dateOccured": 2020-10-01,
        #     "repair_type_id": 1,
        #     "vehicleId": 1,
        # }


        new_car_repair.save()

        serializer = CarRepairTypeSerializer(
            new_car_repair, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            car_repair_type = CarRepairType.objects.get(pk=pk)

            serializer = CarRepairTypeSerializer(
                car_repair_type, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual car repair types
        Returns:
            Response -- Empty body with 204 status code
        """
        car_repair_type = CarRepairType.objects.get(pk=pk)

        car_repair_type.name = request.data["name"]
        car_repair_type.date_occured = request.data["dateOccured"]
        car_repair_type.repair_type_id = request.data["repairTypeId"]
        car_repair_type.vehicle_id = request.data["vehicleId"]

        car_repair_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single car repair type
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            car_repair_type = CarRepairType.objects.get(pk=pk)
            car_repair_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except car_repair_type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        car_repair_types = CarRepairType.objects.all()

        serializer = CarRepairTypeSerializer(
            car_repair_types, many=True, context={'request': request})

        return Response(serializer.data)