from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import VehicleModel

class VehicleModelSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = VehicleModel
        url = serializers.HyperlinkedIdentityField(
            view_name='VehicleModels',
            lookup_field='id'
        )
        fields = ('id', 'model_name')

class VehicleModels(ViewSet):

    def create(self, request):
    
        new_vehicle_model = VehicleModel()

        new_vehicle_model.model_name = request.data["name"]
        
        # FOR POSTMAN TESTING
        # {
        #     "name": "1234VV7JCW910",
        # }


        new_vehicle_model.save()

        serializer = VehicleModelSerializer(
            new_vehicle_model, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            vehicle_model = VehicleModel.objects.get(pk=pk)

            serializer = VehicleModelSerializer(
                vehicle_model, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual vehicle model
        Returns:
            Response -- Empty body with 204 status code
        """
        vehicle_model = VehicleModel.objects.get(pk=pk)

        vehicle_model.model_name = request.data["name"]
        
        vehicle_model.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single vehicle model
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            vehicle_model = VehicleModel.objects.get(pk=pk)
            vehicle_model.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except vehicle_model.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        vehicle_models = VehicleModel.objects.all()

        limit = self.request.query_params.get('limit')

        if limit is not None:
            vehicle_models = VehicleModel.objects.all()[:int(limit)]

        serializer = VehicleModelSerializer(
            vehicle_models, many=True, context={'request': request})

        return Response(serializer.data)