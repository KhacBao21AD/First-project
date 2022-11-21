from server import app, API_KEY
from flask import request
from CRUD_functions import CRUD

'''
key = ['EmployeeID','LastName','FirstName','Title','TitleOfCourtesy','BirthDate','HireDate','Address','City','Region','PostalCode','Country','HomePhone','Extension','Photo','Notes','ReportsTo']
'''
obligatory_keys = ['LastName', 'FirstName', 'BirthDate', 'Address', 'Photo', 'Notes']
crud = CRUD('employees', obligatory_keys, 'EmployeeID')


@app.route('/read_employee')
def read_employee():
    return crud.read()


@app.route('/create_employee', methods=["POST"])
def create_employee():
    data = request.form.to_dict()
    return crud.create(data)


@app.route('/update_employee/<string:id>', methods=["PUT"])
def update_employee(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_employee/<string:id>', methods=["DELETE"])
def delete_employee(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}
