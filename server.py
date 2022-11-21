from flask import Flask
from connect_db import Connector

connector = Connector()
cursor = connector.cur
con = connector.cnx
API_KEY = "somekey"

app = Flask(__name__)


@app.route('/')
def welcome():
    return "<h1 style='text-align:center;'>WELCOME TO FIRST PROJECT</h1>"


from CRUD_customers import *
from CRUD_employees import *
from CRUD_suppliers import *
from CRUD_categories import *
from CRUD_shippers import *
from CRUD_products import *
from CRUD_orders import *
from CRUD_order_details import *
from search_info import *
from Statistical_functions import *


if __name__ == "__main__":
    app.run(debug=True, port=2424)