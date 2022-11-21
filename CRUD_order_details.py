from server import app, API_KEY
from flask import request
from CRUD_functions import CRUD
'''
column = ['ID','OrderID','ProductID','UnitPrice','Quantity','Discount'] 
'''

obligatory_keys = ['OrderID', 'ProductID', 'UnitPrice', 'Quantity', 'Discount']
crud = CRUD('order_details', obligatory_keys, 'ID')


@app.route('/read_order_detail')
def read_order_detail():
    return crud.read()


'''
ORDER DETAIL WILL BE CREATED WHEN SYSTEM HAVE NEW ORDER (CREATE ORDER)

@app.route('/create_order_detail', methods=["POST"])
def create_order_detail():
    data = request.form.to_dict()
    try:
        keys = [*data]
        keys = str(keys).replace("[", "(").replace("]", ")").replace("'", "")
        values = [*data.values()]
        values = str(values).replace("[", "").replace("]", "")

        sql = f"""
        INSERT INTO order_details {keys}
        VALUES ({values});
        """

        cursor.execute(sql)
        con.commit()
    except Exception as e:
        return {"message": f"Some error {e}"}
    return {"message": "Create order_detail successfully !"}
'''


@app.route('/update_order_detail/<string:id>', methods=["PUT"])
def update_order_detail(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_order_detail/<string:id>', methods=["DELETE"])
def delete_order_detail(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}
