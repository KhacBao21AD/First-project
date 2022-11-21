from server import app, API_KEY
from flask import request
from CRUD_functions import CRUD

# key = ['SupplierID','CompanyName','ContactName','ContactTitle','Address','City','Region','PostalCode','Country','Phone','Fax','HomePage']

obligatory_keys = ['CompanyName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country', 'Phone']
crud = CRUD('suppliers', obligatory_keys, 'SupplierID')


@app.route('/read_supplier')
def read_supplier():
    return crud.read()


@app.route('/create_supplier', methods=["POST"])
def create_supplier():
    data = request.form.to_dict()
    return crud.create(data)


@app.route('/update_supplier/<int:id>', methods=["PUT"])
def update_supplier(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_supplier/<int:id>', methods=["DELETE"])
def delete_supplier(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}
