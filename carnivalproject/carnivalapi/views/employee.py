from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Employee

class EmployeeSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Employee
        url = serializers.HyperlinkedIdentityField(
            view_name='Employees',
            lookup_field='id'
        )
        fields = ('id', 'first_name', 'last_name', 'email_address', 'phone', 'dealership_id', 'employee_type_id')

class Employees(ViewSet):

    def create(self, request):
    
        new_employee = Employee()

        new_employee.first_name = request.data["firstName"]
        new_employee.last_name = request.data["lastName"]
        new_employee.email_address = request.data["emailAddress"]
        new_employee.phone = request.data["phone"]
        new_employee.dealership_id = request.data["dealershipId"]
        new_employee.employee_type_id = request.data["employeeTypeId"]

        # FOR POSTMAN TESTING
        # {
        #     "firstName": "Test",
        #     "lastName": "Employee",
        #     "emailAddress": "testemployee@gmail.com",
        #     "phone": "615-555-4321",
        #     "isActive": true,
        #     "employeeTypeId": 1,
        # }


        new_employee.save()

        serializer = EmployeeSerializer(
            new_employee, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            employee = Employee.objects.get(pk=pk)

            serializer = EmployeeSerializer(
                employee, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual employee
        Returns:
            Response -- Empty body with 204 status code
        """
        employee = Employee.objects.get(pk=pk)

        employee.first_name = request.data["firstName"]
        employee.last_name = request.data["lastName"]
        employee.email_address = request.data["emailAddress"]
        employee.phone = request.data["phone"]
        employee.isActive = request.data["isActive"]
        employee.employee_type_id = request.data["employeeTypeId"]

        employee.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single employee
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except employee.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        employees = Employee.objects.all()

        serializer = EmployeeSerializer(
            employees, many=True, context={'request': request})

        return Response(serializer.data)