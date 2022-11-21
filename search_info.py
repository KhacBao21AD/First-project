from server import app, cursor


def search(table, key, value):
    try:
        sql = f'''
        SELECT * FROM {table} WHERE {key} = %s;
        '''
        cursor.execute(sql, (value, ))
        data = cursor.fetchall()
        if not data:
            return {'message': f"don't have any {table} have {key} is {value}"}
    except BaseException:
        return {'message': f"{table} don't have properties '{key}' !"}
    else:
        return data


@app.route('/search_product_by_categoryid/<string:CategoryID>')
def search_product_by_categoryid(CategoryID):
    return search('products', 'CategoryID', CategoryID)


# CUSTOMERS
@app.route('/search_customers/<key>/<value>', methods=['GET'])
def search_customers(key, value):
    return search('customers', key, value)


# EMPLOYEES
@app.route('/search_employees/<key>/<value>', methods=['GET'])
def search_employees(key, value):
    return search('employees', key, value)


# CATEGORY
@app.route('/search_categories/<key>/<value>', methods=['GET'])
def search_categories(key, value):
    return search('categories', key, value)


# SUPPLIER
@app.route('/search_suppliers/<key>/<value>', methods=['GET'])
def search_suppliers(key, value):
    return search('suppliers', key, value)


# SHIPPERS
@app.route('/search_shippers/<key>/<value>', methods=['GET'])
def search_shipper(key, value):
    return search('shippers', key, value)


# PRODUCT
@app.route('/search_products/<key>/<value>', methods=['GET'])
def search_product(key, value):
    return search('products', key, value)


# ORDERS
@app.route('/search_orders/<key>/<value>', methods=['GET'])
def search_orders(key, value):
    return search('orders', key, value)


# ORDER DETAILS
@app.route('/search_order_details/<key>/<value>', methods=['GET'])
def search_order_details(key, value):
    return search('order_details', key, value)