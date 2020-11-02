from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Sale, SaleType, SaleMetric
# from django.db import connection

class SaleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sale
        url = serializers.HyperlinkedIdentityField(
            view_name='sale',
            lookup_field='id'
        )
        fields = ('id' ,'sales_type', 'vehicle','employee','customer','dealership', 'price', 'deposit', 'purchase_date', 'pickup_date', 'invoice_number', 'payment_method', 'returned')
        depth = 2

class SaleMetricSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SaleMetric
        url = serializers.HyperlinkedIdentityField(
            view_name='sale',
            lookup_field='id'
        )
        fields = ('id', 'sale_count')

class Sales(ViewSet):

    def create(self, request):
    
        new_sale = Sale()
        new_sale.price = request.data["price"]
        new_sale.deposit = request.data["deposit"]
        new_sale.purchase_date = request.data["purchase_date"]
        new_sale.pickup_date = request.data["pickup_date"]
        new_sale.invoice_number = request.data["invoice_number"]
        new_sale.payment_method = request.data["payment_method"]
        new_sale.returned = request.data["returned"]
        new_sale.customer_id = request.data["customer_id"]
        new_sale.dealership_id = request.data["dealership_id"]
        new_sale.employee_id = request.data["employee_id"]
        new_sale.sales_type_id = request.data["sales_type_id"]
        new_sale.vehicle_id = request.data["vehicle_id"]
       

        # FOR POSTMAN TESTING
        # {
        #     "price": "Tester",
        #     "deposit": "Testerrr",
        #     "purchase_date": "tester@gmail.com",
        #     "pickup_date": "615-555-4321",
        #     "invoice_number": "123 Main St.",
        #     "payment_method": "Franklin",
        #     "returned": "TN",
        #     "customer_id": 37067,
        #     "dealership_id": "some company"
        #     "employee_id": "some company"
        #     "sales_type_id": "some company"
        #     "vehicle_id": "some company"
        # }


        new_sale.save()

        serializer = SaleSerializer(
            new_sale, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            sale = Sale.objects.get(pk=pk)

            # cursor = connection.cursor()
            # cursor.execute('''SELECT count(*) FROM people_person''')

            serializer = SaleSerializer(
                sale, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual sale
        Returns:
            Response -- Empty body with 204 status code
        """
        sale = Sale.objects.get(pk=pk)

        sale.first_name = request.data["firstName"]
        sale.last_name = request.data["lastName"]
        sale.email = request.data["email"]
        sale.phone = request.data["phone"]
        sale.street = request.data["street"]
        sale.city = request.data["city"]
        sale.state = request.data["state"]
        sale.zipcode = request.data["zipcode"]
        sale.company_name = request.data["companyName"]

        sale.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single frend
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            sale = Sale.objects.get(pk=pk)
            sale.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except sale.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        recent_sales = Sale.objects.raw('select * from recent_sales;')

        limit = self.request.query_params.get('limit')
        sale_count = self.request.query_params.get('sale_count')

        if limit is not None:
            recent_sales = Sale.objects.raw('select * from recent_sales;')[:int(limit)]
        
        elif sale_count is not None:
            four_month_recent_sales = Sale.objects.raw('select * from four_month_recent_sales;')

            serializer = SaleMetricSerializer(
                four_month_recent_sales, many=True, context={'request': request})
                
            return Response(serializer.data)


        serializer = SaleSerializer(
            recent_sales, many=True, context={'request': request})

        return Response(serializer.data)