#/customer/views.py >> request method-validation-service-response + openapi extend
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from restapi.utils.response_wrapper import success_response
from restapi.utils.exception_handler import NotFoundException
from .services import *
from .serializers import *
from drf_spectacular.utils import extend_schema
from .schema import (
    customer_list_schema,
    customer_retrieve_schema,
    customer_create_schema,
    customer_update_schema,
    customer_delete_schema,
)


class CustomerViewSet(ViewSet):

    @customer_list_schema
    def list(self, request):
        customers = get_all_customers()
        serializer = CustomerOutputSerializer(customers, many=True)
        return Response(success_response("List Customer", data=serializer.data))

    @customer_retrieve_schema
    def retrieve(self, request, pk=None):
        customer = get_customer_by_id(pk)
        if not customer:
            raise NotFoundException("Customer not found")
        serializer = CustomerOutputSerializer(customer)
        return Response(success_response("Detail Customer", data=serializer.data))

    @customer_create_schema
    def create(self, request):
        serializer = CustomerInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = create_customer(serializer.validated_data)
        output = CustomerOutputSerializer(customer)
        return Response(success_response("Customer Created", data=output.data), status=status.HTTP_201_CREATED)

    @customer_update_schema
    def update(self, request, pk=None):
        serializer = CustomerInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        customer = update_customer(pk, serializer.validated_data)
        if not customer:
            raise NotFoundException("Customer not found")
        output = CustomerOutputSerializer(customer)
        return Response(success_response("Customer Updated", data=output.data))

    @customer_delete_schema
    def destroy(self, request, pk=None):
        customer = get_customer_by_id(pk)
        if not customer:
            raise NotFoundException("Customer not found")
        delete_customer(pk)
        return Response(success_response("Customer Deleted", data={}), status=status.HTTP_204_NO_CONTENT)