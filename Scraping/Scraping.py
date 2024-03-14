from urllib.request import Request, urlopen
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from urllib.parse import quote

real_estate_url = 'https://www.realestate.com.kh/buy/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}


class Real_estate_scapping:
    
    def __init__(self, headers, page_number):
        """
        headers: pass block during request.
        page_number = n, n-th we want to scrap
        """
        
        self.page = page_number
        self.url_RAS = 'https://www.realestate.com.kh/buy/?page=' +str(self.page)
        self.headers = headers
        
    def get_html(self, url):
        
        rq_url_agian = Request(url, headers = self.headers)
        respone = urlopen(rq_url_agian).read()
        rs_html = bs(respone, 'html.parser')
        
        return rs_html
    def get_locations(self):

        return self.get_html(self.url_RAS).find('div', class_="css-67juzu e1p824xt0")
    
    def get_url_province(self):
    
        provices_urls = []
        
        provinces = self.get_locations().find_all('button', class_="e1ope10j0 css-ib3p51")
        
        for i in range(len(provinces)):
            url = provinces[i].span.text
            url = str(url).lower().split(' ')
            if len(url) == 2:
                url_province = 'https://www.realestate.com.kh/buy/'+url[0]+'-'+url[1]
            else: 
                url_province = 'https://www.realestate.com.kh/buy/'+url[0]


            provices_urls.append(url_province)

        return provices_urls
    
    def get_box_of_provinces(self):
        boxs_ls = []
        url_provinces = self.pages_of_province()
        for i in range(len(url_provinces)):
            url_each_pv = url_provinces[i]
            try:
                html = self.get_html(url_each_pv)
            
                boxs = html.find_all('div', class_ ="item css-16n7mg5 eq4or9x0")
                boxs_ls.append(boxs)
            except: pass
        return boxs_ls
    
    def condo_only(self, box_in_pv):
        condo_url = []
        for i in range(len(box_in_pv)):
            try:
                name = box_in_pv[i].find('div', class_="heading").text.split('$')[0]
            except: pass
            if name == 'Condo':
                condoUrl = 'https://www.realestate.com.kh'+box_in_pv[i].a['href']

                condo_url.append(condoUrl)
            else: pass

        return condo_url

    def condo_url(self):
        box_in_pv = self.get_box_of_provinces()
        condos_url = []
        for i in range(len(box_in_pv)):
            checking = self.condo_only(box_in_pv[i])
            if checking != []:
                condos_url.append(checking)
            else: pass
        
        condo_urls_ls = []
        for i in range(len(condos_url)):
            for j in condos_url[i]:
                condo_urls_ls.append(j)
                
        return condo_urls_ls
    
    def condos_in_condo_url(self):
        url_condos = self.condo_url()
        ls_condo = []
        
        for i in range(len(url_condos)):
            ht = r.get_html(url_condos[i])
            section = ht.find('div', class_="hidden").find_all('section')[0].find_all('a', href = True)
            for j in section:
                url = 'https://www.realestate.com.kh'+ j.get('href')
                ls_condo.append(url)
                    
        return ls_condo


    
    def get_data_condo(self):
    
        condo_data = []
        url_condo = self.condos_in_condo_url()
        locations = self.locatoins()
        
        dt = len(url_condo)/len(locations)
        
        for i in range(len(url_condo)):
            location = locations[int(i/dt)]
            try:
                url_earch_condo = url_condo[i]
                html_condo = self.get_html(url_earch_condo)

                box_info1 = html_condo.find('div', class_="css-1pxprz3 e1ffu0v20")
                box_info2 = html_condo.find('div', class_="css-r7o7s2 elr7wbp0")
            except: pass
            
            try:
                name_condo = box_info1.find_all('div')[0].h1.text
            except: name_condo = 'NaN'
                
            ls = ['Bedroom', 'Bathroom', 'Floor Area (m²)','Facing','Floors','Floor Level','Completion Year'] 
            bedroom, bathroom, Floor_area, Facing, Floor, Floor_Level, Completing_year = 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN' 
            
            try:
                cat_info = box_info2.find_all('div')
            except: pass
            
            for i in range(len(cat_info)):
                tx = cat_info[i].find('span', class_="text").text
                if tx == ls[0]:
                    bedroom = int(cat_info[i].find('span',class_ = "value").text)
                elif tx == ls[1]:
                    bathroom = int(cat_info[i].find('span',class_ = "value").text)
                elif tx == ls[2]:
                    Floor_area = float(cat_info[i].find('span',class_ = "value").text)
                elif tx == ls[3]:
                    Facing = cat_info[i].find('span',class_ = "value").text
                elif tx == ls[4]:
                    Floor = int(cat_info[i].find('span',class_ = "value").text)
                elif tx == ls[5]:
                    Floor_Level = float(cat_info[i].find('span',class_ = "value").text)
                elif tx == ls[6]:
                    Completing_year = int(cat_info[i].find('span',class_ = "value").text)
                else: pass
                
            try:
                prices = box_info1.find('div', class_ = 'prices')
                types = prices.find_all('span', class_ = 'prefix')
            
                for j in range(len(types)):
                    if types[j].text == 'For sale':
                        try:
                            sale = prices.find('span', class_="price-value").text.replace('$', '').split(',')
                            sale_price = float(sale[0]+sale[1])
                        except: sale_price = 'NAN'
                        rent_price = 0
                    else: 
                        try:
                                rent = prices.find('span', class_="price-value").text.replace('$', '').split(',')
                                rent_price = float(sale[0]+sale[1])
                        except: rent_price = 'NaN'
                        sale_price = 0

                    condo_data.append([name_condo,rent_price,sale_price, bedroom, bathroom, Floor_area, Facing, Floor, Floor_Level,location, Completing_year])
            except: pass
            
        return condo_data
    
    def locatoins(self):
        
        box_in_pv = self.get_box_of_provinces()
        ls = []
        ls1 = []
        ls2 = []
        pv_ls = ['Phnom Penh', 'Siem Reap', 'Sihanoukville', 'Kep', 'Kampot', 'Battambang', 'Kandal', 'Kampong Thom', 'Kampong Chhnang', 'Kampong Speu', 'Kampong Cham', 'Koh Kong', 'Pursat', 'Oddar Meanchey', 'Banteay Meanchey', 'Pailin', 'Kratie', 'Mondulkiri', 'Preah Vihear', 'Ratanakiri', 'Tboung Khmum', 'Svay Rieng', 'Takeo', 'Stung Treng', 'Prey Veng']
        for i in range(len(box_in_pv)):
            
            checking = self.condo_only(box_in_pv[int(i/(len(box_in_pv)/len(pv_ls)))])
            
            ls.append(checking)
            
        for i in range(len(ls)):
            if ls[i] != []:
                for j in ls[i]:
                    location = pv_ls[int(i/(len(ls)/len(pv_ls)))]
                    ls1.append(location)
        return ls1
    
    def to_data_frame(self):
        coloumns = ['Title', 'Rent Price', 'Sale Price', 'Bedroom', 'Bathroom', 'Floor Area','Facing','Floor','Floor Level','Location','Completing Year']
        df = pd.DataFrame(self.get_data_condo(), columns= coloumns)
        
        return df
    
    def pages_of_province(self):
        
        page = self.page
        url_pv  = self.get_url_province()
        pages_url = []
        
        for i, url in enumerate(url_pv):
            for j in range(page):
                url = url_pv[i]+f'/?page={j+1}'
                pages_url.append(url)
        return pages_url
    
        


