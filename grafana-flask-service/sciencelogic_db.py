from helpers import Helpers
import pymysql
import os


class ScienceLogicDb:
    # Private variable
    # __db_conn = None
    # cursor = None

    def __init__(self):
        self._helpers = Helpers()
        self.env = self._helpers.get_env_path()

    def __connect(self):
        try:
            host_name = self.env['SCIENCELOGIC_DB_HOSTNAME']
            user = self.env['SCIENCELOGIC_DB_USER']
            password = self.env['SCIENCELOGIC_DB_PASSWORD']
            db_name = self.env['SCIENCELOGIC_DB_NAME']
            db_conn = pymysql.connect(
                db=db_name, user=user,
                passwd=password, host=host_name, port=7706)
            # self.cursor = self.db_conn.cursor()
            return db_conn
        except Exception as e:
            print("ScienceLogic Database Connection Error:", str(e))

    def execute(self, sql, params, prepend_column_names=False):
        rows = []
        _cursor = None
        try:
            db_conn = self.__connect()
            _cursor = db_conn.cursor()
            sql = self._helpers.replace_with_sciencelogic_dynamic_ids(sql)
            if sql is None and len(sql) == 0:
                return []
            if _cursor:
                _cursor.execute(sql, params)
                if prepend_column_names:
                    column_names = [i[0] for i in _cursor.description]
                    rows.append(column_names)

                for row in _cursor.fetchall():
                    temp_row = []
                    for value in row:
                        from decimal import Decimal
                        if not (type(value) is int or type(value) is float or type(value) is Decimal):
                            value=str(value)
                            if value.isdigit():
                                value = int(value)
                        temp_row.append(value)
                    rows.append(temp_row)
                return rows
            else:
                raise Exception("Cursor is None")
        except Exception as ex:
            print(sql.replace("\n", " "))
            print("Error: unable to fetch data :" + str(ex))
            return []
        finally:
            if _cursor is not None:
                _cursor.close()
            if db_conn is not None:
                db_conn.close()
