#/product/services.py
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
