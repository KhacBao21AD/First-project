from server import app, API_KEY
from flask import request
from CRUD_functions import CRUD

'''
key = ['ProductID','ProductName','SupplierID','CategoryID','QuantityPerUnit','UnitPrice','UnitsInStock','UnitsOnOrder','ReorderLevel','Discontinued']
'''
obligatory_keys = ['ProductName', 'SupplierID', 'CategoryID', 'QuantityPerUnit', 'UnitPrice']
crud = CRUD('products', obligatory_keys, 'ProductID')


@app.route('/read_product')
def read_product():
    return crud.read()


@app.route('/create_product', methods=["POST"])
def create_product():
    data = request.form.to_dict()
    return crud.create(data)


@app.route('/update_product/<int:id>', methods=["PUT"])
def update_product(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_product/<int:id>', methods=["DELETE"])
def delete_product(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}
