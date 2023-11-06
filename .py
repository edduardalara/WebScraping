import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
produtos = []
valores = []
def ofertas(pagina:int):
    # página de ofertas do mercado livre
    URL = 'https://www.mercadolivre.com.br/ofertas?container_id=MLB779362-1&page=' + str(pagina)
    response = requests.get(URL)
    doc = BeautifulSoup(response.text,'html.parser')
    if response.status_code != 200:
        raise Exception('Problemas na URL: {0}'.format(response))
    # nome do produto
    produtos_tags = doc.find_all('p', class_ = 'promotion-item__title')
    for tags in produtos_tags:
        produtos.append(tags.text)
    # preço do produto
    valor_tags = doc.find_all('div', class_ = 'andes-money-amount-combo__main-container')
    for tags in valor_tags:
        valores.append(tags.text.replace('Â',''))

for p in range(1,11):
    print('Extraindo página', p)
    ofertas(p)

ml = pd.DataFrame({
    'Produtos': produtos,
    'Preços': valores,
})

ml['Preços'] = ml['Preços'].str.extract(r'(\d+[\.,]?\d*)')

ml.to_csv('mercadolivre.csv',index=False)        