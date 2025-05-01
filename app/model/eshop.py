# model/eshop.py

class Eshop:
    def __init__(self, id=None, location="", shop="", detail=""):
        """
        :param id: ショップID（Noneの場合は未設定）
        :param location: 店舗の立地情報
        :param shop: 店舗名
        :param detail: 店舗詳細（URL 等）
        """
        self.id = id
        self.location = location
        self.shop = shop
        self.detail = detail

    def __repr__(self):
        return f"<Eshop id={self.id}, location='{self.location}', shop='{self.shop}'>"
