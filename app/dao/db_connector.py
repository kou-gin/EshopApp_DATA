# dao/db_connector.py

import mysql.connector

def get_connection():
    """
    MySQL への接続を返す。接続パラメータは環境に合わせて設定してください。
    """
    return mysql.connector.connect(
        host="mysql80.gins-net25.sakura.ne.jp",           # ホスト名
        user="gins-net25_eshopapp",           # ユーザー名（例：root など）
        password="Ba3gkC9-",   # パスワード
        database="gins-net25_eshopapp"         # 利用するデータベース名
    )
