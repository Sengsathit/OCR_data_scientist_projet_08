import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# Url de l'API de scoring
api_url = 'http://13.38.185.52:5000/scoring'

# Header de la page
image_url = "https://raw.githubusercontent.com/Sengsathit/OCR_data_scientist_assets/main/header_pret_a_depenser.png"
st.image(image_url, use_column_width=True)
st.markdown(
    "<h1 style='text-align: center; font-size: 48px; margin-bottom: 40px;'>Évaluation du risque de crédit</h1>", 
    unsafe_allow_html=True
)

# Champ de saisie pour le numéro de client
client_id = st.text_input("Saisir le numéro de client")

# Bouton pour soumettre le numéro de client
if st.button("Vérifier le risque"):

    if client_id:      

        # Valeur de l'ID à envoyer à l'API
        payload = {"sk_id_curr": int(client_id)}  
        try:
            # Appel vers l'API + récupération de la réponse
            response = requests.post(api_url, json=payload)

            if response.status_code == 200:
                # Récupérer les données JSON
                data = response.json()

                # Vérifier le dépassement du seuil de probabilité
                is_credit_default = data.get('probability') > data.get('threshold')

                # Affichage des informations récupérées
                st.markdown("***")
                st.subheader(f"Résultat de l'évaluation pour le client {data.get('sk_id_curr')}")
                st.write(f"Seuil de décision : {data.get('threshold') * 100:.2f}")
                st.write(f"Score du client : {data.get('probability') * 100:.2f}")

                if is_credit_default:
                    st.markdown(
                        """
                        <div style="background-color:#ffcccb;padding:10px;border-radius:5px;">
                        <strong style="color:#b30000;">Client à risque</strong>
                        </div>
                        """, unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        """
                        <div style="background-color:#d4edda;padding:10px;border-radius:5px;">
                        <strong style="color:#155724;">Client éligible pour un crédit</strong>
                        </div>
                        """, unsafe_allow_html=True
                    )

                # Trier les valeurs négatives du plus petit au plus grand
                sorted_negatives = sorted(data['feature_importances_negative'], key=lambda x: x['shap_value'])[:10]

                # Trier les valeurs positives du plus grand au plus petit
                sorted_positives = sorted(data['feature_importances_positive'], key=lambda x: x['shap_value'], reverse=True)[:10]

                # Affichage de la contribution des features
                st.markdown("<hr>", unsafe_allow_html=True)
                st.subheader('Contribution des features')

                st.text('')

                # Convertir les données en DataFrames
                df_sorted_negatives = pd.DataFrame(sorted_negatives).sort_values(by='shap_value', ascending=False)
                df_sorted_positives = pd.DataFrame(sorted_positives).sort_values(by='shap_value', ascending=True)

                # Fonction pour créer un graphique de barres horizontales avec Plotly
                def plot_feature_importance(df, title, color):
                    fig = px.bar(df, 
                                y='feature_name', 
                                x='shap_value', 
                                orientation='h', 
                                title=title, 
                                labels={'shap_value': 'SHAP Value', 'feature_name': ''},
                                color_discrete_sequence=[color])
                    return fig

                # Créer les graphiques pour les importances positives et négatives
                fig_neg = plot_feature_importance(df_sorted_negatives, 'Contributions négatives', 'gray')
                fig_pos = plot_feature_importance(df_sorted_positives, 'Contributions positives', 'orange')

                # Afficher les graphiques avec Streamlit
                st.plotly_chart(fig_neg)
                st.plotly_chart(fig_pos)

            elif response.status_code == 400:
                # Récupérer les données JSON
                data = response.json()

                # Afficher l'erreur retournée par l'API
                st.error(f"Erreur : {data['error']}")
            else :
                # Afficher l'erreur retournée par l'API
                st.error(f"Erreur : {response}")

        except Exception as e:
            # Traiter les exceptions
            st.error(f"Erreur lors de l'appel API : {e}")
    else:

        st.warning("Veuillez saisir un numéro de client.")