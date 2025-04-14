
## 1. PERSIAPAN INSTALASI

```py
#buat folder dj-api2 >> buka dengan vscode
#create venv
python3 -m venv .venv 
python -m venv .venv # Windows
#activate venv
source .venv/bin/activate
.venv/Scripts/activate #Windows
#check python venv
which python
#deactivate venv
#deactivate
```

```py
#melanjutkan 
python3 -m pip install --upgrade pip
python3 -m pip --version

python -m pip install --upgrade pip  # Windows
python -m pip --version  # Windows
```

```py
pip install django djangorestframework

django-admin --version

django-admin startproject restapi .

python manage.py runserver

#Starting development server at http://127.0.0.1:8000/

```

```cmd
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/edycoleee/django-new1.git
git push -u origin main
```
```cmd
git clone https://github.com/edycoleee/django-new1.git

git chekcout (branch yg dituju)

git pull
```

## 2. COBA APP 1 >> RESPONSE SEDERHANA

```js
//Membuat api : coba

GET http://localhost:8000/api/test

response : {
  "message": "Hello World"
}
```
```py
python manage.py startapp coba
```

```py
#/restapi/settings.py
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'coba',
]

# restapi/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('coba.urls')),  # versioned API
]

# coba/urls.py
from django.urls import path
from .views import TestView

urlpatterns = [
    path('test', TestView.as_view(), name='test'),
]

# coba/views.py
from rest_framework.views import APIView
from rest_framework.response import Response

class TestView(APIView):
    def get(self, request):
        return Response({"message": "Hello World"})


# coba/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TestViewTests(APITestCase):
    def test_get_test_view(self):
        url = reverse('test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"message": "Hello World"})

```
```js
//coba/request.rest
### 1. GET TEST
GET http://localhost:8000/api/test HTTP/1.1
```

## 3. COBA APP 2 >> RESPONSE WRAPPER

```py
#Install library recommended yang mendukung DRF full (CBV, ViewSet, Router, dll)
pip install drf-spectacular
```

```js

//Response Wrapper di Django REST Framework (DRF)

{
  "status": "success",
  "message": "Hello World",
  "data": {
    // isi data sebenarnya
  }
}
```

```py
#/restapi/utils/response_wrapper.py
def success_response(message, data=None, status="success"):
    return {
        "status": status,
        "message": message,
        "data": data if data is not None else {}
    }

# coba/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from restapi.utils.response_wrapper import success_response

class TestView(APIView):
    def get(self, request):
        data = {"info": "This is a wrapped response"}
        return Response(success_response("Hello World", data))

//coba/request.rest
### 1. GET TEST
GET http://localhost:8000/api/test HTTP/1.1

### Response :
{
  "status": "success",
  "message": "Hello World",
  "data": {
    "info": "This is a wrapped response"
  }
}
```

## 3. COBA APP 3 >> EXCEPTION HANDLER

```js
//Custom Exception Handler biar response error juga konsisten

{
  "status": "error",
  "message": "Not Found",
  "data": {}
}
```
```py
# restapi/settings.py >>exception

REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'restapi.utils.exception_handler.custom_exception_handler'
}

#/restapi/utils/exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from restapi.utils.response_wrapper import success_response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        message = response.data.get('detail') if 'detail' in response.data else "Something went wrong"
        return Response(success_response(
            message=message,
            data={},
            status="error"
        ), status=response.status_code)

    # Untuk unhandled exception
    return Response(success_response(
        message=str(exc),
        data={},
        status="error"
    ), status=500)


# coba/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from restapi.utils.response_wrapper import success_response
from rest_framework.exceptions import NotFound

class TestView(APIView):
    def get(self, request):
        data = {"info": "This is a wrapped response"}
        return Response(success_response("Hello World", data))

class ErrorExampleView(APIView):
    def get(self, request):
        raise NotFound("Halaman tidak ditemukan")


# coba/urls.py
from django.urls import path
from .views import ErrorExampleView, TestView

urlpatterns = [
    path('test', TestView.as_view(), name='test'),
    path('error', ErrorExampleView.as_view(), name='error'),  # endpoint baru
]

# coba/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

class TestViewTests(APITestCase):
    def test_get_test_view(self):
        url = reverse('test')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #self.assertEqual(response.data, {"message": "Hello World"})
        self.assertEqual(response.data['status'], 'success')
        self.assertEqual(response.data['message'], 'Hello World')
        self.assertIn('data', response.data)
        self.assertEqual(response.data['data']['info'], 'This is a wrapped response')

class ErrorViewTests(APITestCase):
    def test_get_error_view(self):
        url = reverse('error')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['status'], 'error')
        self.assertEqual(response.data['message'], 'Halaman tidak ditemukan')
        self.assertEqual(response.data['data'], {})

```
```js
//coba/request.rest
### 1. GET TEST
GET http://localhost:8000/api/test HTTP/1.1

### 2. GET TEST
GET http://localhost:8000/api/error HTTP/1.1
```

