from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import OilChangeLog

class OilChangeLogSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = OilChangeLog
        url = serializers.HyperlinkedIdentityField(
            view_name='OilChangeLog',
            lookup_field='id'
        )
        fields = ('id', 'oil_change_date', 'vehicle_id')

class OilChangeLogs(ViewSet):

    def create(self, request):
    
        new_oilchangelog = OilChangeLog()

        new_oilchangelog.oil_change_date = request.data["oilChangeDate"]
        new_oilchangelog.vehicle_id = request.data["vehicleId"]

        # FOR POSTMAN TESTING
        # {
        #     "oilChangeDate": "2020-01-12",
        #     "vehicleId": "1"
        # }


        new_oilchangelog.save()

        serializer = OilChangeLogSerializer(
            new_oilchangelog, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            oilchangelog = OilChangeLog.objects.get(pk=pk)

            serializer = OilChangeLogSerializer(
                oilchangelog, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual oil change log
        Returns:
            Response -- Empty body with 204 status code
        """
        oilchangelog = OilChangeLog.objects.get(pk=pk)

        oilchangelog.oil_change_date = request.data["oilChangeDate"]
        oilchangelog.vehicle_id = request.data["vehicleId"]

        oilchangelog.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single oil change log
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            oilchangelog = OilChangeLog.objects.get(pk=pk)
            oilchangelog.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except oilchangelog.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        oilchangelog = OilChangeLog.objects.all()

        serializer = OilChangeLogSerializer(
            oilchangelog, many=True, context={'request': request})

        return Response(serializer.data)