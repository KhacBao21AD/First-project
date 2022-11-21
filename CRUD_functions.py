from server import con, cursor


class CRUD:
    def __init__(self, table, obligatory_keys, pri_id):
        self.table = table
        self.obligatory_keys = obligatory_keys
        self.pri_id = pri_id

    def read(self):
        try:
            sql = f'''
            SELECT * FROM {self.table};   
            '''
            cursor.execute(sql)
            data = cursor.fetchall()
        except Exception as e:
            return {"message": f"Some error {e}"}
        return data

    def create(self, data):
        try:
            missing = []
            null = []

            # check missing key and value is null
            for key in self.obligatory_keys:
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
                if key not in self.obligatory_keys:
                    unknown_keys.append(key)
            if unknown_keys:
                return {"message": f"unknown key {unknown_keys} !"}

            keys = tuple([*data])
            keys = str(keys).replace("'", "")
            values = tuple([*data.values()])

            # generate number of syntax '%s' for sql statement
            syntax = "s" * len(values)  # sss
            syntax = ",%".join(syntax)  # s,%s,%s

            sql = f"INSERT INTO {self.table} {keys} VALUES (%{syntax});"

            cursor.execute(sql, values)
            con.commit()
        except Exception as e:
            return {"message": f"Some error {e}"}
        return {"message": f"Create {self.table} successfully !"}

    def update(self, id, data):
        try:
            # check unknown keys and null value
            unknown_keys = []
            null = []
            for key in data:
                if key == self.pri_id:
                    return {"message": f"You can't update {self.pri_id} !"}
                elif key not in self.obligatory_keys:
                    unknown_keys.append(key)
                else:
                    if data[key] == '':
                        null.append(key)

            if unknown_keys:
                return {"message": f"unknown key {unknown_keys} !"}
            elif null:
                return {"message": f"the value of {null} is null !"}

            for key in data:
                sql = f"UPDATE {self.table} SET {key} = %s WHERE {self.pri_id} = %s;"
                val = (data[key], id)
                cursor.execute(sql, val)
            con.commit()
        except Exception as e:
            return {"message": f"Some error {e}"}
        return {"message": f"Update {self.table} successfully !"}

    def delete(self, id):
        try:
            sql = f"DELETE FROM {self.table} WHERE {self.pri_id} = %s;"
            cursor.execute(sql, (id,))
            con.commit()
        except Exception as e:
            return {"message": f"Some error {e}"}
        return {"success": f"Successfully deleted the {self.table} id: {id}."}