## 4. COBA APP 4 >> SWAGGER UI

```py
pip install drf-spectacular
```

```py
# restapi/settings.py >>swagger
INSTALLED_APPS += [
    'drf_spectacular',
]

REST_FRAMEWORK.update({
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
})

SPECTACULAR_SETTINGS = {
    'TITLE': 'REST API COBA',
    'DESCRIPTION': 'Dokumentasi API project coba',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

# restapi/urls.py
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (SpectacularSwaggerView)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('coba.urls')),  # versioned API

     # Swagger
    path('api/docs/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

Buka di browser:

Swagger UI: `http://localhost:8000/api/docs/swagger/`

## 5. PRODUCT APP

1. Membuat App product

```py
python manage.py startapp product
```
2. Membuat tabel SQLITE tanpa ORM

```py
python3 manage.py dbshell
```

```sql
CREATE TABLE tb_product (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kd_product TEXT NOT NULL,
    nm_product TEXT NOT NULL,
    price REAL NOT NULL
);
```
```py
.tables
```
JIKA TERJADI ERROR TIDAK BISA MASUK SQLITE >> OS WINDOWS

Download https://sqlite.org/download.html >> sqlite-tools-win-x64-3490100.zip
Extrac kemudian copykan sqlite3.exe ke folder django.
`python manage.py dbshell`


3. OpenAPI 3.0
```py
pip install drf-spectacular
```
drf-spectacular adalah pustaka tambahan (third-party library) untuk Django REST Framework (DRF) yang digunakan untuk membuat dokumentasi OpenAPI 3.0 secara otomatis dari API ditampilkan dalam bentuk Swagger UI.

```py
# restapi/settings.py >> apps
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'coba',
    'product',
]

# restapi/settings.py >>exception
REST_FRAMEWORK = {
    'EXCEPTION_HANDLER': 'restapi.utils.exception_handler.custom_exception_handler'
}

# restapi/settings.py >>swagger
INSTALLED_APPS += [
    'drf_spectacular',
]

# restapi/settings.py >>drf_spectacular
REST_FRAMEWORK.update({
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
})


# Setting yang tampil di swagger 
SPECTACULAR_SETTINGS = {
    'TITLE': 'REST API COBA',
    'DESCRIPTION': 'Dokumentasi API project coba',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}


```
4. FOLDER UTAMA
```py
# restapi/urls.py >> URL UTAMA
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ini yang penting: path ini HARUS ada
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Include routes dari apps
    path('api/', include('coba.urls')),  # Coba App
    path('api/', include('product.urls')), #Product App
    #path('api/', include('customer.urls')), #Customer App

     # 🔍 Swagger UI >> API Dokumentasi >> AUTO
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

#/restapi/utils/response_wrapper.py
def success_response(message=None, data=None, status="success"):
    return {
        "status": status,
        "message": message,
        "data": data if data is not None else {}
    }

#restapi/utils/exception_handler.py
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status
from restapi.utils.response_wrapper import success_response

class NotFoundException(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found'
    default_code = 'not_found'

def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is not None:
        response.data = success_response(status='error', data=None, message=str(exc))
    return response

#/restapi/utils/db.py`
from django.db import connection

def dictfetchall(cursor): # >> ARRAY OBJECT
    columns = [col[0] for col in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]

def dictfetchone(cursor):# >> SATU OBJECT
    columns = [col[0] for col in cursor.description]
    row = cursor.fetchone()
    return dict(zip(columns, row)) if row else None

def execute_query(query, params=None, fetchone=False, fetchall=True): # DEFAULT >> ARRAY OBJECT
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        if fetchone:
            return dictfetchone(cursor)
        if fetchall:
            return dictfetchall(cursor)
        return None

```
4. PRODUCT APP

```py
#/product/serializer.py >>validation dan swagger input
from rest_framework import serializers

class ProductInputSerializer(serializers.Serializer):
    kd_product = serializers.CharField()
    nm_product = serializers.CharField()
    price = serializers.FloatField()

class ProductOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    kd_product = serializers.CharField()
    nm_product = serializers.CharField()
    price = serializers.FloatField()

#/product/services.py >>raw SQL
from restapi.utils.db import execute_query

