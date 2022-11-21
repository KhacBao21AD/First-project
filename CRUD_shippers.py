from server import app, API_KEY
from flask import request
from CRUD_functions import CRUD


# key = ['ShipperID','CompanyName','Phone']
obligatory_keys = ['CompanyName', 'Phone']
crud = CRUD('shippers', obligatory_keys, 'ShipperID')


@app.route('/read_shipper')
def read_shipper():
    return crud.read()


@app.route('/create_shipper', methods=["POST"])
def create_shipper():
    data = request.form.to_dict()
    return crud.create(data)


@app.route('/update_shipper/<int:id>', methods=["PUT"])
def update_shipper(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_shipper/<int:id>', methods=["DELETE"])
def delete_shipper(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}