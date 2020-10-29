from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import VehicleBodyType

class VehicleBodyTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VehicleBodyType
        url = serializers.HyperlinkedIdentityField(
            view_name='VehicleBodyType',
            lookup_field='id'
        )
        fields = ('id', 'name')

class VehicleBodyTypes(ViewSet):

    def create(self, request):
    
        new_vehiclebodytype = VehicleBodyType()

        new_vehiclebodytype.name = request.data["name"]

        # FOR POSTMAN TESTING
        # {
        #     "name": "BodyTypeName"
        # }


        new_vehiclebodytype.save()

        serializer = VehicleBodyTypeSerializer(
            new_vehiclebodytype, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            vehiclebodytype = VehicleBodyType.objects.get(pk=pk)

            serializer = VehicleBodyTypeSerializer(
                vehiclebodytype, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual vehicle body type
        Returns:
            Response -- Empty body with 204 status code
        """
        vehiclebodytype = VehicleBodyType.objects.get(pk=pk)

        vehiclebodytype.name = request.data["name"]

        vehiclebodytype.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single vehicle body type
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            vehiclebodytype = VehicleBodyType.objects.get(pk=pk)
            vehiclebodytype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except vehiclebodytype.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        vehiclebodytype = VehicleBodyType.objects.all()

        limit = self.request.query_params.get('limit')

        if limit is not None:
            vehiclebodytype = VehicleBodyType.objects.all()[:int(limit)]

        serializer = VehicleBodyTypeSerializer(
            vehiclebodytype, many=True, context={'request': request})

        return Response(serializer.data)