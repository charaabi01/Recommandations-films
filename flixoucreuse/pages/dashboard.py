from modules.importation import st

from modules.display import background, menu_navigation, menu_select_genres, menu_select_date, menu_select_paysProd,menu_select_real
from modules.function import data_importation
from modules.display_graph import *


################################
#   importation des dataframes
################################

flixcreuse, flixcreuse2, df_film_select = data_importation()

################################
#   Gestion du style de la page
################################

# mise en mode large de la page streamlit
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# affichage de l'image de fond
background()


################################
#   Affichage de la sideBar
################################

# affichage du menu de navigation
menu_navigation()


################################
#   Affichage et gestion des filtres (sidebar)
################################

#titre 
st.sidebar.subheader("Filtres")

# filtre sur les différents pays de production
flixcreuse, options_pays_prod = menu_select_paysProd(flixcreuse)

# filtre sur les différents réalisateurs
flixcreuse, option_realisateur = menu_select_real(flixcreuse, flixcreuse2)
    
# filtre sur les différents genres
flixcreuse, options_genre = menu_select_genres(flixcreuse)

# Filtre sur les année avec un slider
flixcreuse, min_date, max_date = menu_select_date(flixcreuse)


################################
#   Affichage de la page principal
################################

# gestion des cadres ( 4 lignes de graph et 3 colonnes)
container_titre = st.container(border=False)
container1 = st.container(border=True)
container2 = st.container(border=True)
container3 = st.container(border=True)
container4 = st.container(border=True)

col11, col21, col31 = container1.columns(3)
col12, col22, col32 = container2.columns(3)
col13, col23, col33 = container3.columns(3)
col14, col24, col34 = container4.columns(3)

st.set_option('deprecation.showPyplotGlobalUse', False)


with container_titre:

    # Titre de la page
    st.markdown("<h1 style='text-align:center;'>Dashboard</h1>", unsafe_allow_html=True)

with container1:
    with col11:

        # Top 10 des films les plus populaires
        graph_film_pop(flixcreuse)

    
    with col21:
        #Figure Top 10 des films par revenu
        graph_film_revenu(flixcreuse)

    
    with col31:
        
        #FIgure Top 10 des films par note
        graph_film_note(flixcreuse)
        

with container2:
    with col12:

        #TOP 10 des acteurs les plus présent
        graph_acteurs(flixcreuse, flixcreuse2)

    
    with col22:
        
        # TOP 10 des actrices les plus présentes
        graph_actrices(flixcreuse, flixcreuse2)

    
    with col32:

        #TOP 10 des sociétés de production
        graph_societeProd(flixcreuse)


with container3:
    with col13:
        # TOP 10 des réalisateurs les plus présent
        graph_real(flixcreuse, flixcreuse2)

    
    with col23:
        # TOP 10 des genres de films
        graph_film_genres(flixcreuse)

    
    with col33:

        # TOP 10 des pays de production
        graph_paysProd(flixcreuse)


with container4:
    with col14:
        
        # Figure Distribution du temps des films
        graph_duree_film(flixcreuse)
            
    
    with col24:    

        # Filtrer les valeurs non-nulles pour la colonne 'averageRatings'
        graph_note_moyenne(flixcreuse)


    with col34:
        pass





