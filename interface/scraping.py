from bs4 import BeautifulSoup as bs4
import requests
import pandas as pd
import re

def get_topic(nb_pages : int):
    '''
    Returns a list with all topic URLs
    Number of URLs returned = topic_page_max * 25
    Carefull, can take some time to run, even with 'only' topic_page_max = 100
    '''

    if type(nb_pages) is not int:
        raise ValueError("Function only take Integrer")


    list_topic_urls = []

    for page in range(nb_pages):

        #Each URL_topic_page lists 25 topics.
        url_topic_page = f'https://www.jeuxvideo.com/forums/0-51-0-1-0-{25*page+1}-0-blabla-18-25-ans.htm'
        response = requests.get(url_topic_page)
        soup = bs4(response.content, "html.parser")
        for topic in soup.find_all("li"):

            post_nb = topic.find("span",class_="topic-count")
            if post_nb and post_nb.string != "Nb":
                if int(str(post_nb.string).strip()) > 19:
                    list_topic_urls.append(''.join(('https://www.jeuxvideo.com/',\
                    topic.find("a", class_="lien-jv topic-title stretched-link").get("href"))))
    return list_topic_urls

def get_post(topic_url : list):
    df = []
    url = topic_url
    test = True
    page_n = 1
    while(test):
        response = requests.get(url)
        soup = bs4(response.content, "html.parser")
        if 1 == int(soup.find('span',class_="page-active").text) and page_n != 1 or response.status_code == 404:
            break
        for post in soup.find_all("div", class_="conteneur-message"):
            # Scrap username
            username =""
            if post.select_one('span[class*="bloc-pseudo-msg text-user"]'):
                username = post.select_one('span[class*="bloc-pseudo-msg text-user"]').text.replace('\n', '').strip()

            # Scrap date of message
            date =""
            if post.select_one('span[class*="lien-jv"]'):
                date = post.select_one('span[class*="lien-jv"]').text

            # Scrap the message (join different paragraphs among 1 message)
            full_message = []
            for paraph in post.find_all("div", class_="txt-msg text-enrichi-forum"):
                x = str(paraph.findChildren("p" , recursive=False))
                x = re.sub('<.*?>', '', x)
                x= x.replace("["," ").replace("]"," ")
                full_message.append(x)

            full_message = ''.join(full_message)

            # Scrap topic
            topic = soup.find(id='bloc-title-forum').string


            df.append({'username': username, 'date': date, 'message': full_message, 'topic': topic})

        #scrap Url of the next page
        new_url = url.split('-')
        new_url[3] = str(int(new_url[3])+1)
        page_n = new_url[3]
        url = '-'.join(new_url)

    return pd.DataFrame(df)

if __name__ == '__main__':
    print("get_topic")
    urls = get_topic(10)
    print("get_topic_done")
    print(urls)
    for url in urls:
        with open("../data/new_data.csv", 'a') as f:
           get_post(url).to_csv(f, mode='a', header=f.tell()==0)