class Kh24_scrapping:
        
    def get_html(self, url, headers):
        
        rq_url = Request(url, headers= headers)
        read_url = urlopen(rq_url).read()
        page_html = bs(read_url, 'html.parser')
        
        return page_html
    
    class Phone:
        
        def __init__(self, headers = None, pages_quntative = None, url= None):
            
            self.url = url
            self.headers = headers
            self.kh24 = Kh24_scrapping()
            self.page = pages_quntative
        
        def get_html_all_pages(self):
            
            ls_html = []
            kh24 = Kh24_scrapping()
            pages = self.page
            url = self.url
            
            for i in range(0, 50*pages, 50):
                if url:
                    each_url = url.strip()+"{i}"
                else:
                    each_url = f"https://www.khmer24.com/km/mobiles/phones.html?location=&per_page={i}"
                
                try:
                    each_html = self.kh24.get_html(each_url, self.headers)
                    ls_html.append(each_html)
                except: pass
            return ls_html
        
        def get_box_prods(self, html = None):
            if html:
                ls_html = [html]
            else:
                ls_html = self.get_html_all_pages()
            
            ls_boxs = []
            for i in range(len(ls_html)):
                box = ls_html[i].find_all('li', class_='item')
                ls_boxs.append(box)
                
            return ls_boxs
        def convert_box(self):
            boxs = self.get_box_prods()
            
            box_ls = []
            for i in range(len(boxs)):
                box_each_html = boxs[i]
                
                for j in box_each_html:
                    box_ls.append(j)
                    
            return box_ls
        
        def url_prods(self, boxs_ = None):
            
            if boxs_:
                boxs = boxs_
            else: 
                boxs = self.convert_box()
            
            url_prods = []
            for i in range(len(boxs)):
                try:
                    prod_url = quote(boxs[i].a['href'], safe=':/')
                    url_prods.append(prod_url)
                except: pass
                
                
            return url_prods
        
        def box_info_prod(self, html):
            
            return html.find('div', class_="item-short-description p-3 position-relative"), html.find('div', class_="item-detail p-3")
            
        def prods_data(self):
            
            url_prods = self.url_prods()
            url = self.url
            
            def name_price(box_info):
                try:
                    title = box_info.find('h1').text
                except: title = 'NaN'
                
                try:
                    price_box = box_info.find('b', class_="price").text.replace('$', '')
                    if ',' in price_box:
                        price_ = price_box.split(',')
                        price  = float(price_[0]+price_[1])
                    else: price = float(price_box)
        
                except: price = 'NaN'
                
                return title, price
            
            def id_locatoin(box_info):
                box_dis = box_info.find('ul', class_="list-unstyled item-info m-0").find_all('li')
                id_, location = 'NaN', 'NaN'
                if url:
                    Id_locat_detect = ['Ad ID :', 'Locations :']
                else:
                    Id_locat_detect = ['Ad ID :', 'ទីតាំង :']

                for i in range(len(box_dis)):
                    tit = box_dis[i].find('span', class_="title").text
                    feature = box_dis[i].find('span', class_="value").text

                    if tit == Id_locat_detect[0]:
                        id_ = feature
                    elif tit == Id_locat_detect[1]:
                        location = feature
                    else: pass
                return id_, location
            
            def mak_mod_stor_con(box_info1):
                
                box_dis1 = box_info1.find_all('li')
                if url:
                    detect = ['Brand:', 'Model:', 'Storage:', 'Condition:']
                else:
                    detect = ['ម៉ាក:', 'ម៉ូដែល:', 'ទំហំផ្ទុកទិន្នន័យ:', 'លក្ខខណ្ឌ:']
                make, model, storage, condition = 'NaN', 'NaN', 'NaN', 'NaN'

                for i in range(len(box_dis1)):
                    tit = box_dis1[i].find('span', class_="title").text
                    feature = box_dis1[i].find('span', class_="value").text

                    if tit == detect[0]:
                        make = feature
                    elif tit == detect[1]:
                         model = feature
                    elif tit == detect[2]:
                        storage = feature
                    elif tit == detect[3]:
                        condition = feature
                return make, model, storage, condition
            
            ls_data = []
            for i in range(len(url_prods)):
                url_each_prods = url_prods[i]
                html = self.kh24.get_html(url_each_prods, self.headers)
                
                box_info, box_info1 = self.box_info_prod(html)
                
                title, price = name_price(box_info)
                id_, location = id_locatoin(box_info)
                make, model, storage, condition = mak_mod_stor_con(box_info1)
                
                ls_data.append([title, price, id_, location, make, model, storage, condition])
            
            return ls_data
        
        def to_df(self):
            data = self.prods_data()
            col = ["Title", "Price", "Id", "Location", "Make", "Model", "Storage", "Condition"]
            
            return pd.DataFrame(data, columns = col)
        
    class Car(Phone):
                                  
        def prods_data(self, url_prods_ = None):
            url = self.url
            if url_prods_:
                url_prods = url_prods_
            else:
                url_prods = self.url_prods()
         
            def name_price(box_info):
                try:
                    title = box_info.find('h1').text
                except: title = 'NaN'

                try:
                    price_box = box_info.find('b', class_="price").text.replace('$', '')
                    if ',' in price_box:
                        price_ = price_box.split(',')
                        price  = float(price_[0]+price_[1])
                    else: price = float(price_box)

                except: price = 'NaN'

                return title, price

            def id_locatoin(box_info):
                box_dis = box_info.find('ul', class_="list-unstyled item-info m-0").find_all('li')
                id_, location = 'NaN', 'NaN'
                if url:
                    Id_locat_detect = ['Ad ID :', 'Locations :']
                else:
                    Id_locat_detect = ['Ad ID :', 'ទីតាំង :']

                for i in range(len(box_dis)):
                    tit = box_dis[i].find('span', class_="title").text
                    feature = box_dis[i].find('span', class_="value").text

                    if tit == Id_locat_detect[0]:
                        id_ = feature
                    elif tit == Id_locat_detect[1]:
                        location = feature
                    else: pass
                return id_, location

            def mak_mod_year_type_con_body_fuel_tr(box_info1):

                box_dis1 = box_info1.find_all('li')
                if url:
                    detect = ['Car Makes:', 'Car Model:', 'Year:', 'Tax Type:', 'Condition:', 'Body Type:', 'Fuel:', 'Transmission:', 'Color:']
                make, model, year, tax_type, condition, body_type, fuel, transmission, color = 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN', 'NaN'

                for i in range(len(box_dis1)):
                    tit = box_dis1[i].find('span', class_="title").text
                    feature = box_dis1[i].find('span', class_="value").text

                    if tit == detect[0]:
                        make = feature
                    elif tit == detect[1]:
                         model = feature
                    elif tit == detect[2]:
                        year = int(feature)
                    elif tit == detect[3]:
                        tax_type = feature
                    elif tit == detect[4]:
                        condition = feature
                    elif tit == detect[5]:
                        body_type = feature
                    elif tit == detect[6]:
                        fuel = feature
                    elif tit == detect[7]:
                        transmission = feature
                    elif tit == detect[8]:
                        color = feature
                return make, model, year, tax_type, condition, body_type, fuel, transmission, color

            ls_data = []
            for i in range(len(url_prods)):
                url_each_prods = url_prods[i]
                html = self.kh24.get_html(url_each_prods, self.headers)

                box_info, box_info1 = self.box_info_prod(html)

                title, price = name_price(box_info)
                id_, location = id_locatoin(box_info)
                make, model, year, tax_type, condition, body_type, fuel, transmission, color = mak_mod_year_type_con_body_fuel_tr(box_info1)

                ls_data.append([title, price, id_, location, make, model, year, tax_type, condition, body_type, fuel, transmission, color])

            return ls_data
            
        def to_df(self, data_ = None):
            if data_:
                data = data_
            else:
                data = self.prods_data()
                
            col = ["Title", "Price", "Id", "Location", 'Car Makes', 'Car Model', 'Year', 'Tax Type', 'Condition', 'Body Type', 'Fuel', 'Transmission', 'Color']

            return pd.DataFrame(data, columns = col)
        
        def get_df(self):
            
            
            header = self.headers
            
            pages = self.page
            data = []
            for i in range(0,50*pages, 50):
                
                url = self.url.strip()+f"{i}"
                htm_page = self.kh24.get_html(url, header)
                box_prod = self.get_box_prods(htm_page)
                url_prod = self.url_prods(box_prod)
                
                data_ = self.prods_data(url_prod)
                
                for j in data_:
                    data.append(j)
            df =  self.to_df(data)
            
            return df
            
 