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
