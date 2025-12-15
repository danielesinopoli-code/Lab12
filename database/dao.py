from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.rifugio import Rifugio

class DAO:
    """
    Implementare tutte le funzioni necessarie a interrogare il database.
    #commit prova
    """

    @staticmethod
    def get_all_rifugi():
        cnx= DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query="""  SELECT * FROM rifugio """
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(Rifugio(**row))
        cursor.close()
        cnx.close()
        return result

    @staticmethod
    def get_all_connessione_by_year(year):
        cnx= DBConnect.get_connection()
        cursor = cnx.cursor(dictionary=True)
        query="""  SELECT * FROM connessione WHERE anno <= %s """
        cursor.execute(query,(year,))
        result = []
        for row in cursor:
            result.append(Connessione(**row))
        cursor.close()
        cnx.close()
        return result


