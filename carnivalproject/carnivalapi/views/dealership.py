from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Dealership

class DealershipSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Dealership
        url = serializers.HyperlinkedIdentityField(
            view_name='Dealership',
            lookup_field='id'
        )
        fields = ('id', 'business_name', 'phone', 'city', 'state', 'website', 'tax_id')

class Dealerships(ViewSet):

    def create(self, request):
    
        new_dealership = Dealership()

        new_dealership.business_name = request.data["businessName"]
        new_dealership.phone = request.data["phone"]
        new_dealership.city = request.data["city"]
        new_dealership.state = request.data["state"]
        new_dealership.website = request.data["website"]
        new_dealership.tax_id = request.data["taxId"]

        # FOR POSTMAN TESTING
        # {
        #     "businessName": "New Dealership",
        #     "phone": "615-555-4321",
        #     "city": "Franklin",
        #     "state": "TN",
        #     "website": "newdealer.com",
        #     "taxId": "1234567891011"
        # }


        new_dealership.save()

        serializer = DealershipSerializer(
            new_dealership, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            dealership = Dealership.objects.get(pk=pk)

            serializer = DealershipSerializer(
                dealership, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual customer
        Returns:
            Response -- Empty body with 204 status code
        """
        dealership = Dealership.objects.get(pk=pk)

        dealership.business_name = request.data["business_name"]
        dealership.phone = request.data["phone"]
        dealership.city = request.data["city"]
        dealership.state = request.data["state"]
        dealership.website = request.data["website"]
        dealership.tax_id = request.data["tax_id"]

        dealership.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single dealership
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            dealership = Dealership.objects.get(pk=pk)
            dealership.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except dealership.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):

        dealerships = Dealership.objects.all()

        limit = self.request.query_params.get('limit')
        searchVal = self.request.query_params.get('searchTerm')

        if limit is not None:
            dealerships = Dealership.objects.all()[:int(limit)]
        
        elif searchVal is not None:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM carnivalapi_dealership WHERE business_name ILIKE %s", [searchVal+'%'])

            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            return Response(dictfetchall(cursor))

        serializer = DealershipSerializer(
            dealerships, many=True, context={'request': request})

        return Response(serializer.data)