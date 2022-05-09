import requests
import httplib2
from bs4 import BeautifulSoup
import sys

products = {'p':[]}
    
def check_status(url):
    h = httplib2.Http()
    resp = h.request(url, 'HEAD')
    if (int(resp[0]['status']) < 400):
        return True
    else:
        return False

def scrap_euro_rtv(product_url):
    URL = product_url
    c = requests.get(URL)
    soup_content = BeautifulSoup(c.content, 'html.parser') 

    c = 0
    for i in soup_content.find_all('div', {'id':'product-list'}):
        for x in i.find_all('div', {'id': 'products'}):
            for t in x.find_all('h2', {'class':'product-name'}):
                tmp_arr=[]
                name = t.text
                tmp_arr.append(name.strip())

                href = t.find(href=True)
                url = 'www.euro.com.pl'+href['href']
                tmp_arr.append(url)   
                tmp_arr.append('EuroRtvAgd')

                price = x.find_all('div', {'class':"price-normal selenium-price-normal"})[c].get_text()
                tmp_arr.append(price.strip())
                c = c + 1

                products['p'].append(tmp_arr)
            

def scrap_mediaexpert(product_url):
    URL = product_url
    c = requests.get(URL)
    soup_content = BeautifulSoup(c.content, 'html.parser') 
    for i in soup_content.find_all('div', {'class':"offers-list"}):
        for x in i.find_all('div', {'class': 'offer-box'}):
            tmp_arr=[]
            for t in x.find_all('h2', {'class':'name is-section'}):
                name = t.text
                tmp_arr.append(name.strip())

                href = t.find(href=True)
                url = 'www.mediaexpert.pl'+href['href']
                tmp_arr.append(url)   
                tmp_arr.append('MediaExpert')

                try:
                    price = x.find_all('span', {'class':"whole"})[-1].get_text()
                    tmp_arr.append(price.strip())
                except:
                    print("Error")
                    tmp_arr.append('NaN')

            products['p'].append(tmp_arr)
                

def run_euro():
    euro_list = ['https://www.euro.com.pl/gry-playstation-5.bhtml', 'https://www.euro.com.pl/gry-playstation-4.bhtml', 'https://www.euro.com.pl/gry-xbox-series.bhtml', 'https://www.euro.com.pl/gry-xbox-one.bhtml', 'https://www.euro.com.pl/gry-nintendo-switch.bhtml', 'https://www.euro.com.pl/gry-pc.bhtml']

    for e in euro_list:
        try:
            scrap_euro_rtv(e)
            print('EuroRTVAGD: OK.')
        except:
            print('EuroRTVAGD: ERROR.')

def run_media_old():
    #get data from mediaexpert
    #W przypadku przekroczenia maksymalnej strony, pojawia siê ca³y czas jedna strona.
    page = 1
    while True:
        if check_status(f'https://www.mediaexpert.pl/gaming/gry/gry?limit=50&page={page}'):
            scrap_mediaexpert(f'https://www.mediaexpert.pl/gaming/gry/gry?limit=50&page={page}')
            page =+ 1
            print('Working')
        else:
            print("Error: MediaExpert")
            break

def run_media():
    for p in range(33):
        try:
            scrap_mediaexpert(f'https://www.mediaexpert.pl/gaming/gry/gry?limit=50&page={p}')
            print("MediaExpert: OK.")
        except:
            print("MediaExpert: ERROR.")

def save_to_file():
    try:
        with open("games_data.csv", "w", encoding="utf-8") as f:
            for i in products['p']:
                line = ';'.join(i)
                f.write(line+'\n')
        f.close()
        print('Game_data.csv: OK.')
    except:
        print('Game_data.csv: ERROR.')

run_euro()
run_media()
save_to_file()
sys.exit()

