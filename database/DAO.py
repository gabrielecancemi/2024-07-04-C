from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_all_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct year(s.`datetime`) as y from sighting s order by `datetime` desc"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["y"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_shapes(anno):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct shape from sighting s where shape <> "" and year(s.`datetime`) = %s order by shape asc"""
            cursor.execute(query, (anno,))

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_nodes(anno, forma):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * from sighting s where year(s.`datetime`) = %s and s.shape = %s"""
            cursor.execute(query, (anno, forma))

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result