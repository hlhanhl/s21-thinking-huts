from WebScraper import WebScraper
import requests
from bs4 import BeautifulSoup
import csv

class Madayp(WebScraper):
    def __init__(self):
        super().__init__('')
        self.search_terms = ['Construction','Pumps_Manufacturers','Building_materials','Construction_equipment','Construction_services','Vehicle_services','Transport','Furniture','Furniture_manufactures','Paper_Products']
        self.search_term2key_word = {'Construction':'Construction','Building_materials':'Material','Pumps_Manufacturers':'Water','Construction_equipment':'Construction','Construction_services':'Construction','Vehicle_services','Transport':'Truck','Furniture':'school supplies','Furniture_manufactures':'school supplies','Paper_Products':'school supplies'}

    def get_urls(self,term):
        url_list = []
        base_url = "http://www.madayp.com/category/"
        payload = {'api_key': '87cf9eaf91cc5f9abfb30940fb594f24', 'url': base_url+term}
        page_num = 12
        try:
            mainpage = requests.get("http://api.scraperapi.com", params=payload, timeout=60)
            soup = bs(page.content, 'html.parser')
            page_container = soup.find(class_="pages_container_top")
            text = page_container.text
            text_split = [int(s) for s in text.split() if s.isdigit()]
            page_num = int(text_split[0]/30)+1
        except:
            page_num = 12
        for i in range(1,page_num):
            url_list.append(base_url+term+"/"+str(i))
        return url_list

    def parse(self):
        for term in self.search_terms:
            url_list = self.get_urls(term)
            all_urls=[]
            all_urls_only=[]
            for url in url_list:
                payload = {'api_key': '87cf9eaf91cc5f9abfb30940fb594f24', 'url': url}
                try:
                    page = requests.get("http://api.scraperapi.com", params=payload, timeout=60)
                    #print("Connected")
                except:
                    continue
                soup1=bs(page.content, 'html.parser')
                results=soup1.find_all(class_="company g_0")
                for company in results:
                    address = company.find(class_="address")
                    a = address.find("a")
                    city=a.text
                    for site in company:
                        a = site.find('a', href=True)
                        try:
                            url=a['href']
                            if url not in all_urls_only:
                                all_urls.append([url,city])
                                all_urls_only.append(url)
                        except:
                            continue

            for url in all_urls:
                if 'company' not in url[0]:
                    continue
                url[0]="http://www.madayp.com"+url[0]
                payload = {'api_key': '87cf9eaf91cc5f9abfb30940fb594f24', 'url': url[0]}
                try:
                    page = requests.get("http://api.scraperapi.com",params=payload, timeout=30)
                except:
                    print('connection failed')
                    continue
                soup2=bs(page.content, 'html.parser')
                business = {}
                fields = [0,0,0,0]
                fields[0]=soup2.find(id = "company_name")
                fields[2]=soup2.find(class_ = "text phone")
                fields[3]=soup2.find(class_ = "text weblinks")
                fields[1]=soup2.find(class_ = "city523")
                for i in range(0,3):
                    try:
                        fields[i] = fields[i].contents[0]
                    except:
                        fields[i]=''

                try:
                    fields[3] = fields[3].contents[0].contents[0]
                except:
                    fields[3]=''

                business["name"] = fields[0]
                business["search_term"]= self.search_term2key_word[term]
                business["location"]=url[1]
                business["phone"]=fields[2]
                business["website"]=fields[3]
                if business["name"]!="":
                    self.business_list.append(business)
