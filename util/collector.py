from typing import Sequence, Any
import requests 
from bs4 import BeautifulSoup as BS4
from textwrap import dedent
import re
from sqlalchemy import (
                        create_engine, 
                        insert, 
                        update, 
                        MetaData, 
                        Table, 
                        String, 
                        Column, 
                        Integer
                )

from dataclasses import dataclass

@dataclass
class Collect:

    html_list: list()
    list_of_products: list()
    list_of_prices: list()
    dict_of_products: dict()

    def __init__(self, 
                    db_conn: str=None, 
                    url: str = 'https://www.selver.ee/',
                    *args,
                    **kwargs
                ) -> None:

        self._db_conn = db_conn
        self._url = url
        self.url_class = re.compile(r'(item level0 nav.\w+.+\d)')
        self.product_class = re.compile(r'(col-lg-3 \w+).+') 
        self.price_and_qty = re.compile(r'\s+(\d+.+)')

        self.html_list = list()
        self.list_of_products = list()
        self.list_of_prices = list()
        self.dict_of_products = dict()

    
    def collect_url(self) -> Sequence[Any]:

        req = requests.get(self._url)
        soup = BS4(req.content, features='html.parser')
        find_tag = soup.find_all('li',{'class':self.url_class})
        #leia URL'id ja lista toote nimekirja pikkus
        get_urls = [i.find_next('a').get('href')+"/?limit=96&p=" for i in find_tag]

        return get_urls

    def page_data(self):

        get_urls = self.collect_url()
       
        for z in range(5,23):
            #Find product last page
            product_html = requests.get(get_urls[z])
            #puhasta ilusa seebiga
            soup = BS4(product_html.content, features='html.parser')
            try:
                find_product_last_page = soup.find('a',{'class':'last'}).text
            except AttributeError:
                find_product_last_page = 3
            
            for i in range(1,int(find_product_last_page)+1):
                product_html = requests.get(get_urls[z]+str(i))
                soup = BS4(product_html.content, features='html.parser')
                self.html_list.append(soup)  
                print(f"Page URL: {get_urls[z]+str(i)} Last page is: {find_product_last_page}")

            for y in range(len(self.html_list)):  
                find_product_group = self.html_list[y].find_all('li',{'class':self.product_class})
                find_product_group_prices = self.html_list[y].find_all('span',{'class':'price'})
                find_product_group_titles = [i.find_next('a').get('title') for i in find_product_group]
                prices = [dedent(i.text.replace(u'\xa0',' ')) for i in find_product_group_prices if len(i) > 1]
                for t,f in zip(find_product_group_titles,prices):
                    self.dict_of_products.update({t:re.split(self.price_and_qty,f)[:2]})

        return [{'toode':x,'hind':y[0],'hind_kogus':y[1]} for x,y in self.dict_of_products.items()]

def main():

    table_conn = create_engine('sqlite:///selver_data.db', echo=True)

    toode = Collect().page_data()

    with table_conn.connect() as conn:

        meta = MetaData(table_conn)
        table = Table(
                        'Selver', meta,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('toode', String),
                        Column('hind', String),
                        Column('hind_kogus', String),
                    )

        meta.create_all()

        conn.execute(table.insert(None),toode)
       

if(__name__=="__main__"):
    main()

