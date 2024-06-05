from modules.importation import st, requests, pd

# fonction non utilisé sur version en ligne pour ne pas laisser libre la clé API
# recuperation de la clé API tmdb
def get_api_key(path: str = "data/api.txt") -> str:
    """
    Récupère la clé API pour accéder à l'API de The Movie Database (TMDB) à partir d'un fichier texte.

    Parameters:
    path (str): Le chemin du fichier texte contenant la clé API.
                Par défaut, le chemin est défini sur "data/API_tmdb.txt".

    Returns:
    str: La clé API pour accéder à l'API de TMDB.
    """
    
    with open(path, 'r') as api_file:
        first_line = api_file.read()


    if first_line == "":
        first_line = st.secrets["API_KEY"]


    return first_line

    
@st.cache_data
def fetch_people_imagePath(tmdb_id: int, api_key: str = get_api_key())-> str:
    """
    Récupère le chemin de l'image de profil d'une personne à partir de son identifiant TMDB.

    Parameters:
    tmdb_id (int): L'identifiant TMDB de la personne.
    api_key (str): La clé API pour accéder à l'API de The Movie Database (TMDB).

    Returns:
    str: Le chemin de l'image de profil de la personne.
    """
    api_key = str(api_key)
    url = f'https://api.themoviedb.org/3/person/{tmdb_id}/images?api_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['profiles'])

        if len(df) != 0:
            path = df['file_path'][0] 
            return path
        else :
            return ""

    else:
        print("Erreur fetching data")



@st.cache_data 
def fetch_tmdbId_from_imdbId(my_imdb_id: str, api_key: str = get_api_key())->tuple[int,str]:
    """
    Récupère l'identifiant TMDB et le nom d'une personne à partir de son identifiant IMDb.

    Parameters:
    my_imdb_id (str): L'identifiant IMDb de la personne.
    api_key (str): La clé API pour accéder à l'API de The Movie Database (TMDB).

    Returns:
    tuple[int, str]: L'identifiant TMDB et le nom de la personne.
    """
    api_key = str(api_key)
    url = f'https://api.themoviedb.org/3/find/{my_imdb_id}?external_source=imdb_id&api_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['person_results'])

        if len(df) != 0:
            tmdb_id = int(df['id'][0])
            tmdb_name = df['original_name'][0]

            return tmdb_id, tmdb_name
        else:
            return 0, ""

    else:
        print("Erreur fetching data")

    


def display_people_image(imdb_id: str)-> tuple[str, str]:    
    """
    Affiche l'image de profil d'une personne à partir de son identifiant IMDb.

    Parameters:
    imdb_id (str): L'identifiant IMDb de la personne.

    Returns:
    tuple[str, str]: Le chemin de l'image de profil et le nom de la personne.
    """

    tmdb_id, name = fetch_tmdbId_from_imdbId(imdb_id)
    image_name = fetch_people_imagePath(tmdb_id)

    chemin = f"https://image.tmdb.org/t/p/w220_and_h330_face{image_name}" 

    return chemin, name




def fetch_idMovie_fromImdbtconst(my_imdb_id: str, api_key: str = get_api_key())->tuple[int,str]:
    """
    Récupère l'identifiant TMDB d'un film à partir de son identifiant IMDb.

    Parameters:
    my_imdb_id (str): L'identifiant IMDb du film.
    api_key (str): La clé API pour accéder à l'API de The Movie Database (TMDB).

    Returns:
    int: L'identifiant TMDB du film.
    """
        # les trois freres: tt0114732 - 37653
    api_key = str(api_key)
    url = f'https://api.themoviedb.org/3/find/{my_imdb_id}?external_source=imdb_id&api_key={api_key}'

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data['movie_results'])

        if len(df) != 0:
            tmdb_id = int(df['id'][0])
            return tmdb_id
        
        else:
            return 0

    else:
        print("Erreur fetching data")




def fetch_video_link(movie_id: int, api_key: str = get_api_key())->str:
    """
    Récupère le lien de la vidéo du trailer d'un film à partir de son identifiant TMDB.

    Parameters:
    movie_id (int): L'identifiant TMDB du film.
    api_key (str): La clé API pour accéder à l'API de The Movie Database (TMDB).

    Returns:
    str: Le lien de la vidéo du trailer sur YouTube.
    """
    api_key = str(api_key)
    url = f"https://api.themoviedb.org/3/movie/{str(movie_id)}/videos?api_key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        
        df = pd.DataFrame(data['results'])
        if len(df) != 0:
            df = df[df['type'] == 'Trailer'].reset_index()
            
            if len(df) != 0:
                youtube_key = df['key'][0]
                
                return f'https://www.youtube.com/watch?v={youtube_key}'
            else:
                return f''

    else:
        st.write("Erreur fetching data", response.status_code)
        return ''
