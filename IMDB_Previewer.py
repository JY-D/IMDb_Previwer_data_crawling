
# coding: utf-8

# In[ ]:

import requests
import re
from bs4 import BeautifulSoup
from operator import is_not
from functools import partial
from IPython.display import display, HTML

list_title = []
list_posterUrl = []
list_page = []
list_weekend_box = []
list_box = []
list_week = []

list_rate = []
list_score = []
list_gen = []
list_dir = []
list_star = []

wrong_input = 1

#clean up data list
def clenList():
    list_posterUrl[:] = []
    list_title[:] = []
    list_page[:] = []
    list_rate[:] = []
    list_score[:] = []
    list_dir[:] = []
    list_gen[:] = []
    list_star[:] = []
    list_weekend_box[:] = []
    list_box[:] = []
    list_week[:] = []
    return;

#Top Box Functions
def getPoster(beautifulSoup):
    for url in beautifulSoup.select('.posterColumn'):
        posterUrl = url.find('img')['src']
        list_posterUrl.append(posterUrl)
        #print(posterUrl)
    return;

def getUrl(beautifulSoup):
    for title in beautifulSoup.select('.titleColumn'):
        pat = '/title/[a-zA-Z0-9_]+'
        titleurl = title.select('a')
        #print(titleurl)  
        titleurlShort = re.findall(pat, ''.join(str(v) for v in titleurl) )
        #print (titleurlShort)
        pages = "http://www.imdb.com" + ''.join(titleurlShort)
        #print (pages)
        list_page.append(pages)
    return;    

def getWeekend(beautifulSoup):
    for weekend_box in beautifulSoup.select('.ratingColumn'):
        if weekend_box.string != None :
            weekend = weekend_box.string
            pat = '[0-9M\.$]+'
            weekendshort = re.findall(pat, ''.join(str(v) for v in weekend))  
            #print (''.join(weekendshort))
            list_weekend_box.append(''.join(weekendshort))
    return

def getBox(beautifulSoup):
    for total_box in beautifulSoup.select('.secondaryInfo'):    
        total = total_box.string
        #print (total)
        list_box.append(total)
    return

def getWeek(beautifulSoup):
    for week in beautifulSoup.select('.weeksColumn'):    
        num_week = week.string
        #print (num_week)
        list_week.append(num_week)
    return

#Searching function
def getPhoto(beautifulSoup):
    for url in beautifulSoup.select('.primary_photo'):
        posterUrl = url.find('img')['src']
        list_posterUrl.append(posterUrl)
        #print(posterUrl)
    #print(len(list_posterUrl))
    return;

def getResult(beautifulSoup):
    for title in beautifulSoup.select('.result_text'):        
        pat = '/title/[a-zA-Z0-9_]+'
        titleurl = title.find('a')
        #print(titleurl)
        #print(titleurl.parent.name)    
        titleurlShort = re.findall(pat, ''.join(str(v) for v in titleurl) )
        #print (titleurlShort)
        pages = "http://www.imdb.com" + ''.join(titleurlShort)
        #print (pages)
        list_page.append(pages)
        #if titleurl.parent.name == "small" :
            #del list_page[-1]
    #print(len(list_page))
    return;   

#page functions
def getTitle(beautifulSoup):
    for title in beautifulSoup.select('.title_wrapper'):
        movieTitle = title.find('h1').get_text()
        #print(movieTitle)
        list_title.append(movieTitle)
    return;    

def getRate(beautifulSoup):
    list_rate.append("N/A")
    for rate in beautifulSoup.select('.ratingValue'):
        movieRate = rate.find('span').get_text()
        #print(movieRate)
        if movieRate is not None :
            del list_rate[-1]
            list_rate.append(movieRate)        
    return;    

def getMeta(beautifulSoup):
    list_score.append("N/A")
    for score in beautifulSoup.select('.metacriticScore'):
        metaScore = score.find('span').get_text()        
        #print(metaScore)
        if metaScore is not None :
            del list_score[-1]
            list_score.append(metaScore) 
    return;

def getGenre(beautifulSoup):
    s_genres = ""
    for genre in beautifulSoup.find_all("div", { "class" : "subtext" }):
        l = 1
        for genres in genre.find_all('span', { "class" : "itemprop" }):
            #print(genres.text)
            if len(genre.find_all('span', { "class" : "itemprop" })) == 1:
                list_gen.append(genres.text)
            else :
                if l == 1 :
                    s_genres = genres.text
                else :    
                    s_genres = s_genres + ", " + genres.text
                if l == len(genre.find_all('span', { "class" : "itemprop" })) :
                    list_gen.append(s_genres)
            l = l + 1        
    #print(list_gen)
    return;

