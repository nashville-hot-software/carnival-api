# FOR POSTMAN TESTING
# {
#     "price": 25555.55,
#     "deposit": 5000,
#     "pickup_date": "2020-11-25",
#     "invoice_number": "543WW215JE",
#     "payment_method": "mastercard",
#     "returned": "false",
#     "dealership_id": "20",
#     "employee_id": "5",
#     "sales_type_id": "2",
#     "vehicle_id": "44",
#     "first_name": "Jim",
#     "last_name": "Rogers",
#     "email": "jimr@yahoo.com",
#     "phone": "555-555-4433",
#     "street": "123 main st.",
#     "city": "Franklin",
#     "state": "TN",
#     "zipcode": "37067",
#     "company_name": "landscaperz"
# }


from django.http import HttpResponseServerError
from django.db import connection
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import Sale, SaleType, Customer
import string
import random


class SaleSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Sale
        url = serializers.HyperlinkedIdentityField(
            view_name='sale',
            lookup_field='id'
        )
        fields = ('id', 'sales_type', 'vehicle', 'employee', 'customer', 'customer_id', 'dealership', 'price',
                  'deposit', 'purchase_date', 'pickup_date', 'invoice_number', 'payment_method', 'returned')
        depth = 2


class Sales(ViewSet):

    def create(self, request):

        def id_generator(size=10, chars=string.digits):
            return ''.join(random.choice(chars) for _ in range(size))

        invoice_num = id_generator()

        new_sale = Sale()

        new_sale.price = request.data["price"]
        new_sale.deposit = request.data["deposit"]
        new_sale.pickup_date = request.data["pickup_date"]
        new_sale.invoice_number = invoice_num
        new_sale.payment_method = request.data["payment_method"]
        new_sale.returned = request.data["returned"]
        new_sale.dealership_id = request.data["dealership_id"]
        new_sale.employee_id = request.data["employee_id"]
        new_sale.sales_type_id = request.data["sales_type_id"]
        new_sale.vehicle_id = request.data["vehicle_id"]

        new_customer = Customer()

        new_customer.first_name = request.data["first_name"]
        new_customer.last_name = request.data["last_name"]
        new_customer.email = request.data["email"]
        new_customer.phone = request.data["phone"]
        new_customer.street = request.data["street"]
        new_customer.city = request.data["city"]
        new_customer.state = request.data["state"]
        new_customer.zipcode = request.data["zipcode"]
        new_customer.company_name = request.data["company_name"]

        print(
            f'XXXXXX {new_sale.invoice_number} {new_sale.vehicle_id} XXXXXXX')

        if new_sale is not None:
            cursor = connection.cursor()
            cursor.execute("""CALL new_sale(%s, %s, %s, %s, %s, %s, %s, %s, %s,
                                %s, %s, %s, %s, %s, CURRENT_DATE, %s, %s,
                                %s, %s, %s)""", [new_customer.first_name, new_customer.last_name,
                                                 new_customer.email, new_customer.phone, new_customer.street,
                                                 new_customer.city, new_customer.state, new_customer.zipcode,
                                                 new_customer.company_name, new_sale.sales_type_id, new_sale.employee_id,
                                                 new_sale.dealership_id, new_sale.price, new_sale.deposit,
                                                 new_sale.pickup_date, new_sale.invoice_number,
                                                 new_sale.payment_method, new_sale.returned, new_sale.vehicle_id])

            return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):

        try:
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM one_sale_with_one_customer(%s)""",[pk])

            

            # cursor = connection.cursor()
            # cursor.execute('''SELECT count(*) FROM people_person''')

            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            return Response(dictfetchall(cursor))


        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual sale
        Returns:
            Response -- Empty body with 204 status code
        """
        edited_sale = Sale()
        edited_sale.id = request.data["id"]
        edited_sale.price = request.data["price"]
        edited_sale.deposit = request.data["deposit"]
        edited_sale.pickup_date = request.data["pickup_date"]
        edited_sale.purchase_date = request.data["purchase_date"]
        edited_sale.payment_method = request.data["payment_method"]
        edited_sale.returned = request.data["returned"]
        edited_sale.sales_type_id = request.data["sales_type_id"]
        edited_sale.customer_id = request.data["customer_id"]
        edited_sale.first_name = request.data["first_name"]
        edited_sale.last_name = request.data["last_name"]
        edited_sale.email = request.data["email"]
        edited_sale.phone = request.data["phone"]
        edited_sale.street = request.data["street"]
        edited_sale.city = request.data["city"]
        edited_sale.state = request.data["state"]
        edited_sale.zipcode = request.data["zipcode"]
        edited_sale.company_name = request.data["company_name"]

        cursor = connection.cursor()
        cursor.execute("CALL update_sale_and_customer(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        [edited_sale.id,
        edited_sale.customer_id,
        edited_sale.first_name,
        edited_sale.last_name,
        edited_sale.email,
        edited_sale.phone,
        edited_sale.street,
        edited_sale.city,
        edited_sale.state,
        edited_sale.zipcode,
        edited_sale.company_name,
        edited_sale.sales_type_id,
        edited_sale.price,
        edited_sale.deposit,
        edited_sale.purchase_date,
        edited_sale.pickup_date,
        edited_sale.payment_method,
        edited_sale.returned
        ])
        def dictfetchall(cursor):
            "Return all rows from a cursor as a dict"
            columns = [col[0] for col in cursor.description]
            return [
                dict(zip(columns, row))
                for row in cursor.fetchall()
            ]
        # return Response(dictfetchall(cursor))
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

        recent_sales = Sale.objects.raw('select * from one_month_sales;')

        limit = self.request.query_params.get('limit')
        sale_count = self.request.query_params.get('sale_count')
        revenue = self.request.query_params.get('revenue')
        searchVal = self.request.query_params.get('searchTerm')

        if limit is not None:
            recent_sales = Sale.objects.raw(
                'select * from recent_sales;')[:int(limit)]

        elif sale_count is not None and revenue is not None:
            four_month_recent_sales_revs = Sale.objects.raw(
                'select * from four_month_recent_sales_revenue;')


        elif sale_count is not None:
            cursor = connection.cursor()
            cursor.execute('select * from four_month_recent_sales;')

            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            return Response(dictfetchall(cursor))

        elif searchVal is not None:
            cursor = connection.cursor()
            cursor.execute("""SELECT * 
                              FROM carnivalapi_sale s
                              INNER JOIN carnivalapi_customer c  
                              ON s.customer_id = c.id 
                              WHERE first_name ILIKE %s""", [searchVal+'%'])

            def dictfetchall(cursor):
                "Return all rows from a cursor as a dict"
                columns = [col[0] for col in cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in cursor.fetchall()
                ]

            return Response(dictfetchall(cursor))
            
        serializer = SaleSerializer(
            recent_sales, many=True, context={'request': request})

        return Response(serializer.data)
