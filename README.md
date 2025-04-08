
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

## 2. COBA APP 1

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
## 3. COBA APP 2

```js
//Membuat api : coba

GET http://localhost:8000/api/test

response : {
  "message": "Hello World"
}
```