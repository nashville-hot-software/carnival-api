from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import EmployeeType

class EmployeeTypeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = EmployeeType
        url = serializers.HyperlinkedIdentityField(
            view_name='EmployeeTypes',
            lookup_field='id'
        )
        fields = ('id', 'name')

class EmployeeTypes(ViewSet):

    def create(self, request):
    
        new_employee_type = EmployeeType()

        new_employee_type.name = request.data["name"]
        
        # FOR POSTMAN TESTING
        # {
        #     "name": "Customer Service",
        # }


        new_employee_type.save()

        serializer = EmployeeTypeSerializer(
            new_employee_type, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            employee_type = EmployeeType.objects.get(pk=pk)

            serializer = EmployeeTypeSerializer(
                employee_type, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual employee type
        Returns:
            Response -- Empty body with 204 status code
        """
        employee_type = EmployeeType.objects.get(pk=pk)

        employee_type.name = request.data["name"]

        employee_type.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single employee type
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            employee_type = EmployeeType.objects.get(pk=pk)
            employee_type.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except employee_type.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        employee_types = EmployeeType.objects.all()

        limit = self.request.query_params.get('limit')

        if limit is not None:
            employee_types = EmployeeType.objects.all()[:int(limit)]

        serializer = EmployeeTypeSerializer(
            employee_types, many=True, context={'request': request})

        return Response(serializer.data)