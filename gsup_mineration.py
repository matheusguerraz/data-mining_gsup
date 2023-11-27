"""

Script baseado em maquina de estados (https://miro.com/app/board/uXjVNKm-ub4=/) sem utilização de bibliotecas para mineração de dados

"""

import requests
import re
import pandas as pd
from datetime import datetime

# Criar um DataFrame vazio para armazenar os dados
data_list = []
date_today = datetime.now().strftime("%d-%m-%Y")

find_products = ['whey+concentrado', 'whey+hidrolisado', 'creatina', 'pré+treino', 'multivitaminico', 'barrinha']


for search in find_products:
    url = f'https://www.gsuplementos.com.br/busca/?busca={search}'

    # Solicitar a página
    response = requests.get(url)

    # Verificar se a solicitação foi bem-sucedida (código de status 200)
    if response.status_code == 200:
        
        # Remover as partes de estilo usando expressões regulares
        content_without_style = re.sub(r'<style.*?</style>', '', response.text, flags=re.DOTALL)

        # Imprimir os primeiros 500 caracteres do conteúdo
    else:
        print(f'Erro na solicitação. Código de status: {response.status_code}')

    product = ''
    pix_value = ''
    stage = 1
    out_of_stock = 1

    for c in content_without_style:

        if   stage == 1: stage =(1 if c != 'e' else 2)
        elif stage == 2: stage =(1 if c != 'G' else 3)
        elif stage == 3: stage =(1 if c != 'r' else 4)
        elif stage == 4: stage =(1 if c != 'a' else 5)
        elif stage == 5: stage =(1 if c != 'd' else 6)
        elif stage == 6: stage =(6 if c != '3' else 7)
        elif stage == 7: stage =(6 if c != '>' else 8)  
        elif stage == 8:
            if c != '<':
                product += c
                
            else:
                data_list.append({'Nome do produto': product, 'Preço': '', 'Data da extração': ''})
                print(f'O produto {product}')
                data_list[-1]['Data da extração'] = date_today
                product = ''
                stage = 9

        if stage == 9: stage =(9 if c != 'l' else 10)
        elif stage == 10: stage =(9 if c != 'o' else 11)
        elif stage == 11: stage =(9 if c != 'r' else 12)
        elif stage == 12: stage =(9 if c != '"' else 13)
        elif stage == 13: stage =(13 if c == '$' else 14)
        elif stage == 14:
            
            if c != '<':
                pix_value += c
            else:
                data_list[-1]['Preço'] = pix_value
                print(f'Tem o valor de R${pix_value} no Pix')
                pix_value = ''
                stage = 1
        
        if stage == 9: stage =(9 if c != 'v' else 15)
        elif stage == 15: stage =(9 if c != 'e' else 16)
        elif stage == 16: stage =(9 if c != 'l' else 17)
        elif stage == 17:
            if c == '"':
                data_list[-1]['Preço'] = 'Sem estoque'
                print('Sem estoque')

                stage = 1
            else:
                stage = 9

# Criar um DataFrame a partir da lista
df = pd.DataFrame(data_list)

# Salvar o DataFrame em um arquivo Excel
df.to_excel('dados_suplementos.xlsx', index=False)




    