def getDir(beautifulSoup):
    list_dir.append("N/A")
    directors = ""
    for director in beautifulSoup.find_all("span", { "itemprop" : "director" }):
        if director.text is not None :
            #print(director.text)
            if ',' in director.text:
                directors = directors + director.text.replace("             ", "")
            else:
                if directors == "" :
                    del list_dir[-1]
                    list_dir.append(director.text.replace("\n", ""))
                else:
                    directors = directors + director.text
                    del list_dir[-1]
                    list_dir.append(directors.replace("\n", ""))          
    #print(list_dir)        
    return;

def getStar(beautifulSoup):
    stars = ""
    for star in beautifulSoup.find_all("span", { "itemprop" : "actors" }):       
        #print(star.text)
        if ',' in star.text:
            stars = stars + star.text.replace("             ", "")
        else:
            if stars == "" :
                list_star.append(star.text.replace("\n", ""))
            else:
                stars = stars + star.text
                list_star.append(stars.replace("\n", ""))          
    #print(list_star)        
    return;

#get page info
def getPage(page_list):    
    for page in page_list :
        resOfPage = requests.get(page)
        pageSoup = BeautifulSoup(resOfPage.text, "html.parser")
        
        getTitle(pageSoup)
        getRate(pageSoup)
        getMeta(pageSoup)
        getGenre(pageSoup)
        getDir(pageSoup)
        getStar(pageSoup)
    return;   

#main functions
def topBox():
    
    resOfBox = requests.get("http://www.imdb.com/chart/boxoffice")
    boxSoup = BeautifulSoup(resOfBox.text, "html.parser")
    
    #functions
    getPoster(boxSoup)
    getUrl(boxSoup)
    getWeekend(boxSoup)
    getBox(boxSoup)
    getWeek(boxSoup)
    getPage(list_page)
    
    #display
    print("\t\t\t\t\t" + "Rate" + "\t" + "Metascore" + "\t" +"weekend" + "\t" + "gross" + "\t" + "weeks" )
    for i in range(0, len(list_weekend_box)):
        print("----------------------------------------------------------------------------------")
        display(HTML("<img src="'"' + list_posterUrl[i]+ '"'">" ))
        print(list_title[i]
              + "\n" + list_gen[i] + "\n" +
              list_page[i] + "\t" + list_rate[i] + "\t" + list_score[i] +"\t\t"+ list_weekend_box[i] +"\t"+ list_box[i] +"\t"+ list_week[i]
             +"\nDirector: "+ list_dir[i]
             +"\nStarring: " + list_star[i] + "\n")
    print("----------------------------------------------------------------------------------")
    
    #clean list
    clenList()
       
    return

def search():
    searching = input('Search Titles form IMDB : ')
    resOfSearch = requests.get("http://www.imdb.com/find?ref_=nv_sr_fn&q=" + searching + "&s=tt")
    searchSoup = BeautifulSoup(resOfSearch.text, "html.parser")
    print("Now loading... Please wait")
    
    #functions
    getPhoto(searchSoup)
    getResult(searchSoup)
    getPage(list_page)
    #print(list_score)

    #display
    print("\t\t\t\t\t" + "Rate" + "\t" + "Metascore")
    for i in range(0, len(list_title)):
        print("----------------------------------------------------------------------------------")
        display(HTML("<img src="'"' + list_posterUrl[i]+ '"'">" ))
        print(list_title[i] 
              + "\n" + list_gen[i] + "\n" + 
              list_page[i] + "\t" + list_rate[i] + "\t" + list_score[i]
             +"\nDirector: "+ list_dir[i]
             +"\nStarring: " + list_star[i] + "\n")
    print("----------------------------------------------------------------------------------")
    
    #clean list
    clenList()
       
    return

#call main functions
while wrong_input == 1 :
    
    print("IMDB Previewer beta ver.1.00")
    userInput = input("Enter 's' for searching movies title, 'b' for top box office information, enter others for exit.")

    if userInput == 'b' :
        print("Now loading... Please wait")
        topBox()
    else : 
        if userInput == 's' :
            search()
        else :
            print("Bye")
            wrong_input = 0

