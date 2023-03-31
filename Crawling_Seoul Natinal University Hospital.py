import requests
from bs4 import BeautifulSoup
import json


def get_link_list_per_page(num):
    url = f"https://terms.naver.com/list.naver?cid=51007&categoryId=51007&page={num}"
    # pg 1 ~ 118까지 있음

    response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    links = soup.select("ul > li > div.info_area > div.subject > strong > a:nth-child(1)")
    linklist = []

    for link in links:
        href = link.attrs['href']
        linklist.append("http://terms.naver.com"+href)
    
    return linklist


invalid_links = []

def get_elements(url):
    # 한 개의 페이지에 대한 요소를 크롤링하여 dictionary로 저장하는 함수
    temp_dict = {}

    response = requests.get(url)

    html = response.text
    soup = BeautifulSoup(html, 'html.parser')

    # 질병명
    title = soup.select_one("div.section_wrap > div.headword_title > h2").get_text()
    title_en = soup.select_one("div.section_wrap > div.headword_title > p.word > span").get_text()
    temp_dict['용어'] = title
    temp_dict['영문용어'] = title_en

    # 요약
    summary = soup.select_one("div.section_wrap > #size_ct > dl").get_text()
    summary = summary.split(' ', 1)[1]
    summary = summary.rstrip()
    temp_dict['요약'] = summary

    # 목차
    agendas = soup.select("#size_ct > div.tmp_agenda > ol > li")
    agendalist = []
    for agenda in agendas:
        text = agenda.get_text()
        agendalist.append(text)
    
    # 내용
    contents = soup.select("#size_ct > p")
    contentlist = []
    for content in contents:
        text = content.get_text()
        contentlist.append(text)

    if len(agendalist) != len(contentlist):
        invalid_links.append(url)
    else:
        for agenda, content in zip(agendalist, contentlist):
            temp_dict[agenda] = content
    
    print(temp_dict)

    return temp_dict


# 크롤링
medic_info = []

for i in range(1, 119):
    urls = get_link_list_per_page(i)
    for url in urls:
        medic_info.append(get_elements(url))


with open('medic_info.json','w', encoding='utf-8') as file:
    json.dump(medic_info, file, ensure_ascii=False, indent='\t')


with open('invalid_links.json','w', encoding='utf-8') as file:
    json.dump(invalid_links, file, ensure_ascii=False, indent='\t')

print(invalid_links)


'''
print(agendatype)
print(set(agendatype))

#{'식이요법/생활가이드', '관련질병', '예방방법', '원인', '치료', '증상', '진단/검사', '정의', '경과/합병증', '하위질병'}

'''