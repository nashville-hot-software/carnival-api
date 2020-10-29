from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import RepairType

class RepairTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = RepairType
        url = serializers.HyperlinkedIdentityField(
            view_name='RepairType',
            lookup_field='id'
        )
        fields = ('id', 'name')

class RepairTypes(ViewSet):

    def create(self, request):
    
        new_repairtype = RepairType()

        new_repairtype.name = request.data["name"]

        # FOR POSTMAN TESTING
        # {
        #     "name": "nameTesting"
        # }


        new_repairtype.save()

        serializer = RepairTypeSerializer(
            new_repairtype, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            repairtype = RepairType.objects.get(pk=pk)

            serializer = RepairTypeSerializer(
                repairtype, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual repair type
        Returns:
            Response -- Empty body with 204 status code
        """
        repairtype = RepairType.objects.get(pk=pk)

        repairtype.name = request.data["name"]

        repairtype.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single repair type
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            repairtype = RepairType.objects.get(pk=pk)
            repairtype.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except repairtype.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        repairtype = RepairType.objects.all()

        limit = self.request.query_params.get('limit')

        if limit is not None:
            repairtype = RepairType.objects.all()[:int(limit)]

        serializer = RepairTypeSerializer(
            repairtype, many=True, context={'request': request})

        return Response(serializer.data)