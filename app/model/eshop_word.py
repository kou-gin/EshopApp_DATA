# model/eshop_word.py

class EshopWord:
    def __init__(self, search_location="", search_shop=""):
        self.search_location = search_location
        self.search_shop = search_shop
        self.total_count = 0
        self.page = 1
        self.list = []  # Eshop オブジェクトのリストを格納

    def __repr__(self):
        return (f"<EshopWord search_location='{self.search_location}', "
                f"search_shop='{self.search_shop}', "
                f"total_count={self.total_count}, page={self.page}>")
