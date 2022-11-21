from server import app, API_KEY
from flask import request
from CRUD_functions import CRUD


# keys = ['CustomerID','CompanyName','ContactName','ContactTitle','Address','City','Region','PostalCode','Country','Phone','Fax']
obligatory_keys = ['CustomerID', 'CompanyName', 'ContactName', 'Address', 'City', 'PostalCode', 'Country']
crud = CRUD('customers', obligatory_keys, 'CustomerID')


@app.route('/read_customer')
def read_customer():
    return crud.read()


@app.route('/create_customer', methods=["POST"])
def create_customer():
    data = request.form.to_dict()
    return crud.create(data)


@app.route('/update_customer/<string:id>', methods=["PUT"])
def update_customer(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_customer/<string:id>', methods=["DELETE"])
def delete_customer(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}
