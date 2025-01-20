# Streamlit
#### rodar - c:caminho\streamlit run deploy_imovel.py
# Streamlit

import pandas as pd
import joblib
import streamlit as st


x_numericos = {'latitude': 0, 'longitude': 0, 'accommodates': 0, 'bathrooms': 0, 'bedrooms': 0, 'beds': 0, 'extra_people': 0,
               'minimum_nights': 0, 'ano': 0, 'mes': 0, 'n_amenities': 0, 'host_listings_count': 0}

x_tf = {'host_is_superhost': 0, 'instant_bookable': 0}

x_listas = {'property_type': ['Apartment', 'Bed and breakfast', 'Condominium', 'Guest suite', 'Guesthouse', 'Hostel', 'House', 'Loft', 'Outros', 'Serviced apartment'],
            'room_type': ['Entire home/apt', 'Hotel room', 'Private room', 'Shared room'],
            'cancellation_policy': ['flexible', 'moderate', 'strict', 'strict_14_with_grace_period']}

dicionario_armazenar = dict()
for chave, valores in x_listas.items():
        for valor in valores:
            nova_chave = f"{chave}_{valor}"
            dicionario_armazenar[nova_chave] = 0

# campo numerico
for item in x_numericos:
    if item == 'longitude' or item == 'latitude':
        valor = st.number_input(f'{item}',  # Nome
                            step=0.00001,    # Valor incremento
                            value=float(0), # Tipo
                            format='%.5f')  # Formatacao
                            
    elif item == 'extra_people':
        valor = st.number_input(f'{item}',  # Nome
                            step=0.01,      # Valor incremento
                            value=float(0)) # Tipo
        
    else:
        valor = st.number_input(f'{item}',value=0)


    x_numericos[item] = valor # alterar valor dentro do meu dicionario

# campo verdadeiro ou falso
for item in x_tf:
    valor = st.selectbox(f'{item}',     # Nome
                         ('Sim','Não')) # Opcoes

    if valor == 'Sim':
        x_tf[item] = 1
    else:
        x_tf[item] = 0


# campo de listas de itens
for item in x_listas:
    valor = st.selectbox(f'{item}',x_listas[item])
    dicionario_armazenar[f"{item}_{valor}"] = 1



botao = st.button('Prever valor do Imóvel')

if botao:
    # agrupar os dicionarios
    dicionario_armazenar.update(x_numericos)
    dicionario_armazenar.update(x_tf)

    valores_x = pd.Dataframe(dicionario_armazenar, index=[0])# todas as linhas com mesmo valor de index
    dados = pd.read_csv('dados.csv')
    colunas_ordem = list(dados.columns)[1:-1]
    '''Para reordernar um dataframer, passa uma lista de colunas na ordem que preferir (atencao!! Lista com os valores de suas colunas)'''
    valores_x = valores_x[colunas_ordem]

    modelo = joblib.load('modelo.joblib')
    preco = modelo.predict(valores_x)
    st.write(preco[0])


