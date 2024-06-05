from modules.importation import st

from modules.display import (background, menu_navigation, 
                             aff_casting, aff_etoile_rate, read_st_local_img)
from modules.function import data_importation, image_exists, trad
from modules.video_display import aff_video


################################
#   importation des dataframes
################################

df_film, df_name, df_film_select = data_importation()


################################
#   gestion du film selectionné pour la navigation de page
################################

# recupération du film sélectionné en url
if 'tconst' in st.query_params:
    tconst = st.query_params["tconst"] 
    df_film = df_film[df_film['tconst']==tconst].reset_index()
    st.session_state['tconst'] = tconst
    st.session_state['affichage'] = False

elif 'tconst' in st.session_state:
    df_film = df_film[df_film['tconst']==st.session_state['tconst']].reset_index()
    st.session_state['affichage'] = False


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
#   Affichage de la page principal
################################

# gestion des cadres
col1, col2 = st.columns([1,3])
tab1, tab2 = col2.tabs(['Informations générales', 'Trailer'])
container1 = tab1.container(border=True)
container2 = tab1.container(border=True)
container3 = tab2.container(border=True)
col11, col12, col13 = container3.columns([1,4,1])

with col1:

    ################################
    #   Affichage poster et rating du film selectionné
    ################################

    chemin=f"https://image.tmdb.org/t/p/w220_and_h330_face{df_film['poster_path'][0]}"

    if image_exists(chemin):
        pass
    else:
        encode_image = read_st_local_img(r"img/poster.png")
        chemin = f"data:image/png;base64,{encode_image}"
        
    st.markdown(f"""<div style='display: flex; justify-content: center;'>
                        <img src="{chemin}" style='width:400px;'>
                    </div>
                """, unsafe_allow_html=True)
        
    
    title_format = f"""<p style="text-align: center; font-family: Arial; color: #808080; font-size: 40px; font-weight: bold;">
                            {aff_etoile_rate(df_film['averageRating'][0])}
                        </p>
                    """
    
    st.markdown(title_format, unsafe_allow_html=True)
    

with col2:
    with tab1:
        with container1:

            ################################
            #   Affichage des différentes infos concernant le film
            ################################

            # titre
            st.header(df_film['title'][0])
            
            # overview - description du film
            if (str(df_film['overview'][0]) !=""):
                st.write(trad(df_film['overview'][0]))
            
            # année de sortie et durée du film
            if (int(df_film['year_release_date'][0]) !=0) & (int(df_film['runtime'][0]) !=0):
                textAnneeDuree = f"""<B>Année de sortie :</B> {str(df_film['year_release_date'][0])} - <B>Durée du film :</B> {str(df_film['runtime'][0])} minutes"""
                st.markdown(textAnneeDuree, unsafe_allow_html=True)

            # genre
            if (str(df_film['genres'][0]) !="[]"):
                textGenre = f"""<B>Genre : </B>{str(df_film['genres'][0]).replace("' '", " - ").replace("['", "").replace("']", "")}"""
                st.markdown(textGenre, unsafe_allow_html=True)

            # pays et société de production du film 
            if (str(df_film['production_countries'][0]) !="[]") & (str(df_film['production_companies_name'][0]) !="[]"):
                textprod = f"""<B>Pays de production :</B> {str(df_film['production_countries'][0]).replace("' '", " - ").replace("['", "").replace("']", "")} - <B>Société de production : </B>{str(df_film['production_companies_name'][0]).replace("' '", " - ").replace("['", "").replace("']", "")}"""
                st.markdown(textprod, unsafe_allow_html=True)

            # version originale du film
            if (str(df_film['original_language'][0]) !="[]"):
                textVO = f"""<B>Version Originale :</B> {str(df_film['original_language'][0]).replace("' '", " - ").replace("['", "").replace("']", "").upper()}"""
                st.markdown(textVO, unsafe_allow_html=True)
            

        with container2:

            ################################
            #   Affichage du casting et prod du film selectionné
            ################################
            aff_casting(df_film)

    
    with tab2:
        with container3:
            with col11:
                pass
            with col12:
                aff_video(df_film)
            with col13:
                pass
