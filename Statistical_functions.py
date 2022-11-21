"""
- TOP SELLER, TOP CUSTOMER. TOP PRODUCTS, TOP SUPPLIERS, HISTORY
- PROFIT (IN DAY, IN A TIME)
PROFIT NHIỀU VÒNG FOR QUÁ, CÓ CÁCH NÀO GIẢM BỚT K ???
"""
from server import app, cursor
from datetime import datetime


def check_datetime(fromm='', to=''):
    if to == '':
        try:
            sp = fromm.split('-')
            year = int(sp[0])
            month = int(sp[1])
            ngay = int(sp[2])
            day1 = datetime(year, month, ngay)
            day2 = datetime(year, month, ngay, 23, 59, 59)
            return day1, day2
        except Exception as e:
            return f"{e}\nmake sure you enter the correct format yyyy-mm-dd"
    else:
        try:
            sp_f = fromm.split('-')
            year_f = int(sp_f[0])
            month_f = int(sp_f[1])
            ngay_f = int(sp_f[2])
            fromm1 = datetime(year_f, month_f, ngay_f)

            sp_t = to.split('-')
            year_t = int(sp_t[0])
            month_t = int(sp_t[1])
            ngay_t = int(sp_t[2])
            to1 = datetime(year_t, month_t, ngay_t, 23, 59, 59)
            return fromm1, to1
        except Exception as e:
            return f"{e}\nmake sure you enter the correct format /<from:yyy-mm-dd>/<to:yyyy-mm-dd>\nEx:/1996-07-04/1996-07-22"


# 2 VÒNG FOR
@app.route('/profit/<string:fromm>', methods=['GET'])
def profit_in_a_day(fromm):
    # day = '1996-07-22'
    day = check_datetime(fromm)
    if type(day) is str:
        return day
    try:
        sql = f"""
        SELECT OrderID FROM orders WHERE OrderDate >= %s AND OrderDate <= %s;
        """
        cursor.execute(sql, (day[0], day[1]))
        inf_oid = cursor.fetchall()

        inf_oid = [datum['OrderID'] for datum in inf_oid]

        data = {
            "total_profit": 0,
            f"{fromm}": []
        }

        for oid in inf_oid:
            sql = f"""
                SELECT ProductID,UnitPrice,Quantity FROM `order_details` WHERE OrderID = '{oid}';
                """
            cursor.execute(sql)
            data_from_order_details = cursor.fetchall()
            temp_di = {
                "OrderID": oid
            }
            for inf in data_from_order_details:
                sql = f"""
                    select ProductName from  products where ProductID = '{inf['ProductID']}' 
                    """
                cursor.execute(sql)
                product_name = cursor.fetchall()[0]['ProductName']
                profit = round(inf['UnitPrice'] * inf['Quantity'], 2)
                temp_di.update({product_name: profit})
                data['total_profit'] += profit
            data[fromm].append(temp_di)
        return data
    except Exception as e:
        print(e)
        return "some error, check on server !"


# 3 VÒNG FOR LỒNG NHAU
# TÌM CÁCH KHẮC PHỤC ???
@app.route('/profit/<string:fromm>/<string:to>', methods=['GET'])
def profit_in_a_time(fromm, to):
    # fromm = '1996-07-04'
    # to = '1996-07-22'
    d = check_datetime(fromm, to)
    if type(d) is str:
        return d
    try:
        sql = f"""
        SELECT OrderDate FROM `orders` WHERE OrderDate >= %s AND OrderDate <= %s;
        """
        cursor.execute(sql, (d[0], d[1]))
        order_date = cursor.fetchall()

        order_date = [str(i['OrderDate']).split()[0] for i in order_date]  # ['1996-07-05','00:00:00']
        order_date.append("z")

        order_date = [order_date[i] for i in range(len(order_date[:-1])) if order_date[i] != order_date[i + 1]]
        data = {
            "total_profit": 0,
        }

        for day in order_date:
            data.update({day: []})
            sql = f"""
                SELECT OrderID FROM orders WHERE OrderDate >= '{day} 00:00:00' AND OrderDate <= '{day} 23:59:59';
                """
            cursor.execute(sql)
            inf_oid = cursor.fetchall()
            inf_oid = [oid['OrderID'] for oid in inf_oid]

            for oid in inf_oid:
                sql = f"""
                    SELECT ProductID,UnitPrice,Quantity FROM `order_details` WHERE OrderID = '{oid}';
                    """
                cursor.execute(sql)
                data_from_order_details = cursor.fetchall()
                temp_di = {
                    "OrderID": oid
                }
                for inf in data_from_order_details:
                    sql = f"""
                        select ProductName from  products where ProductID = '{inf['ProductID']}'
                        """
                    cursor.execute(sql)
                    product_name = cursor.fetchall()[0]['ProductName']
                    profit = round(inf['UnitPrice'] * inf['Quantity'],2)
                    temp_di.update({product_name: profit})
                    data['total_profit'] += profit
                data[day].append(temp_di)
    except Exception as e:
        return str(e)
    else: return data


