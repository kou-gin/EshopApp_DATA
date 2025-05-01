# dao/eshop_dao.py

from dao.db_connector import get_connection
from model.eshop import Eshop

class EshopDAO:
    def find_all(self):
        """
        テーブル 'eshops' の全件取得を行い、Eshop オブジェクトのリストとして返す。
        """
        eshops = []
        sql = "SELECT * FROM eshops"
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql)
            rows = cursor.fetchall()
            for row in rows:
                eshop = Eshop(
                    id=row.get("id"),
                    location=row.get("location"),
                    shop=row.get("shop"),
                    detail=row.get("detail")
                )
                eshops.append(eshop)
        except Exception as e:
            print("Error in find_all:", e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return eshops

    def get_total_count(self, search_location):
        """
        serch_location に部分一致するレコードの総件数を返す。
        """
        total_count = 0
        search_keyword = "%" + search_location + "%"
        sql = """
            SELECT count(*) AS total
            FROM eshops
            WHERE location LIKE %s
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (search_keyword,))
            row = cursor.fetchone()
            if row:
                total_count = row.get("total", 0)
        except Exception as e:
            print("Error in get_total_count:", e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return total_count

    def get_list_by_search_shop(self, search_location):
        """
        serch_location に部分一致するレコードを取得して Eshop オブジェクトのリストとして返す。
        LIMIT 100、OFFSET 0 を使用している。
        """
        eshops = []
        search_keyword = "%" + search_location + "%"
        sql = """
            SELECT id,location, shop, detail
            FROM eshops
            WHERE location LIKE %s
            LIMIT %s OFFSET %s
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, (search_keyword, 200, 0))
            rows = cursor.fetchall()
            for row in rows:
                eshop = Eshop(
                    id=row.get("id"),
                    location=row.get("location"),
                    shop=row.get("shop"),
                    detail=row.get("detail")
                )
                eshops.append(eshop)
        except Exception as e:
            print("Error in get_list_by_search_shop:", e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()

        return eshops

    def insert_one(self, eshop):
        """
        Eshop オブジェクトの内容を 'eshops' テーブルに1件挿入する。
        """
        sql = """
            INSERT INTO eshops (location, shop, detail)
            VALUES (%s, %s, %s)
        """
        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(sql, (eshop.location, eshop.shop, eshop.detail))
            conn.commit()
        except Exception as e:
            print("Error in insert_one:", e)
        finally:
            if cursor is not None:
                cursor.close()
            if conn is not None:
                conn.close()