def get_all_products():
    return execute_query("SELECT * FROM tb_product")

def get_product_by_id(product_id):
    return execute_query(
        "SELECT * FROM tb_product WHERE id = %s",
        [product_id],
        fetchone=True
    )

def delete_product(product_id):
    execute_query("DELETE FROM tb_product WHERE id = %s", [product_id], fetchall=False)

def create_product(data):
    query = """
        INSERT INTO tb_product (kd_product, nm_product, price)
        VALUES (%s, %s, %s)
        RETURNING id, kd_product, nm_product, price
    """
    params = [data.get('kd_product'), data.get('nm_product'), data.get('price')]
    return execute_query(query, params, fetchone=True)

def update_product(product_id, data):
    query = """
        UPDATE tb_product
        SET kd_product = %s, nm_product = %s, price = %s
        WHERE id = %s
        RETURNING id, kd_product, nm_product, price
    """
    params = [data.get('kd_product'), data.get('nm_product'), data.get('price'), product_id]
    return execute_query(query, params, fetchone=True)


#/product/views.py >> request method-validation-service-response + openapi extend
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

#/product/urls.py
from django.urls import path
from rest_framework.routers import DefaultRouter
from product.views import ProductViewSet

router = DefaultRouter()
router.register(r'product', ProductViewSet, basename='product')

urlpatterns = router.urls

```

```py 
#/product/tests.py
import json
from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from django.db import connection


