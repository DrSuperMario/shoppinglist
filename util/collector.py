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


html_list = list()
list_of_products = list()
list_of_prices = list()
dict_of_products = dict()

def master():

    req = requests.get('https://www.selver.ee/')
    soup = BS4(req.content, features='html.parser')
    #esilehelt URL otsingu regex
    url_class = re.compile(r'(item level0 nav.\w+.+\d)')
    #Hinna ja toote otsingu regex
    product_class = re.compile(r'(col-lg-3 \w+).+') 
    price_and_qty = re.compile(r'\s+(\d+.+)')
    #Leia kõik HTML Li tagilt mis hoiab URLi
    find_tag = soup.find_all('li',{'class':url_class})
    #leia URL'id ja lista toote nimekirja pikkus
    get_urls = [i.find_next('a').get('href')+"/?limit=96&p=" for i in find_tag]


    #start of the urls and end of the URLS
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
            html_list.append(soup)  
            print(f"Page URL: {get_urls[z]+str(i)} Last page is: {find_product_last_page}")

        for y in range(len(html_list)):  
            find_product_group = html_list[y].find_all('li',{'class':product_class})
            find_product_group_prices = html_list[y].find_all('span',{'class':'price'})
            find_product_group_titles = [i.find_next('a').get('title') for i in find_product_group]
            prices = [dedent(i.text.replace(u'\xa0',' ')) for i in find_product_group_prices if len(i) > 1]
            for t,f in zip(find_product_group_titles,prices):
                dict_of_products.update({t:re.split(price_and_qty,f)[:2]})
    
    return dict_of_products 


if(__name__=="__main__"):

    table_conn = create_engine('sqlite:///selver_data.db', echo=True)

    dict_of_producrs = master()

    toode = [{'Toode':x,'Hind':y[0],'Hind/Kogus':y[1]} for x,y in dict_of_products.items()]


    with table_conn.connect() as conn:

        meta = MetaData(table_conn)
        table = Table(
                        'Selver', meta,
                        Column('id', Integer, primary_key=True, autoincrement=True),
                        Column('Toode', String),
                        Column('Hind', String),
                        Column('Hind/Kogus', String),
                 )

        meta.create_all()

        conn.execute(table.insert(None),toode)
        

