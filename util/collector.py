import requests 
from bs4 import BeautifulSoup as BS4
from textwrap import dedent
import re
import pandas as pd
from sqlalchemy import create_engine


html_list = list()
dict_of_products = dict()

    
def master():

    
    req = requests.get('https://www.selver.ee/')
    soup = BS4(req.content, features='html.parser')

    #esilehelt URL otsingu regex
    url_class = re.compile(r'(item level0 nav.\w+.+\d)')
    #Hinna ja toote otsingu regex
    product_class = re.compile(r'(col-lg-3 \w+).+')

    #Leia kõik HTML Li tagilt mis hoiab URLi
    find_tag = soup.find_all('li', {'class': url_class})

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
                dict_of_products.update({t:re.split(r'\s+([0-9]+.[0-9]+\s+./[A-z]+)',f)[:2]})
                
        
    df = pd.DataFrame(index=dict_of_products.keys(),data=[y for _, y in dict_of_products.items()], columns=['Hind','Hind/Kogus)'])
    df.reset_index(inplace=True)
    df['ID'] = range(len(dict_of_products))
    df.to_sql('Selver_items', table_c, if_exists='replace')


if(__name__=="__main__"):

    table = create_engine("sqlite:///selver_data.db", echo=True)
    table_c = table.connect()

    master()

    with table_c.connect() as c:
        c.execute('ALTER TABLE `Selver_items` ADD PRIMARY KEY (`ID`);')

    
    table_c.close()

