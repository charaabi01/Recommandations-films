from modules.importation import st, time

from modules.display import background, menu_navigation, menu_select_genres, menu_select_date, diplay_title, display_reco, display_selection
from modules.function import data_importation
from modules.machine_learning import ML_reco

################################
#   importation des dataframes
################################

df_film, df_name, df_film_select = data_importation()


################################
#   Gestion du style de la page
################################

# mise en mode large de la page streamlit
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# integration du style css
with open(r"style.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# affichage de l'image de fond
background()



################################
#   gestion de la première ouverture
################################


if 'affichage' not in st.session_state:
    st.session_state['affichage'] = True


#affichage de l'introduction F comme FLIXOUCREUSE
if st.session_state['affichage'] :

    st.session_state['affichage'] = False

    # temporisation de 5 seconde avant de rerun en supprimant l'appel de l'intro
    t=5
    time.sleep(t)
    
    st.rerun()



################################
#   gestion du film selectionné pour la navigation de page
################################

# si session_state existe alors select du film
if 'tconst' not in st.session_state:
    index = 32
    st.session_state['tconst'] = df_film['tconst'][33]
else:
    result = df_film[df_film['tconst'] == st.session_state['tconst']]
    if result.empty:
        index = 32
    else:
        index = int(df_film[df_film['tconst']==st.session_state['tconst']].index[0])
   
    

################################
#   Affichage de la sideBar
################################

# affichage du menu de navigation
menu_navigation()

# affichage du menu de selection de genre, retour de la liste des genres et dataframe filtré
df_film, options_genre_film = menu_select_genres(df_film)

# affichage du slider de date, retour des startet end year puis retour dataframe filté 
df_film, start_year, end_year = menu_select_date(df_film)


################################
#   Affichage de la page principal
################################

# gestion des cadres
ctn_titre = st.container(border=False)
ctn_princ = st.container(border=False)
col1, col2 = ctn_princ.columns([3, 1])
ctn1 = col1.container(border=False)
ctn2 = col1.container(border=True)


#cadre titre
with ctn_titre:

    ################################
    #   Affichage du titre de la page
    ################################

    diplay_title()


# cadre principale
with ctn_princ:       
    # colonne recherches et recommandation
    with col1: 
        # cadre pour bare de recherche
        with ctn1:

            ################################
            #   affichage de la barre de recherche de film
            ################################
            
            result = st.selectbox('Recherche film', df_film_select['title'], index = index)

            # génération du DataFrame concernant le film selectionné
            result_film = df_film[df_film['title']==result].reset_index()

            # vérification qu'il y a bien une valeur de retour sion affichage d'un message d'avertissement
            if result_film.empty:
                st.write('Désolé, le film choisi n\'est pas dans la plage des filtres')
            else:
                st.session_state['tconst'] = result_film['tconst'][0]


                ################################
                #   ML suite à la sélection
                ################################

                df_result = ML_reco(df_film, options_genre_film, start_year, end_year)

                # Récupérations des 5 index des films à recommandés
                list_film2 = df_result['tconst'].tolist()


                with ctn2:

                    ################################
                    #   Affichage des posters des 5 recommendatoins
                    ################################

                    display_reco(list_film2, df_film)

    # vérification que result_film renvoie une info sion ne rien afficher
    if result_film.empty:
        pass
    else:
        # colonne affichage de l'affiche du film selectionné
        with col2: 

            ################################
            #   Affichage du poster du film sélectionné
            ################################

            display_selection(result_film)



