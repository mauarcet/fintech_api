from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from users_transactions.models import User, Transaction
from users_transactions.serializers import UserSerializer, TransactionSerializer, AccountSummarySerializer
from users_transactions.custom_classes import AccountSummary
from rest_framework.decorators import api_view
from datetime import date
import uuid

# USERS .......................................................................
@csrf_exempt
def users_list(request):
    """
    List all users, or create a new user.
    """
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def user_detail(request, pk):
    """
    Get user details
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = UserSerializer(user)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        user.delete()
        return HttpResponse(status=204)

# TRANSACTIONS ................................................................
@csrf_exempt
def transactions_list(request):
    """
    List all transactions, or create a new transaction.
    """
    if request.method == 'GET':
        transactions = Transaction.objects.all()
        serializer = TransactionSerializer(transactions, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
@csrf_exempt
def transaction_detail(request, pk):
    """
    Get transaction details

    The primary key of the transaction model is the field reference, 
    is necessary to cast the pk to uuid in order to perform the search of the object
    """
    pk = uuid.UUID(pk)
    try:
        transaction = Transaction.objects.get(pk=pk)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = TransactionSerializer(transaction)
        return JsonResponse(serializer.data)

    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TransactionSerializer(transaction, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == 'DELETE':
        transaction.delete()
        return HttpResponse(status=204)

# USER TRANSACTIONS ...........................................................
@api_view(["GET"])
def user_transactions_list(request, pk):
    try:
        transactions = Transaction.objects.filter(user_id=pk)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)    
    serializer = TransactionSerializer(transactions, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(["GET"])
def user_transactions_summary_by_account(request, pk):
    start_date = request.query_params.get('start_date', '2000-01-01')
    end_date = request.query_params.get('end_date', date.today())

    try:
        transactions = Transaction.objects.filter(user_id=pk, created_at__gte=start_date, created_at__lte=end_date)
    except Transaction.DoesNotExist:
        return HttpResponse(status=404)
    summary_by_account = AccountSummary.fromTransactions(transactions)
    serializer = AccountSummarySerializer(summary_by_account, many=True)
    return (JsonResponse(serializer.data, safe=False))