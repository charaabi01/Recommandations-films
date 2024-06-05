from modules.importation import (st, pd, np, Pipeline, 
                                StandardScaler, FunctionTransformer, 
                                MultiLabelBinarizer, ColumnTransformer, 
                                SimpleImputer, BaseEstimator, 
                                TransformerMixin, NearestNeighbors)


def prepa_data_filtered(df:pd.DataFrame, tconst_titre:str, genres:list[str], start_end_year:list[int, int])->pd.DataFrame:
    '''
    Prépare les données filtrées en fonction des genres et de l'année.

    Args:
        df (pd.DataFrame): DataFrame contenant les informations sur les films.
        tconst_titre (str): Identifiant du film à exclure de la sélection.
        genres (list): Liste des genres à filtrer.
        start_end_year (list): Liste contenant l'année de début et l'année de fin pour le filtre par année.

    Returns:
        pd.DataFrame: DataFrame contenant les données filtrées.
    '''

    df_copy = df.copy()

    # Extraction des informations du film à exclure de la sélection
    df_film_cherche = df[df['tconst'] == tconst_titre]

    # Exclusion du film à rechercher de la sélection
    df = df[df['tconst'] != tconst_titre]

    # Filtrage par genres si des genres sont spécifiés
    if genres != []:
        df = df[df['genres'].apply(lambda x: any(genre in x for genre in genres))]

    # Filtrage par année
    df = df[(df['year_release_date'] >= start_end_year[0]) & (df['year_release_date'] <= start_end_year[1])]

    #verification que df n'est pas vide sinon on garde le df avant le trie
    if df.shape[0] == 0:
        df = df_copy
    
    del df_copy

    # Concaténation du DataFrame filtré avec les informations du film à rechercher
    df = pd.concat([df, df_film_cherche], axis=0)

    return df



def fetch_feautures_reco()->tuple[list[str], list[str], list[str]]:
    """
    Récupère les caractéristiques à utiliser pour la recommandation de films.

    Returns:
        tuple: Un tuple contenant trois listes :
               - features_std: Caractéristiques avec une standardisation directe.
               - features_log_and_std: Caractéristiques nécessitant une transformation logarithmique avant la standardisation.
               - features_cat_list: Caractéristiques catégorielles.
    """

    # features par defaut
    features_std = ['year_release_date', 'runtime', 'averageRating'] 
    features_log_and_std = ['budget', 'popularity', 'numVotes', 'revenue']
    features_cat_list =  ['genres','production_countries', 'production_companies_name', 'production_companies_country', 'actor', 'actress', 'cinematographer', 'composer', 'editor', 'producer', 'directors', 'writers']

    return features_std, features_log_and_std, features_cat_list



def prepa_transformer_stdScaler()->Pipeline:
    """
    Prépare le transformateur pour la standardisation des caractéristiques numériques.

    Returns:
        Pipeline: Pipeline contenant les étapes de transformation pour la standardisation.
    """
    # en prévision pour le feature std
    numeric_transformer_std = (Pipeline( steps= [
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('stdScaller', StandardScaler()),
        # ('pca', PCA(n_coponents=2))
    ]))

    return numeric_transformer_std



def prepa_transformer_stdScaler_Log()->Pipeline:
    """
    Prépare le transformateur pour la transformation logarithmique et la standardisation des caractéristiques numériques.

    Returns:
        Pipeline: Pipeline contenant les étapes de transformation pour la transformation logarithmique et la standardisation.
    """

    # Préparation du pipeline pour la transformation logarithmique et la standardisation des caractéristiques numériques
    numeric_transformer_log_std = (Pipeline( steps= [
        ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
        ('log_Scaler', FunctionTransformer(np.log1p)),
        ('std_caler', StandardScaler()) 
    ]))

    return numeric_transformer_log_std


    
def prepa_transformer_multiBin()->Pipeline:
    """
    Prépare le transformateur pour la transformation des caractéristiques catégorielles en utilisant MultiLabelBinarizer.

    Returns:
        Pipeline: Pipeline contenant les étapes de transformation pour MultiLabelBinarizer.
    """

    # Create a custom transformer using MultiLabelBinarizer
    class CustomMultiLabelBinarizer(BaseEstimator, TransformerMixin):
        def __init__(self):
            self.mlb = MultiLabelBinarizer(sparse_output= True)
        def fit(self, X, y=None):
            self.mlb.fit(X)
            return self
        def transform(self, X):
            return self.mlb.transform(X)

    # Préparation du pipeline pour la transformation des caractéristiques catégorielles en utilisant MultiLabelBinarizer
    category_list_transformer_multibinary = (Pipeline( steps= [
        ('Multi_bin', CustomMultiLabelBinarizer())
    ]))

    return category_list_transformer_multibinary



