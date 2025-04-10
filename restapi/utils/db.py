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

# utilitas untuk menjalankan query SQL raw di Django, dan mengubah hasilnya 
# menjadi dictionary agar lebih mudah digunakan (seperti hasil ORM). 
# Ini cocok saat kamu memakai raw SQL 

#Keuntungan:
#Ringan dan fleksibel (dibandingkan ORM)
#Bisa digunakan untuk semua DB backend Django (SQLite, PostgreSQL, MySQL)
#Return berupa dictionary → mudah digunakan di serializer atau JSON response