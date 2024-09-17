import streamlit as st
import pandas as pd
from utils.functions import load_dataset, display_banner, show_info_message, show_error_message
from utils.constants import *

def display_info_line(feature, value, additional_string=""):
    st.markdown(f"""
        <p style='font-size:24px; display:inline;'>{feature} : </p>
        <p style='font-size:16px; display:inline;'>{value} {additional_string}</p>
    """, unsafe_allow_html=True)

# Affichage de l'en-tête de la page
display_banner(title='Informations client')

try:
    data = st.session_state['data']
    df = load_dataset()

    client = df.query(f"SK_ID_CURR == {data.get('sk_id_curr')}")

    client_id = client['SK_ID_CURR'].values[0]
    display_info_line(feature='Numéro client', value=client_id)

    age = round(client['DAYS_BIRTH'].values[0] / 365)
    display_info_line(feature='Age', value=age, additional_string='ans')

    isWoman = client['CODE_GENDER_F'].values[0]
    display_info_line(feature='Sexe', value="Femme" if isWoman else "Homme")

    # Récupérer la première valeur de 'DAYS_EMPLOYED'
    days_employed = client['DAYS_EMPLOYED'].values[0]
    work_experience = round(days_employed / -365) if pd.notna(days_employed) else 'NC'
    additional_string = 'année(s)' if pd.notna(days_employed) else ""
    display_info_line(feature='Expérience professionnelle', value=work_experience, additional_string=additional_string)

    amt_income_total = client['AMT_INCOME_TOTAL'].values[0]
    if pd.notna(amt_income_total):
        income = f"{amt_income_total:,.0f}".replace(',', ' ')
    else:
        income = 'NC'
    additional_string = '$' if pd.notna(amt_income_total) else None
    display_info_line(feature='Revenu annuel', value=income, additional_string=additional_string)


    amt_credit = client['AMT_CREDIT'].values[0]
    if pd.notna(amt_credit):
        credit = f"{amt_credit:,.0f}".replace(',', ' ')
    else:
        credit = 'NC'
    additional_string = '$' if pd.notna(amt_credit) else None
    display_info_line(feature='Crédit en cours', value=credit, additional_string=additional_string)
    
except Exception as e:
    show_error_message(message='Aucune information client à afficher. Vous devez d\'abord vérifier l\'éligibilité d\'un client.')