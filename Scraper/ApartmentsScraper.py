from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
import requests
from bs4 import BeautifulSoup
import pandas as pd


path_ChromDriver = r"C:\Users\us\Desktop\chromedriver-win64\chromedriver-win64\chromedriver.exe" 
options =Options()

options.headless =True  ## scrap without see the screen
options.add_argument('widow-size=1920x1080') #more biggr screen more data fit in the screen

driver = webdriver.Chrome(path_ChromDriver,options=options)


surface =[]
pieces=[]
rooms=[]
bathrooms=[]
state=[]
stage=[]
age=[]
houseLink =[]
cities=[]
generaleFeatures =[]
prices=[]
imagesLinks=[]







for num_page in range(1,500):

    driver.get(f"https://www.mubawab.ma/fr/sc/appartements-a-vendre:p:{num_page}")
   
    # print(imagesLinks)

    cards =driver.find_elements_by_xpath('//li[@class="listingBox w100"]')







    comp=1
    for card in cards:
        try:
            imageLinksTags=driver.find_elements_by_xpath(f'//li[@class="listingBox w100"][{comp}]//div[@aria-hidden="false"]//img')
            imagelink=imageLinksTags.get_attribute("data-url")
        except:
            imagelink='https://www.mubawab-media.com/assets/common/no-photo/m/no-photo.jpg'
        imagesLinks.append(imagelink)
        try:
            print(str(comp)+"/"+str(len(cards))+"|"+str(num_page))
            comp+=1
            link =card.get_attribute("linkref")
            houseLink.append(link)
            print('-------------------------'+link)
            page = requests.get(link)
            content=page.text
            soup =BeautifulSoup(content, 'lxml')



            ###---------features1-----------##
            try:
                carcs = soup.find('div',class_="catNav").find_all('span',class_="tagProp")
            except:
                print('no carcs found')
                carcs=[]
            # ------Price------#
            try:
                price=soup.find('div',class_="col-7").h3.text.replace('\xa0','').strip()
            except:
                print('price not')
                price =None
            prices.append(price)

            for carc in carcs:
                c =carc.text.strip()
                if 'm²' in c:
                    surface.append(c.replace('\t','').replace('\n',' '))
                elif 'Pièces' in c:
                    pieces.append(c)
                
                elif 'Chambres' in c:
                    rooms.append(c)
                elif 'ans' in c:
                    age.append(c)
                    
                elif 'état' in c or 'Nouveau' ==c or 'rénover' in c:
                    
                    state.append(c)
                elif 'bains'in  c:
                    
                    bathrooms.append(c)
                elif 'étage' in c:
                    stage.append(c)

            
            verified_lists = [surface,pieces,rooms,bathrooms,state,age,stage]
            for l in verified_lists:
                if len(l) < len(prices):
                    l.append(None)

            ###-----city----#
            try:
                city =soup.find('h3',class_="greyTit").text.strip().replace('\t','').replace('\n',' ')
                
            except:
                print('city not found')
                city=None
            cities.append(city)

            ## ------ generale features -----------#
            try:
                gen_featurers = soup.find_all("ul",class_="features-list inBlock w100")[1].find_all("span",class_="characIconText centered")
                # print(len(gen_featurers))

                feature =''
                for feat in gen_featurers:
                    feature+=feat.text+" "

                generaleFeatures.append(feature.replace('\t','').replace('\n',' '))
            except:
                print('No generalefeatures here')
                generaleFeatures.append(None)

            

        except:
            print('card error')
    print('------------------ len imageLink/prices : '+str(len(imagesLinks))+'/'+str(len(prices))+'-----------------------')     

data_dict ={'surface(m²)':surface,
'pieces':pieces,
'chambres':rooms,
'salles de bains':bathrooms,
'etat':state,
'etage':stage,
'ans':age,
'ville':cities,
'autre' :generaleFeatures,
'prix(DHs)':prices,
'lienImage':imagesLinks,
'lienArticle' :houseLink}

dataFrame = pd.DataFrame(data_dict)

dataFrame.to_csv('../data/appartements.csv' ,index=False,encoding='utf-8')
