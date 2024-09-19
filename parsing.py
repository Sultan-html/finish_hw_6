# from bs4 import BeautifulSoup
# import requests

 
# def parsing():
#     repsonse = requests.get(url='https://www.nbkr.kg/index.jsp?lang=RUS')
#     soap = BeautifulSoup(repsonse.text, 'lxml')
#     cousrer = soap.find_all('table', class_='table table-striped')
#     print()
#     for i in cousrer:
#         print(f"{i.text}")
# parsing()