@app.route('/top_seller', methods=['GET'])
def top_seller():
    try:
        sql = """
        SELECT EmployeeID FROM orders
        """
        cursor.execute(sql)
        EmployeeID = cursor.fetchall()
        EmployeeID = [key['EmployeeID'] for key in EmployeeID]

        range_num = []
        temp_num = ""
        for num in EmployeeID:
            if num != temp_num:
                temp_num = num
                range_num.append(num)

        num_order = [[EmployeeID.count(i), i] for i in range_num]
        num_order.sort(reverse=True)

        top = 1
        data = {}
        for noo, eid in num_order:
            sql = f"""
            SELECT LastName, FirstName FROM employees WHERE EmployeeID = '{eid}'
            """

            cursor.execute(sql)
            name = cursor.fetchall()
            LastName = name[0]["LastName"]
            FirstName = name[0]["FirstName"]
            data.update({top: {"EmployeeID": eid, "LastName": LastName, "FirstName": FirstName, "Num_of_orders": noo}})
            top += 1
        return data
    except Exception as e:
        return {"message": f"some error {e}"}


@app.route('/top_customer', methods=['GET'])
def top_customer():
    try:
        sql = """
        SELECT CustomerID FROM orders
        """

        cursor.execute(sql)
        CustomerID = cursor.fetchall()
        CustomerID = [key['CustomerID'] for key in CustomerID]

        temp_name = ""
        num_name = []
        for name in CustomerID:
            if name != temp_name:
                temp_name = name
                num_name.append([CustomerID.count(name), name])

        num_name.sort(reverse=True)

        index = 1
        data = {}
        for noo, cid in num_name:
            sql = f"""
                SELECT ContactName FROM customers WHERE CustomerID = '{cid}'
                """
            cursor.execute(sql)
            name = cursor.fetchall()
            ContactName = name[0]["ContactName"]
            data.update({index: {"CustomerID": cid, "ContactName": ContactName, "Num_of_order": noo, }})
            index += 1
        return data
    except Exception as e:
        return {"message": f"some error {e}"}


@app.route('/top_product', methods=['GET'])
def top_product():
    sql = """
    SELECT ProductID FROM order_details
    """
    cursor.execute(sql)
    ProductID = cursor.fetchall()
    ProductID = [key['ProductID'] for key in ProductID]

    range_num = []
    temp_num = ""
    for num in ProductID:
        if num != temp_num:
            temp_num = num
            range_num.append([ProductID.count(num), num])
    range_num.sort(reverse=True)

    index = 1
    data = {}
    for noo, pid in range_num:
        sql = f"""
            SELECT ProductName FROM products WHERE ProductID = '{pid}'
            """
        cursor.execute(sql)
        ProductName = cursor.fetchall()
        ProductName = ProductName[0]["ProductName"]
        data.update({index: {"ProductID": pid, "ProductName": ProductName, "Num_of_order": noo,}})
        index += 1

    return data


@app.route('/top_supplier', methods=['GET'])
def top_supplier():
    # SupplierID
    sql = """
        SELECT SupplierID FROM products
        """
    cursor.execute(sql)
    SupplierID = cursor.fetchall()
    SupplierID = [key['SupplierID'] for key in SupplierID]

    range_num = []
    temp_num = ""
    for num in SupplierID:
        if num != temp_num:
            temp_num = num
            range_num.append([SupplierID.count(num), num])
    range_num.sort(reverse=True)

    index = 1
    data = {}
    for nos, sid in range_num:
        sql = f"""
                SELECT ContactName FROM suppliers WHERE SupplierID = '{sid}'
                """
        cursor.execute(sql)
        ContactName = cursor.fetchall()
        ContactName = ContactName[0]["ContactName"]
        data.update({index: {"SupplierID": sid, "ContactName": ContactName, "Num_of_product": nos, }})
        index += 1

    return data


@app.route("/history/<string:id>", methods=['GET'])
def history(id):
    try:
        sql = f"""
        SELECT OrderID, EmployeeID, OrderDate FROM orders WHERE CustomerID = %s ORDER BY OrderDate DESC;
        """
        cursor.execute(sql, (id, ))
        orders = cursor.fetchall()
        data = []
        for order in orders:
            OrderID = order['OrderID']
            sql = f"""
            SELECT ProductID, UnitPrice, Quantity FROM order_details WHERE OrderID = '{OrderID}'
            """
            cursor.execute(sql)
            order_details = cursor.fetchall()
            list_product = []
            for order_detail in order_details:
                ProductID = order_detail['ProductID']
                sql = f"""
                SELECT ProductName FROM products WHERE ProductID = '{ProductID}'
                """
                cursor.execute(sql)
                product_name = cursor.fetchall()[0]['ProductName']

                di = {
                    'ProductName': product_name,
                    'UnitPrice': order_detail['UnitPrice'],
                    'Quantity': order_detail['Quantity']
                }
                list_product.append(di)
            order_date = {f"{str(order['OrderDate']).split()[0]}":list_product}
            data.append(order_date)
    except Exception as e:
        return str(e)
    else: return data