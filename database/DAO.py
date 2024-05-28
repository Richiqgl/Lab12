from database.DB_connect import DBConnect
from modello.Retailer import Retailer
from modello.connessioni import Connessione
class DAO():
    def __init__(self):
        pass

    @staticmethod
    def getNazioni():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT gr.Country 
                FROM go_retailers gr
                ORDER BY gr.Country ASC """
        cursor.execute(query)

        for row in cursor:
            result.append((row["Country"]))
        # print(result)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getYears():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT DISTINCT YEAR(gds.`Date` ) as anno
                    FROM go_daily_sales gds 
                    WHERE YEAR (gds.`Date`)>=2015 AND YEAR (gds.`Date`)<=2018 """
        cursor.execute(query)

        for row in cursor:
            result.append((row["anno"]))
        # print(result)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getRetailer(nazione):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT  gr.*
                FROM go_retailers gr   
                WHERE gr.Country =%s """
        cursor.execute(query,(nazione,))

        for row in cursor:
            result.append(Retailer(**row))
        # print(result)
        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getConnessioni(anno,nazione):

        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """SELECT gds.Retailer_code as codiceRetailer1, gds2.Retailer_code as codiceRetailer2, count(DISTINCT  gds2.Product_number) as Conto
                FROM go_daily_sales gds
                JOIN go_daily_sales gds2 ON gds.Product_number = gds2.Product_number
                JOIN go_retailers gr1 ON gr1.Retailer_code = gds.Retailer_code
                JOIN go_retailers gr2 ON gr2.Retailer_code = gds2.Retailer_code
                WHERE YEAR(gds.Date) = %s
                  AND YEAR(gds2.Date) = %s
                  AND gds.Retailer_code < gds2.Retailer_code
                  AND gr1.Country = %s
                  AND gr2.Country = %s
                GROUP BY gds.Retailer_code ,gds2.Retailer_code  """
        cursor.execute(query, (anno,anno,nazione,nazione))

        for row in cursor:
            result.append(Connessione(**row))
        # print(result)
        cursor.close()
        conn.close()
        return result


if __name__=="__main__":
    print(DAO.getNazioni())
    print(DAO.getYears())
    print(DAO.getRetailer("Brazil"))
    print(DAO.getConnessioni(2017,"United States"))