class ProductViewSetTests(TestCase):

    def setUp(self):
        """Menyiapkan database sebelum setiap pengujian."""
        self.client = Client()

        # Buat tabel siswa jika belum ada
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_product (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    kd_product TEXT NOT NULL,
                    nm_product TEXT NOT NULL,
                    price REAL NOT NULL
                )
            """)

        # Masukkan data dummy untuk pengujian (dilakukan dalam blok with yang berbeda)
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO tb_product (kd_product, nm_product, price)
                VALUES (%s, %s, %s)
            """, ['P001', 'Produk Satu', 10000])
            self.product_id = cursor.lastrowid
            print({self.product_id})

    def tearDown(self):
        """Membersihkan database setelah pengujian."""
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tb_product")

    def test_list_product(self):
        url = reverse('product-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['status'], 'success')
        self.assertIn('data', response.data)

    def test_retrieve_product(self):
        url = reverse('product-detail', args=[self.product_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['kd_product'], 'P001')

    def test_create_product(self):
        url = reverse('product-list')
        data = {
            'kd_product': 'P002',
            'nm_product': 'Produk Dua',
            'price': 20000
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], 'Product Created')

    def test_update_product(self):
        url = reverse('product-detail', args=[self.product_id])
        data = {
            'kd_product': 'P001U',
            'nm_product': 'Produk Update',
            'price': 15000
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Product Updated')
        self.assertEqual(response.data['data']['kd_product'], 'P001U')

    def test_delete_product(self):
        url = reverse('product-detail', args=[self.product_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data['message'], 'Product Deleted')

```

```py
# Test semua
python manage.py test

# Test per folder
python manage.py test product/
```

```json
//coba/request.rest

//API PRODUCT
### 1. CREATE 
POST http://localhost:8000/api/product/ 
content-type: application/json

{
"kd_product": "KPS002", "nm_product": "Kipas Angin", "price" :2000
}

### 2. GET ALL
GET http://localhost:8000/api/product/ HTTP/1.1

### 3. GET BY ID
GET http://localhost:8000/api/product/2/ HTTP/1.1

### 4. UPDATE BY ID
PUT http://localhost:8000/api/product/2/ HTTP/1.1
content-type: application/json

{
"kd_product": "KPS002", "nm_product": "Kipas UPDATE", "price" :2000
}

### 5. DELETE BY ID
DELETE  http://localhost:8000/api/product/1/ HTTP/1.1
```


## 5. CUSTOMER APP

1. Membuat App customer

MASUK VENV `.venv/Scripts/activate`

```py
python manage.py startapp customer
```
2. Membuat tabel SQLITE tanpa ORM

```py
python3 manage.py dbshell
```

```sql
CREATE TABLE tb_customer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nm_customer TEXT NOT NULL,
    alamat TEXT NOT NULL,
    email TEXT NOT NULL,
    nohp TEXT NOT NULL
);
```
```py
.tables
```

4. FOLDER UTAMA
```py
# restapi/urls.py >> URL UTAMA
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ini yang penting: path ini HARUS ada
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    # Include routes dari apps
    path('api/', include('coba.urls')),  # Coba App
    path('api/', include('product.urls')), #Product App
    path('api/', include('customer.urls')), #Customer App

     # 🔍 Swagger UI >> API Dokumentasi >> AUTO
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

```
4. CUSTOMER APP

```py
#/customer/serializer.py >>validation dan swagger input
from rest_framework import serializers

class CustomerInputSerializer(serializers.Serializer):
    nm_customer = serializers.CharField()
    alamat = serializers.CharField()
    email = serializers.EmailField()
    nohp = serializers.CharField()

class CustomerOutputSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nm_customer = serializers.CharField()
    alamat = serializers.CharField()
    email = serializers.EmailField()
    nohp = serializers.CharField()

#/customer/services.py >>raw SQL
from restapi.utils.db import execute_query

def get_all_customers():
    return execute_query("SELECT * FROM tb_customer")

def get_customer_by_id(customer_id):
    return execute_query("SELECT * FROM tb_customer WHERE id = %s", [customer_id], fetchone=True)

def delete_customer(customer_id):
    execute_query("DELETE FROM tb_customer WHERE id = %s", [customer_id], fetchall=False)

def create_customer(data):
    query = """
        INSERT INTO tb_customer (nm_customer, alamat, email, nohp)
        VALUES (%s, %s, %s, %s)
        RETURNING id, nm_customer, alamat, email, nohp
    """
    params = [data['nm_customer'], data['alamat'], data['email'], data['nohp']]
    return execute_query(query, params, fetchone=True)

def update_customer(customer_id, data):
    query = """
        UPDATE tb_customer
        SET nm_customer = %s, alamat = %s, email = %s, nohp = %s
        WHERE id = %s
        RETURNING id, nm_customer, alamat, email, nohp
    """
    params = [data['nm_customer'], data['alamat'], data['email'], data['nohp'], customer_id]
    return execute_query(query, params, fetchone=True)

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

#customer/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomerViewSet

router = DefaultRouter()
router.register(r'customers', CustomerViewSet, basename='customer')

urlpatterns = [
    path('', include(router.urls)),
]
```

```py 
#/customer/tests.py
import json
from django.test import TestCase, Client
from rest_framework import status
from django.urls import reverse
from django.db import connection

class CustomerViewSetTests(TestCase):
    def setUp(self):
        self.client = Client()
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tb_customer (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nm_customer TEXT NOT NULL,
                    alamat TEXT NOT NULL,
                    email TEXT NOT NULL,
                    nohp TEXT NOT NULL
                )
            """)
            cursor.execute("""
                INSERT INTO tb_customer (nm_customer, alamat, email, nohp)
                VALUES (%s, %s, %s, %s)
            """, ['edy1', 'Semarang1', 'edy1@gmail.com', '08122888881'])
            self.customer_id = cursor.lastrowid

    def tearDown(self):
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM tb_customer")

    def test_list_customers(self):
        url = reverse('customer-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_retrieve_customer(self):
        url = reverse('customer-detail', args=[self.customer_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['nm_customer'], 'edy1')

    def test_create_customer(self):
        url = reverse('customer-list')
        data = {
            'nm_customer': 'edy2',
            'alamat': 'Semarang2',
            'email': 'edy2@gmail.com',
            'nohp': '08122888882',
        }
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_customer(self):
        url = reverse('customer-detail', args=[self.customer_id])
        data = {
            'nm_customer': 'edy1 updated',
            'alamat': 'Jakarta',
            'email': 'edy1_new@gmail.com',
            'nohp': '08122999999',
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_delete_customer(self):
        url = reverse('customer-detail', args=[self.customer_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)

```

TESTING
```py
# Test semua
python manage.py test

# Test per folder
python manage.py test customer/
```

```json
//coba/request.rest

//API CUSTOMER
### 1. CREATE 
POST http://localhost:8000/api/customer/ 
content-type: application/json

{
"nm_customer": "edy1", "alamat": "Semarang2", "email" :"edy2@gmail.com", "nohp" : "08122888882"
}

### 2. GET ALL
GET http://localhost:8000/api/customer/ HTTP/1.1

### 3. GET BY ID
GET http://localhost:8000/api/customer/2/ HTTP/1.1

### 4. UPDATE BY ID
PUT http://localhost:8000/api/customer/2/ HTTP/1.1
content-type: application/json

{
"nm_customer": "edy1 UPDATE", "alamat": "Semarang2", "email" :"edy2@gmail.com", "nohp" : "08122888882"
}

### 5. DELETE BY ID
DELETE  http://localhost:8000/api/customer/1/ HTTP/1.1
```



## 6. AUTH