#### Standardize + log + binarizer
def preprocessor_SLB(features_std:list[str], features_log_and_std:list[str], features_cat_list:list[str])-> Pipeline:
    """
    Prépare le préprocesseur pour les caractéristiques standardisées, logarithmiques et catégorielles.

    Args:
        features_std (list): Liste des caractéristiques nécessitant une standardisation directe.
        features_log_and_std (list): Liste des caractéristiques nécessitant une transformation logarithmique avant la standardisation.
        features_cat_list (list): Liste des caractéristiques catégorielles.

    Returns:
        Pipeline: Pipeline contenant les étapes de prétraitement pour les caractéristiques.
    """

    # Préparation des transformateurs pour les caractéristiques numériques
    numeric_transformer_std = prepa_transformer_stdScaler()
    numeric_transformer_log_std = prepa_transformer_stdScaler_Log()

    # Préparation du transformateur pour les caractéristiques catégorielles
    category_list_transformer_multibinary = prepa_transformer_multiBin()

    # création de la liste des tuples pour la transformation en multiLabelBinarizer
    list_tuple = []
    for id, features_cat in enumerate(features_cat_list):
        list_tuple.append((f'cat_multiB{id}', category_list_transformer_multibinary, features_cat))
        

    # Combinaison des transformation pour le preprocessing
    preprocessor = ColumnTransformer(
        transformers= [
            ('num_std', numeric_transformer_std, features_std),
            ('num_log_std', numeric_transformer_log_std, features_log_and_std)
        ] + list_tuple
    )

    return preprocessor



def model_knn_module(df:pd.DataFrame, tconst_titre:str, preprocessor:Pipeline)->pd.DataFrame:
    """
    Entraîne un modèle KNN pour trouver les films les plus similaires à celui sélectionné.

    Args:
        df (pd.DataFrame): Le DataFrame contenant les données des films.
        tconst_titre (str): Le tconst du film sélectionné.
        preprocessor: Le préprocesseur utilisé pour transformer les données.

    Returns:
        pd.DataFrame: DataFrame contenant les informations des films les plus similaires au film sélectionné.
    """

    # Défintion du model
    KNNmodel = NearestNeighbors(n_neighbors= 6, algorithm= "auto")

    # Combinaison du preprocessing et du model
    pipeline_with_knn = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('knn', KNNmodel)
    ])

    # entarinement du model
    pipeline_with_knn.fit(df)

    #regarder la taille en mémoiredu preprocessor
    # x = pipeline_with_knn.named_steps['preprocessor'].transform(df)
    # print(sys.getsizeof(x))




    # fonction trouver plus proche voisin
    def nearsest_neighbor(df:pd.DataFrame, tconst_titre:str, pipeline: Pipeline)->pd.DataFrame:
        """
        Trouve les films les plus similaires au film sélectionné à l'aide du modèle KNN.

        Args:
            df (pd.DataFrame): Le DataFrame contenant les données des films.
            tconst_titre (str): Le tconst du film sélectionné.
            pipeline (Pipeline): Le pipeline contenant le préprocesseur et le modèle KNN.

        Returns:
            pd.DataFrame: DataFrame contenant les informations des films les plus similaires au film sélectionné.
        """
        #recuperation des information du film selectionné
        query_film_features = df[df['tconst'] == tconst_titre].drop(columns=['tconst', 'title'], axis=1)

        # infos transformé sur le film selectionné
        query_film_features_processed = pipeline.named_steps['preprocessor'].transform(query_film_features)

        # utilisation du model knn plus proche voisin du film -> recup des indiczes des films
        id_film_knn = pipeline.named_steps['knn'].kneighbors(query_film_features_processed, return_distance= False)

        # recuperation des infos par rapprot au id trouvés par le model knn
        df_plus_proche_voisin = df.iloc[id_film_knn[0]]

        return df_plus_proche_voisin


    # recommandation du film selectionné
    plus_proche_voisin_df = nearsest_neighbor(df, tconst_titre, pipeline_with_knn)

    return plus_proche_voisin_df.reset_index()



def ML_reco(df_film:pd.DataFrame, options_genre_film:list[str], start_year:int, end_year:int)->pd.DataFrame:
    """
    Effectue une recommandation de films en utilisant un modèle de recommandation basé sur le voisinage le plus proche (KNN).

    Args:
        df_film (pd.DataFrame): Le DataFrame contenant les données des films.
        options_genre_film (list): La liste des genres sélectionnés.
        start_year (int): L'année de début de la plage de dates sélectionnée.
        end_year (int): L'année de fin de la plage de dates sélectionnée.

    Returns:
        pd.DataFrame: DataFrame contenant les informations des films recommandés.
    """

    # génération dataframe suite aux différents filtres
    df_movies_filtered = prepa_data_filtered(df_film, st.session_state['tconst'], options_genre_film, [start_year, end_year])

    # récupération des filtres pour ML
    features_std, features_log_and_std, features_cat_list = fetch_feautures_reco()

    # Génération du preprocessing
    preprocessor = preprocessor_SLB(features_std, features_log_and_std, features_cat_list)
    
    # insertion du module de proche voisin --> dataframe resultat avec les 5 recomandations
    df_result = model_knn_module(df_movies_filtered, st.session_state['tconst'], preprocessor)

    return df_result