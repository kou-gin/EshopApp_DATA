
# dao/eshop_dao.py

from dao.db_connector import get_connection
from model.eshop import Eshop

class EshopDAO:
    def find_all(self):
        """
        テーブル 'eshops' の全件取得を行い、Eshop オブジェクトのリストとして返す。
        """
        eshops = []
        sql = "SELECT * FROM eshops ORDER BY id DESC"
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

    def get_total_count(self, search_location="", search_shop=""):
        """
        search_location や search_shop に部分一致するレコードの総件数を返す。
        """
        total_count = 0
        conditions = []
        params = []

        if search_location:
            conditions.append("location LIKE %s")
            params.append(f"%{search_location}%")
        if search_shop:
            conditions.append("shop LIKE %s")
            params.append(f"%{search_shop}%")

        sql = "SELECT count(*) AS total FROM eshops"
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, tuple(params))
            row = cursor.fetchone()
            if row:
                total_count = row.get("total", 0)
        except Exception as e:
            print("Error in get_total_count:", e)
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return total_count

    def get_list_by_search_shop(self, search_location="", search_shop=""):
        """
        search_location や search_shop に部分一致するレコードを取得し、
        Eshop オブジェクトのリストとして返す。LIMIT 200, OFFSET 0。
        """
        eshops = []
        conditions = []
        params = []

        if search_location:
            conditions.append("location LIKE %s")
            params.append(f"%{search_location}%")
        if search_shop:
            conditions.append("shop LIKE %s")
            params.append(f"%{search_shop}%")

        sql = """
            SELECT id, location, shop, detail
            FROM eshops
        """
        if conditions:
            sql += " WHERE " + " AND ".join(conditions)
        sql += " ORDER BY id DESC LIMIT %s OFFSET %s"
        params.extend([200, 0])

        conn = None
        cursor = None
        try:
            conn = get_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute(sql, tuple(params))
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
            if cursor:
                cursor.close()
            if conn:
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
