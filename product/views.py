#/product/views.py
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from restapi.utils.exception_handler import NotFoundException
from restapi.utils.response_wrapper import success_response
from .services import get_all_products, get_product_by_id, create_product, update_product, delete_product
from .serializers import ProductInputSerializer, ProductOutputSerializer
from drf_spectacular.utils import extend_schema

class ProductViewSet(ViewSet):

    @extend_schema(
        summary="List Products",
        description="Mengambil semua data produk dari tabel `tb_product`.",
        responses={200: ProductOutputSerializer(many=True)}
    )
    def list(self, request):
        products = get_all_products()
        serializer = ProductOutputSerializer(products, many=True)
        return Response(success_response("List Product", data=serializer.data))

    @extend_schema(
        summary="Retrieve Product",
        description="Mengambil detail produk berdasarkan ID.",
        responses={200: ProductOutputSerializer, 404: {"message": "Product not found"}}
    )
    def retrieve(self, request, pk=None):
        product = get_product_by_id(pk)
        if not product:
            raise NotFoundException("Product not found")
        serializer = ProductOutputSerializer(product)
        return Response(success_response("Detail Product", data=serializer.data))

    @extend_schema(
        summary="Create Product",
        description="Membuat data produk baru.",
        request=ProductInputSerializer,
        responses={201: ProductOutputSerializer}
    )
    def create(self, request):
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = create_product(serializer.validated_data)
        output = ProductOutputSerializer(product)
        return Response(success_response("Product Created", data=output.data), status=status.HTTP_201_CREATED)

    @extend_schema(
        summary="Update Product",
        description="Mengupdate data produk berdasarkan ID.",
        request=ProductInputSerializer,
        responses={200: ProductOutputSerializer, 404: {"message": "Product not found"}}
    )
    def update(self, request, pk=None):
        serializer = ProductInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        product = update_product(pk, serializer.validated_data)
        if not product:
            raise NotFoundException("Product not found")
        output = ProductOutputSerializer(product)
        return Response(success_response("Product Updated", data=output.data))

    @extend_schema(
        summary="Delete Product",
        description="Menghapus produk berdasarkan ID.",
        responses={204: None, 404: {"message": "Product not found"}}
    )
    def destroy(self, request, pk=None):
        product = get_product_by_id(pk)
        if not product:
            raise NotFoundException("Product not found")
        delete_product(pk)
        return Response(success_response("Product Deleted", data={}), status=status.HTTP_204_NO_CONTENT)
