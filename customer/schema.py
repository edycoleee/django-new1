# customer/schema.py
from drf_spectacular.utils import extend_schema
from .serializers import CustomerInputSerializer, CustomerOutputSerializer

customer_list_schema = extend_schema(
    summary="List Customers",
    description="Mengambil daftar seluruh customer.",
    responses={200: CustomerOutputSerializer(many=True)},
    tags=["Customer"]
)

customer_retrieve_schema = extend_schema(
    summary="Retrieve Customer",
    description="Mengambil detail customer berdasarkan ID.",
    responses={200: CustomerOutputSerializer},
    tags=["Customer"]
)

customer_create_schema = extend_schema(
    summary="Create Customer",
    description="Membuat customer baru.",
    request=CustomerInputSerializer,
    responses={201: CustomerOutputSerializer},
    tags=["Customer"]
)

customer_update_schema = extend_schema(
    summary="Update Customer",
    description="Memperbarui data customer berdasarkan ID.",
    request=CustomerInputSerializer,
    responses={200: CustomerOutputSerializer},
    tags=["Customer"]
)

customer_delete_schema = extend_schema(
    summary="Delete Customer",
    description="Menghapus customer berdasarkan ID.",
    responses={204: None},
    tags=["Customer"]
)