import mysql.connector
# pip install mysql-connector-python==8.0.29
class Connector:
    def __init__(self):
        config = {
            'user': 'root',
            'password': '',
            'host': '127.0.0.1',
            'database': 'northwind',
        }
        self.cnx = mysql.connector.connect(**config)
        self.cur = self.cnx.cursor(dictionary=True)