# model/eshop_logic.py

from dao.eshop_dao import EshopDAO

class EshopLogic:
    def execute(self, es):
        dao = EshopDAO()
        total_count = dao.get_total_count(es.search_location)
        es.total_count = total_count
        es.list = dao.get_list_by_search_shop(es.search_location)
