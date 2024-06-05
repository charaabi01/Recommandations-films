from modules.importation import st, pd
from modules.tmdb_api import fetch_video_link, fetch_idMovie_fromImdbtconst


def aff_video(df: pd.DataFrame)->None:
    """
    Affiche la vidéo du trailer d'un film à partir du DataFrame contenant les données du film.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données du film.
                       Doit inclure la colonne 'tconst'.

    Returns:
    None
    """

    url = fetch_video_link(fetch_idMovie_fromImdbtconst(df['tconst'][0]))

    if url != '':
        st.video(url)
