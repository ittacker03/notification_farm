import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# unused class
class Web_Crawler:
    def __init__(self, start_url):
        self.start_url = start_url
        self.soup = None
        self.get_html()

    def get_html(self):
        response = requests.get(self.start_url, timeout=10)
        response.raise_for_status()
        self.soup = BeautifulSoup(response.text, "html.parser")

class STnotice_Crawler(Web_Crawler):
    def __init__(self):
        super().__init__(start_url = 'https://www.seoultech.ac.kr/service/info/matters/?allboard=true&bidx=6112&bnum=6112&page=1&size=12')
        self.page = 1
        self.notice_list = []
        self.extract_notices()
    def extract_notices(self):
        self.get_html()
        for notice in self.soup.find_all("tr", class_="body_tr"):
            num = notice.find_all("td")[0].get_text(strip=True)
            title = notice.find_all("td")[1].get_text(strip=True)
            end_url = notice.find_all("td")[1].find("a")["href"]
            writer = notice.find_all("td")[3].get_text(strip=True)
            date = notice.find_all("td")[4].get_text(strip=True)
            views = notice.find_all("td")[5].get_text(strip=True)

            if title and "do=commonview" in end_url:
                notice_url = urljoin(self.start_url, end_url)

                self.notice_list.append({
                    "num": num,
                    "title": title,
                    "url": notice_url,
                    "writer": writer,
                    "date": date,
                    "views": views
                })
    def set_page(self, page):
        self.page = page
        self.start_url = f'https://www.seoultech.ac.kr/service/info/matters/?allboard=true&bidx=6112&bnum=6112&page={self.page}&size=12'
        self.notice_list.clear()
        self.extract_notices()
    def get_notices(self):
        return self.notice_list
