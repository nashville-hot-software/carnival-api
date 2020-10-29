from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Customer

class CustomerSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Customer
        url = serializers.HyperlinkedIdentityField(
            view_name='Customer',
            lookup_field='id'
        )
        fields = ('id', 'first_name', 'last_name', 'email', 'phone', 'street', 'city', 'state', 'zipcode', 'company_name')

class Customers(ViewSet):

    def create(self, request):
    
        new_customer = Customer()
        new_customer.first_name = request.data["firstName"]
        new_customer.last_name = request.data["lastName"]
        new_customer.email = request.data["email"]
        new_customer.phone = request.data["phone"]
        new_customer.street = request.data["street"]
        new_customer.city = request.data["city"]
        new_customer.state = request.data["state"]
        new_customer.zipcode = request.data["zipcode"]
        new_customer.company_name = request.data["companyName"]

        # FOR POSTMAN TESTING
        # {
        #     "firstName": "Tester",
        #     "lastName": "Testerrr",
        #     "email": "tester@gmail.com",
        #     "phone": "615-555-4321",
        #     "street": "123 Main St.",
        #     "city": "Franklin",
        #     "state": "TN",
        #     "zipcode": 37067,
        #     "companyName": "some company"
        # }


        new_customer.save()

        serializer = CustomerSerializer(
            new_customer, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            customer = Customer.objects.get(pk=pk)

            serializer = CustomerSerializer(
                customer, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual customer
        Returns:
            Response -- Empty body with 204 status code
        """
        customer = Customer.objects.get(pk=pk)

        customer.first_name = request.data["firstName"]
        customer.last_name = request.data["lastName"]
        customer.email = request.data["email"]
        customer.phone = request.data["phone"]
        customer.street = request.data["street"]
        customer.city = request.data["city"]
        customer.state = request.data["state"]
        customer.zipcode = request.data["zipcode"]
        customer.company_name = request.data["companyName"]

        customer.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single frend
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            customer = Customer.objects.get(pk=pk)
            customer.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except customer.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        customers = Customer.objects.all()

        limit = self.request.query_params.get('limit')

        if limit is not None:
            customers = Customer.objects.all()[:int(limit)]

        serializer = CustomerSerializer(
            customers, many=True, context={'request': request})

        return Response(serializer.data)