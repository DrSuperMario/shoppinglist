
import jmespath
from dataclasses import dataclass

from resources.shopping import ShowAllShoppingLIst


@dataclass
class ParseJsonToHTML():

    DATA = ShowAllShoppingLIst()
    
    def convert(self):
        json_data = self.DATA.get()
        breakpoint()