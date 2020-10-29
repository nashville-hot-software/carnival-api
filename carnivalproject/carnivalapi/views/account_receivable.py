from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from ..models import AccountReceivable

class AccountReceivableSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = AccountReceivable
        url = serializers.HyperlinkedIdentityField(
            view_name='Account Receivable',
            lookup_field='id'
        )
        fields = ('id', 'credit_amount', 'debit_amount', 'date_received', 'sale')
        depth = 1

class AccountsReceivable(ViewSet):

    def create(self, request):
    
        new_account = AccountReceivable()

        new_account.credit_amount = request.data["creditAmount"]
        new_account.debit_amount = request.data["debitAmount"]
        new_account.date_received = request.data["dateReceived"]
        new_account.sale_id = request.data["saleId"]

        # FOR POSTMAN TESTING
        # {
        #     "creditAmount": 12.34,
        #     "debitAmount": ,
        #     "dateReceived": "2020-10-01",
        #     "saleId": 1,
        # }


        new_account.save()

        serializer = AccountReceivableSerializer(
            new_account, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):

        try:
            account_receivable = AccountReceivable.objects.get(pk=pk)

            serializer = AccountReceivableSerializer(
                account_receivable, context={'request': request})

            return Response(serializer.data)

        except Exception as ex:
            return HttpResponseServerError(ex)

    def put(self, request, pk=None):
        """Handle PUT requests for an individual account receivable
        Returns:
            Response -- Empty body with 204 status code
        """
        account_receivable = AccountReceivable.objects.get(pk=pk)

        account_receivable.credit_amount = request.data["creditAmount"]
        account_receivable.debit_amount = request.data["debitAmount"]
        account_receivable.date_received = request.data["dateReceived"]
        account_receivable.sale_id = request.data["saleId"]

        account_receivable.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single account receivable
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            account_receivable = AccountReceivable.objects.get(pk=pk)
            account_receivable.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except account_receivable.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        
        accounts_receivable = AccountReceivable.objects.all()

        serializer = AccountReceivableSerializer(
            accounts_receivable, many=True, context={'request': request})

        return Response(serializer.data)