
import jmespath
from dataclasses import dataclass

from resources.shopping import ShowAllShoppingLIst


@dataclass
class ParseJsonToHTML():

    DATA = ShowAllShoppingLIst()
    
    def convert(self):
        
        return self.DATA.get()
        