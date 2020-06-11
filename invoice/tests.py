from django.test import TestCase
from . import scraper

class Test(TestCase):
    acc1 = scraper.get_invoice('xaviga@hotmail.fr', 'e22af775')
    acc2 = scraper.get_invoice('arito620@gmail.com', 'e22af775')
    empty =  scraper.get_invoice('xavier.gomez@epita.fr', 'e22af775')

    def test_connect(self):
        assert scraper.get_invoice('patate', 'toto') is None
        assert self.acc1 is not None
        assert self.acc2 is not None
        assert self.empty is not None

    def test_parse(self):
        assert len(self.acc1[0]) == 1 and len(self.acc1[1]) == 1
        assert len(self.acc2[0]) == 0 and len(self.acc2[1]) == 1
        assert len(self.empty[0]) == 0 and len(self.empty[1]) == 0
