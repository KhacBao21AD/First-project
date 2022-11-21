from server import app, con, cursor, API_KEY
from flask import request
from datetime import datetime
from CRUD_functions import CRUD


'''
column = ['OrderID','CustomerID','EmployeeID','OrderDate','RequiredDate','ShippedDate','ShipVia','Freight','ShipName','ShipAddress','ShipCity','ShipRegion','ShipPostalCode','ShipCountry']

{
    "CustomerID":"FRANK",
    "EmployeeID":1,
    "Shippvia":1,
    "ShipAddress":"VKU",
    "ShipCity":"Đà Nẵng",
    "ShipRegion":"Miền Trung",
    "ShipPostalCode":"100000",
    "ShipCountry":"Việt Nam",
    "OrderDetail":{
    "11":10,
    "14":20,
    "15":5
    }
}

'''

obligatory_keys = ['CustomerID', 'EmployeeID', 'Shipvia', 'ShipAddress', 'ShipCity', 'ShipRegion', 'ShipPostalCode',
                   'ShipCountry', 'OrderDetail']
crud = CRUD('orders', obligatory_keys, 'OrderID')


@app.route('/read_order')
def read_order():
    return crud.read()


def create_order_detail(OrderID, OrderDetail):
    try:
        for key in OrderDetail:
            sql = f"""
            SELECT UnitPrice FROM products WHERE ProductID = %s
            """
            cursor.execute(sql,(key,))
            UnitPrice = cursor.fetchall()[0]['UnitPrice']

            # UnitPrice = int(OrderDetail[key])*int(UnitPrice)

            sql = f"""
            INSERT INTO order_details (OrderID,ProductID,UnitPrice,Quantity)
            VALUES (%s,%s,%s,%s)
            """
            val = (OrderID, key, UnitPrice, OrderDetail[key])
            cursor.execute(sql, val)
            con.commit()
        sql = f"""
        SELECT * FROM order_details WHERE OrderID = %s
        """
        cursor.execute(sql, (OrderID,))
        order_detail = cursor.fetchall()
        print(order_detail)
        # return order_detail
    except Exception as e:
        return e


@app.route('/create_order', methods=["POST"])
def create_order():
    try:
        # data = request.form.to_dict()
        data = request.json
        missing = []
        null = []

        # check missing key and value is null
        for key in obligatory_keys:
            try:
                if data[key] == "":
                    null.append(key)
            except KeyError:
                missing.append(key)
        if missing:
            return {"message": f"you are missing {missing} !"}
        if null:
            return {"message": f"the value of {null} is null !"}

        # check unknown keys
        unknown_keys = []
        for key in data:

            if key not in obligatory_keys:
                unknown_keys.append(key)
        if unknown_keys:
            return {"message": f"unknown key {unknown_keys} !"}

        # pop OrderDetail for create data in order_details
        # and check null in OrderDetail
        OrderDetail = data.pop("OrderDetail")
        if len([*OrderDetail]) == 0:
            return {"message": f"OrderDetail is null !"}
        else:
            for key in OrderDetail:
                if OrderDetail[key] == '':
                    return {"message": f"key {key} in OrderDetail is null !"}

        keys = tuple([*data,"OrderDate"])
        # keys.remove("OrderDetail")
        keys = str(keys).replace("'", "")

        now = datetime.now()
        OrderDate = now.strftime("%Y-%m-%d %H:%M:%S")
        values = tuple([*data.values(), OrderDate])

        # generate number of syntax '%s' for sql statement
        syntax = "s" * len(values)
        syntax = ",%".join(syntax)

        sql = f"INSERT INTO orders {keys} VALUES (%{syntax});"

        cursor.execute(sql, values)
        con.commit()

        # get the newly created OrderID
        CustomerID = data["CustomerID"]
        sql = f"""
            SELECT OrderID FROM orders WHERE CustomerID = %s AND OrderDate=%s
            """
        val = (CustomerID, OrderDate)
        cursor.execute(sql, val)
        OrderID = cursor.fetchall()[0]['OrderID']
        create_order_detail(OrderID, OrderDetail)

    except Exception as e:
        return {"message": f"Some error {e}"}
    return {"message": "Create orders successfully !"}


@app.route('/update_order/<int:id>', methods=["PUT"])
def update_order(id):
    data = request.form.to_dict()
    return crud.update(id, data)


@app.route('/delete_order/<int:id>', methods=["DELETE"])
def delete_order(id):
    api_key = request.form.to_dict()["api_key"]
    if api_key == API_KEY:
        return crud.delete(id)
    else:
        return {"success": "wrong api_key for delete !"}
