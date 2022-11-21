from server import app, API_KEY
from flask import request
from CRUD_functions import CRUD

# key = ['CategoryID','CategoryName','Description','Picture']
obligatory_keys = ['CategoryName', 'Description', 'Picture']
crud = CRUD('categories', obligatory_keys, 'CategoryID')


@app.route('/read_categories')
def read_categories():
    return crud.read()


@app.route('/create_categories', methods=["POST"])
def create_categories():
    data = request.form.to_dict()
    return crud.create(data)


@app.route('/update_categories/<int:id>', methods=["PUT"])
def update_categories(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_categories/<int:id>', methods=["DELETE"])
def delete_categories(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}
