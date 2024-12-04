import pandas as pd
import requests
import streamlit as st

# Charger les données
url = "https://ressources.data.sncf.com/api/explore/v2.1/catalog/datasets/frequentation-gares/records?limit=100"
connexion = requests.get(url)
data = connexion.json()["results"]
dic_gare = {i: data[i] for i in range(len(data))}
df = pd.DataFrame(dic_gare).T

# Champs de saisie pour le nom de la gare, code UIC complet, code postal et segmentation DRG
nom_gare = st.text_input("Nom de la gare :")
show_by_name = st.button("Afficher par nom de la gare")
# Filtrage par nom de la gare
if nom_gare and show_by_name:
    resultats = df[df['nom_gare'].str.contains(nom_gare, case=False, na=False)]
    if not resultats.empty:
        st.write(resultats)
    else:
        st.write("Aucune gare correspondante trouvée pour le nom donné.")



code_uic_complet = st.text_input("Code UIC complet :")
show_by_uic = st.button("Afficher par code UIC complet")
# Filtrage par code UIC complet
if code_uic_complet and show_by_uic:
    resultats = df[df['code_uic_complet'] == code_uic_complet]
    if not resultats.empty:
        st.write(resultats)
    else:
        st.write("Aucune gare correspondante trouvée pour le code UIC donné.")


code_postal = st.text_input("Code postal :")
show_by_postal = st.button("Afficher par code postal")
# Filtrage par code postal
if code_postal and show_by_postal:
    resultats = df[df['code_postal'] == code_postal]
    if not resultats.empty:
        st.write(resultats)
    else:
        st.write("Aucune gare correspondante trouvée pour le code postal donné.")


segmentation_drg = st.text_input("Segmentation DRG :")
show_by_drg = st.button("Afficher par segmentation DRG")
# Filtrage par segmentation DRG
if segmentation_drg and show_by_drg:
    resultats = df[df['segmentation_drg'].str.contains(segmentation_drg, case=False, na=False)]
    if not resultats.empty:
        st.write(resultats)
    else:
        st.write("Aucune gare correspondante trouvée pour la segmentation DRG donnée.")









