import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import st_folium

# Charger les données JSON
url = "https://jsonplaceholder.typicode.com/users"
response = requests.get(url)

if response.status_code == 200:
    users_data = response.json()
else:
    st.error("Erreur de téléchargement des données.")

# Ajouter deux utilisateurs fictifs avec leurs coordonnées géographiques
fake_users = [
    {
        "id": 11,
        "name": "John Doe",
        "username": "johndoe",
        "email": "johndoe@example.com",
        "address": {
            "street": "123 Main St",
            "suite": "Apt 4",
            "city": "Gwenborough",
            "zipcode": "12345",
            "geo": {"lat": 40.748817, "lng": -73.985428}
        },
        "phone": "123-456-7890",
        "website": "http://johndoe.com",
        "company": {"name": "Doe Enterprises"}
    },
    {
        "id": 12,
        "name": "Jane Smith",
        "username": "janesmith",
        "email": "janesmith@example.com",
        "address": {
            "street": "456 Elm St",
            "suite": "Apt 3B",
            "city": "Metropolis",
            "zipcode": "67890",
            "geo": {"lat": 34.052235, "lng": -118.243683}
        },
        "phone": "987-654-3210",
        "website": "http://janesmith.com",
        "company": {"name": "Smith Industries"}
    }
]

# Ajouter les utilisateurs fictifs aux données originales
users_data.extend(fake_users)

# Convertir les données en DataFrame Pandas
users_df = pd.DataFrame(users_data)

# Interface utilisateur avec Streamlit
st.set_page_config(page_title="Recherche d'utilisateurs", page_icon="📍", layout="wide")
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 36px;
            color: #fff;
            background-color: #3498db;
            padding: 20px;
            border-radius: 10px;
        }
        .search-box {
            padding: 20px;
            border-radius: 10px;
            background-color: #f0f0f0;
            margin-top: 20px;
        }
        .search-button {
            background-color: #3498db;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            border: none;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        .search-button:hover {
            background-color: #2980b9;
        }
        .map-container {
            margin-top: 30px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
    </style>
""", unsafe_allow_html=True)

# Title with custom styling
st.markdown('<div class="title">Bienvenue dans la recherche d\'utilisateurs !</div>', unsafe_allow_html=True)
st.markdown("Utilisez cet outil pour rechercher des utilisateurs par nom ou par ville et voir leur localisation sur la carte.")

# Choix de la recherche par ville ou par nom
search_option = st.selectbox("Sélectionnez votre méthode de recherche", ("Nom", "Ville"))

# Initialiser filtered_users dans st.session_state pour conserver l'état
if "filtered_users" not in st.session_state:
    st.session_state.filtered_users = pd.DataFrame()  # Initialisation

filtered_users = st.session_state.filtered_users  # Récupérer les données filtrées depuis l'état

# Si recherche par ville
if search_option == "Ville":
    city = st.text_input("Entrez le nom de la ville :")
    search_button = st.button("Rechercher par ville", key="city_button")
    if search_button and city:
        filtered_users = users_df[users_df['address'].apply(lambda x: x['city'].lower()).str.contains(city.lower())]
        st.session_state.filtered_users = filtered_users  # Mettre à jour l'état
        if not filtered_users.empty:
            st.write(f"**Utilisateurs trouvés dans {city.capitalize()} :**")
            st.dataframe(filtered_users[['name', 'email', 'address']], use_container_width=True)
        else:
            st.write(f"Aucun utilisateur trouvé dans la ville {city.capitalize()}.")

# Si recherche par nom
if search_option == "Nom":
    name = st.text_input("Entrez le nom de l'utilisateur :")
    search_button = st.button("Rechercher par nom", key="name_button")
    if search_button and name:
        filtered_users = users_df[users_df['name'].str.contains(name, case=False)]
        st.session_state.filtered_users = filtered_users  # Mettre à jour l'état
        if not filtered_users.empty:
            st.write(f"**Utilisateurs trouvés avec le nom {name.capitalize()} :**")
            st.dataframe(filtered_users[['name', 'email', 'address']], use_container_width=True)
        else:
            st.write(f"Aucun utilisateur trouvé avec ce nom : {name.capitalize()}.")

# Affichage des coordonnées géographiques sur une carte avec folium
if not filtered_users.empty:
    for idx, user in filtered_users.iterrows():
        lat = user['address']['geo']['lat']
        lng = user['address']['geo']['lng']

        # Créer une carte centrée sur l'utilisateur sélectionné
        user_map = folium.Map(location=[lat, lng], zoom_start=12)

        # Ajouter un marqueur pour cet utilisateur
        folium.Marker([lat, lng], popup=user['name']).add_to(user_map)

    # Afficher la carte dans Streamlit
    st.markdown("<div class='map-container'>", unsafe_allow_html=True)
    st_folium(user_map, width=700)
    st.markdown("</div>", unsafe_allow_html=True)

# Styling
st.markdown(
    """
    <style>
        .css-1v0mbdj { font-size: 20px; }
        .css-16hu7kc { background-color: #f0f0f0; }
    </style>
    """, unsafe_allow_html=True
)
