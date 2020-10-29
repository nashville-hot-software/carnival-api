from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import DealershipEmployee

class DealershipEmployeeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = DealershipEmployee
        url = serializers.HyperlinkedIdentityField(
            view_name='dealershipemployee',
            lookup_field='id'
        )
        fields = ('id', 'dealership_id', 'dealership', 'employee_id', 'employee')
        depth = 1

class DealershipEmployees(ViewSet):

    def create(self, request):
    
        new_dealership_employee = DealershipEmployee()

        new_dealership_employee.dealership_id = request.data["dealershipId"]
        new_dealership_employee.employee_id = request.data["employeeId"]

        # FOR POSTMAN TESTING
        # {
        #     "dealershipId": 1,
        #     "employeeId": 1,
        # }


        new_dealership_employee.save()

        serializer = DealershipEmployeeSerializer(
            new_dealership_employee, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            dealership_employee = DealershipEmployee.objects.get(pk=pk)

            serializer = DealershipEmployeeSerializer(
                dealership_employee, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual dealership employee
        Returns:
            Response -- Empty body with 204 status code
        """
        dealership_employee = DealershipEmployee.objects.get(pk=pk)

        dealership_employee.dealership_id = request.data["dealershipId"]
        dealership_employee.employee_id = request.data["employeeId"]

        dealership_employee.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single dealership employee
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            dealership_employee = DealershipEmployee.objects.get(pk=pk)
            dealership_employee.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except dealership_employee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        dealership_employees = DealershipEmployee.objects.all()

        limit = self.request.query_params.get('limit')

        if limit is not None:
            dealership_employees = DealershipEmployee.objects.all()[:int(limit)]

        serializer = DealershipEmployeeSerializer(
            dealership_employees, many=True, context={'request': request})

        return Response(serializer.data)