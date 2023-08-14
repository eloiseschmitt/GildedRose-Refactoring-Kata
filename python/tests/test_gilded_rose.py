import pytest
from approvaltests import combination_approvals

from python.gilded_rose import GildedRose
from python.model.Item import Item


def instantiate_and_update(name, sell_in, quality):
    items = [Item(name, sell_in, quality)]
    gilded_rose = GildedRose(items)
    gilded_rose.update_quality()
    return items[0]


class TestUpdateQuality:

    def test_main(self):
        """Approval tests"""
        names = ["Aged Brie", "Sulfuras", "Hand of Ragnaros",
                 "Backstage " "passes to a " "TAFKAL80ETC " "concert",
                 "toto"]
        sell_in = [0, -1, 1]
        quality = [0, 1, 51]
        combination_approvals.verify_all_combinations(instantiate_and_update,
                                                      [names, sell_in, quality])

    def test_with_quality_superior_to_zero_decrease_quality_by_one(self):
        """Ensure the quality decrease by 1 if quality superior to 0"""
        items = [Item("foo", 0, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        assert items[0].quality == 0

    @pytest.mark.parametrize("sell_in, expected_sell_in, expected_quality",
                             [(0, -1, 3), (1, 0, 2)])
    def test_with_name_in_possibilities_and_quality_inferior_to_50_increase_quality_by_one(
            self, sell_in, expected_quality, expected_sell_in):
        """Ensure the quality is increased"""
        items = [Item("Aged Brie", sell_in, 1)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        assert items[0].quality == expected_quality
        assert items[0].sell_in == expected_sell_in

    @pytest.mark.parametrize("sell_in, expected_quality", [(0, 51), (1, 51)])
    def test_with_name_in_possibilities_and_quality_superior_to_50_do_nothing(self,
                                                                              sell_in,
                                                                              expected_quality):
        items = [Item("Aged Brie", sell_in, 51)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        assert items[0].quality == expected_quality
