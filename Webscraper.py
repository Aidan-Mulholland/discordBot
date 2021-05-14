"""
Webscraper module to collect League champ data from U.gg
"""
import requests
from bs4 import BeautifulSoup
import json
import datetime 

class Scraper: 
    """
    Will Bennett 14/05/21 : Note scraper object which contains the function for getting champ data from u.gg
    """

    @staticmethod
    def GetChampPage(ChampName): #returns HTML page of the Champ site
        pageurl = "https://u.gg/lol/champions/"+ChampName+"/build" #page url for the specific champ

        RawHTML = requests.get(pageurl) #gets u.gg Champ HTML file
        HTMLpage = BeautifulSoup(RawHTML.content, 'html.parser') #encodes html file into BS4 object

        return HTMLpage #returns HTML page in bs4 format
        
    @staticmethod
    def GetChampItems(HTMLpage): #Gets u.gg items by looping over containers then rows then checking img URL to json to get item array. 
        BestItems = HTMLpage.find('div', class_='recommended-build_items')

        ItemImgUrls = [] #will hold the Image urls from u.gg

        for ItemImg in BestItems.find_all('div', class_='item-img'): #iterates over each Image in best items
            ImageContainer = ItemImg.find('div').find('div')['style'] #gets style string inside image container
            start = ImageContainer.find('background-image:') + 71 #gets start of the url string
            ImageUrl = ImageContainer[start:] #gets url and leading style data
            ImageUrl = Scraper.ShortenUrl(ImageUrl)
            if ImageUrl not in ItemImgUrls: #Stops doublicate items appearing
                ItemImgUrls.append(ImageUrl) #adds to list of items

        return ItemImgUrls #returns list of image urls

    @staticmethod
    def ConvertUrlToItem(ItemImgUrls): #converts image urls to item names / tokens
        with open('JSON/ImageUrlTable.json', 'r') as table: #gets dictionary of image urls to Item names
            ImageTable = json.load(table)

        Items = [] #stores best items in string(name) formate
        missing = []#list of items that are not in the JSON for debugging

        #Although this is unfavourable i will use the URL as the key as it will decrease big O to 1.
        for n, url in enumerate(ItemImgUrls): #iterates over urls and converts to Names of items, This should have a more eligant solution.
            try:
                Items.append(ImageTable[url]) #adds item name to list
            except KeyError as e:
                print(str(e) + ": Item not found")
                missing.append(str(e))# adds missing item to list

        return Items, missing #returns list of items

    @staticmethod
    def BestItem(ChampName): #returns list of best items
        HTMLpage = Scraper.GetChampPage(ChampName)
        ItemImgUrls = Scraper.GetChampItems(HTMLpage)
        return Scraper.ConvertUrlToItem(ItemImgUrls)
        
    @staticmethod
    def ShortenUrl(URLstring, n = 2):#returns end position of string to decrease likelyhood of scraping errors, n is the number of ; you want to keep.
        endIndex = [i for i, symbol in enumerate(URLstring) if symbol == ';' ][n] #gets the postition of the nth ;
        return URLstring[:endIndex] #returns shorten string

    @staticmethod
    def Test(ChampList):
        with open(ChampList, 'r') as Champs:
            Champs = json.load(Champs)['ChampNames']

        ProblemChamps = {}

        for i, champ in enumerate(Champs):
            print(f' {i} : {champ}')
            HTMLpage = Scraper.GetChampPage(champ)
            ItemImgUrls = Scraper.GetChampItems(HTMLpage)
            ItemNames, missing = Scraper.ConvertUrlToItem(ItemImgUrls)
            if missing != []:
                ProblemChamps[champ] = {'missing' : missing, 'Found' : ItemNames}
        
        with open('Logs/logtest.json', 'w+') as file:
            json.dump(ProblemChamps, file)
        return ProblemChamps

def Test_Champ(ChampName): #test function to check individual champions
    x, _ = Scraper.BestItem(ChampName)
    print(x)

if __name__ == "__main__":
    Test_Champ("fizz")
    #x = Scraper.Test("JSON/ChampList.json")   

