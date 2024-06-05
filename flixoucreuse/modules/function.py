from modules.importation import pd, requests, Translator

def data_importation()->tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Importe les données de deux fichiers Parquet et crée une copie de l'un des DataFrames pour une sélection par défaut.

    Returns:
        tuple: Un tuple contenant les DataFrames suivants:
            - df_film (pd.DataFrame): DataFrame contenant les données des films.
            - df_name (pd.DataFrame): DataFrame contenant les données des noms.
            - df_film_select (pd.DataFrame): Copie de df_film utilisée pour une sélection par défaut dans select box.
    """
    # Lecture des données des films à partir d'un fichier Parquet
    df_film = pd.read_parquet(r'data/bdd_clean_avant_ml_films.parquet')
    # trie du dfpour le mettre par ordre de ratings
    df_film2 = df_film.sort_values('averageRating', ascending=False).reset_index()


    # Lecture des données des noms à partir d'un fichier Parquet
    df_name = pd.read_parquet(r'data/bdd_clean_avant_ml_name.parquet')
    
    # Création d'un index d'extraction par défaut en copiant le DataFrame des films
    df_film_select = df_film2.copy()

    return df_film2, df_name, df_film_select



def trad(text:str)->str:
    """
    Traduit le texte de la langue d'origine vers le français en utilisant Google Translate.

    Args:
        text (str): Le texte à traduire.

    Returns:
        str: Le texte traduit en français.
    """
    trans = Translator()
    traduction = trans.translate(text, dest='fr')

    return traduction.text


def image_exists(url)->bool:
    """
    Vérifie si une image existe à l'URL donnée.

    Args:
        url (str): L'URL de l'image à vérifier.

    Returns:
        bool: True si une image existe à l'URL donnée, False sinon.
    """
    try:
        response = requests.get(url)
        # Vérifiez si la requête a réussi et si le contenu est une image
        if response.status_code == 200 and response.headers['content-type'].startswith('image'):
            return True
        else:
            return False
    except:
        return False
