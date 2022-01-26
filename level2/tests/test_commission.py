import unittest
import sys
sys.path.append('../')
from main import Main
from models.deals import Deals
from models.users import Users

USER_ID: int = 1
NAME: str = "Yannick"
OBJECTIVE: int = 2000

DEALS_ID: int = 1
DEALS_AMT: int = 300
DEALS_USER_ID: int = 1

DEALS2_ID:int =2
DEALS2_AMT:int= 900
DEALS2_USER_ID:int= 1


class TestCommissionPayout(unittest.TestCase):

    def setUp(self) -> None:
        self.yannick = Users(id=1,name=NAME,objective=OBJECTIVE)
        self.deal1 = Deals(id=DEALS_ID,amount=DEALS_AMT,user=DEALS_USER_ID)
        self.deal2 = Deals(id=DEALS2_ID,amount=DEALS2_AMT,user=DEALS2_USER_ID)

    def test_commission(self):
        self.assertEqual(Main.calculate_commission(self,self.yannick.objective,(self.deal1.amount+self.deal2.amount)),70)

if __name__ == "__main__":
    unittest.main()
