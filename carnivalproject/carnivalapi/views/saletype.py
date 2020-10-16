from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import SaleType

class SaleTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SaleType
        url = serializers.HyperlinkedIdentityField(
            view_name='SaleTypes',
            lookup_field='id'
        )
        fields = ('id', 'name')

class SaleTypes(ViewSet):

    def create(self, request):
    
        new_sale_type = SaleType()

        new_sale_type.name = request.data["name"]
        
        # FOR POSTMAN TESTING
        # {
        #     "name": 12.34,
        # }


        new_sale_type.save()

        serializer = SaleTypeSerializer(
            new_sale_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            sale_type = SaleType.objects.get(pk=pk)

            serializer = SaleTypeSerializer(
                sale_type, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual account receivable
        Returns:
            Response -- Empty body with 204 status code
        """
        sale_type = SaleType.objects.get(pk=pk)

        sale_type.name = request.data["name"]
        
        sale_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single account receivable
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            sale_type = SaleType.objects.get(pk=pk)
            sale_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except sale_type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        sale_types = SaleType.objects.all()

        serializer = SaleTypeSerializer(
            sale_types, many=True, context={'request': request})

        return Response(serializer.data)