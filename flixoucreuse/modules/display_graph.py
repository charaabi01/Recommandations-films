from modules.importation import st, pd, sns, plt


def graph_film_pop(df:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 films les plus populaires à partir d'un DataFrame.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films. 
                       Doit inclure les colonnes 'tconst', 'title', et 'popularity'.

    Returns:
    None
    """
    # Trier le DataFrame par la colonne 'popularity' et obtenir les 10 premières lignes
    top_movies = df.sort_values(by='popularity', ascending=False).head(10)

    # Mapper les tconst aux titres correspondants
    title_mapping = df.set_index('tconst')['title'].to_dict()
    top_movies['original_title'] = top_movies['tconst'].map(title_mapping)
    top_movies['original_title'] = top_movies['original_title'].map(lambda x: x[:25]+'...' if len(x)>25 else x )

    # Créer un graphique à barres
    fig8 = sns.barplot(x='popularity', y='original_title', data=top_movies, hue='original_title', palette='viridis', legend=False)
    fig8.set_title("Top 10 des films les plus populaires")
    fig8.set_ylabel("")
    fig8.set_xlabel("Popularity")

    for index, value in enumerate(top_movies['popularity']):
        fig8.text(value, index, str((int(value))), ha='left', va='center')

    st.pyplot()



def graph_film_revenu(df:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 films ayant généré le plus de revenus à partir d'un DataFrame.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films. 
                       Doit inclure les colonnes 'title' et 'revenue'.

    Returns:
    None
    """
    top_10_films_revenue = df.sort_values(by='revenue', ascending=False).head(10)

    top_10_films_revenue['revenue'] = top_10_films_revenue['revenue'].apply(lambda x1: round(x1*1e-9, 2))

    top_10_films_revenue['title'] = top_10_films_revenue['title'].map(lambda x: x[:25]+'...' if len(x)>25 else x )

    # top_10_films
    # Tracez l'histogramme avec seaborn
    fig3 = sns.barplot(top_10_films_revenue, y= 'title', x= 'revenue', palette='viridis', legend=False)
    fig3.set_title("TOP 10 des films par revenu")
    fig3.set_ylabel("")
    fig3.set_xlabel("Revenus en milliard $")
    
    for index, value in enumerate(top_10_films_revenue['revenue']):
        fig3.text(value, index, str(value)+' m$', ha='left', va='center')

    st.pyplot()

    


def graph_film_note(df:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 films les mieux notés parmi ceux ayant un nombre de votes élevé.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films. 
                       Doit inclure les colonnes 'title', 'numVotes', et 'averageRating'.

    Returns:
    None
    """

    df_vote_desc = df.sort_values(by='numVotes', ascending=False)

    decile_nb_vote = df['numVotes'].quantile(0.2)

    tri_film_note = df[df['numVotes']>= decile_nb_vote]

    top_10_films_note = tri_film_note.sort_values(by='averageRating', ascending=False).head(10)

    
    top_10_films_note['title'] = top_10_films_note['title'].map(lambda x: x[:25]+'...' if len(x)>25 else x )


    # top_10_films
    # Tracez l'histogramme avec seaborn
    fig2 = sns.barplot(top_10_films_note, y= 'title', x= 'averageRating', palette='viridis', legend=False)
    fig2.set_title("TOP 10 des films par note")
    fig2.set_ylabel("")
    fig2.set_xlabel("Note sur 10")
    fig2.set_xlim(0,10)

    for index, value in enumerate(top_10_films_note['averageRating']):
        fig2.text(value, index, str(value), ha='left', va='center')

    st.pyplot()



def graph_acteurs(df_film:pd.DataFrame, df_name:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 acteurs/actrices les plus fréquents dans les films d'un DataFrame.

    Parameters:
    df_film (pd.DataFrame): Le DataFrame contenant les données des films. 
                            Doit inclure les colonnes 'actor' et 'actress'.
    df_name (pd.DataFrame): Le DataFrame contenant les données des noms des acteurs/actrices. 
                            Doit inclure les colonnes 'nconst' et 'primaryName'.

    Returns:
    None
    """

    # Calculer les valeurs uniques combinées des colonnes 'actor' et 'actress'
    unique_actors_actress = df_film['actor'].dropna().explode()

        # Obtenir les 10 valeurs les plus fréquentes
    top_actors_actresses = unique_actors_actress.value_counts().head(10)

        # Extraire les valeurs uniques de 'nconst' et 'primaryName' de BDD_clean_avant_ML_name
    nconst_primaryName_mapping = df_name[['nconst', 'primaryName']].set_index('nconst')['primaryName'].to_dict()

        # Remplacer les 'nconst' par 'primaryName'
    top_actors_actresses_names = top_actors_actresses.rename(index=nconst_primaryName_mapping).reset_index()
    top_actors_actresses_names.columns = ["Acteur", "Nombre d'occurrences"]

        # Créer un dégradé de couleur
    colors = sns.color_palette("viridis", len(top_actors_actresses_names))

        # Créer un graphique à barres
    bars = sns.barplot(top_actors_actresses_names, x= "Acteur", y="Nombre d'occurrences", palette='viridis')
    bars.set_title("TOP 10 des acteurs les plus présent")
    bars.set_ylabel("Occurence d'apparition par film")
    bars.set_xlabel(None)
    bars.set_xticklabels(bars.get_xticklabels(), rotation=45, horizontalalignment='right')

    st.pyplot()



def graph_actrices(df_film:pd.DataFrame, df_name:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 actrices les plus fréquentes dans les films d'un DataFrame.

    Parameters:
    df_film (pd.DataFrame): Le DataFrame contenant les données des films.
                            Doit inclure la colonne 'actress'.
    df_name (pd.DataFrame): Le DataFrame contenant les données des noms des actrices.
                            Doit inclure les colonnes 'nconst' et 'primaryName'.

    Returns:
    None
    """

    # Filtrer les valeurs indésirables
    filtered_actors_actress = df_film['actress'].dropna().explode()

    # Obtenir les 10 valeurs les plus fréquentes
    top_actors_actresses = filtered_actors_actress.value_counts().head(10)

    # Extraire les valeurs uniques de 'nconst' et 'primaryName' de BDD_clean_avant_ML_name
    nconst_primaryName_mapping = df_name[['nconst', 'primaryName']].set_index('nconst')['primaryName'].to_dict()

    # Remplacer les 'nconst' par 'primaryName'
    top_actors_actresses_names = top_actors_actresses.rename(index=nconst_primaryName_mapping).reset_index()
    top_actors_actresses_names.columns = ['Actrice', "Nombre d'occurrences"]

    # Créer un dégradé de couleur
    colors = sns.color_palette("viridis", len(top_actors_actresses_names))

    # Créer un graphique à barres
    bars2 = sns.barplot(top_actors_actresses_names, x= "Actrice", y="Nombre d'occurrences", palette='viridis')
    bars2.set_title("TOP 10 des actrices les plus présentes")
    bars2.set_ylabel("Occurence d'apparition par film")
    bars2.set_xlabel(None)
    bars2.set_xticklabels(bars2.get_xticklabels(), rotation=45, horizontalalignment='right')
    
    st.pyplot()




def graph_societeProd(df:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 sociétés de production ayant produit le plus de films.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films.
                       Doit inclure la colonne 'production_companies_name'.

    Returns:
    None
    """

    production_companies_series = df['production_companies_name'].explode()
    production_companies_counts = production_companies_series.value_counts()

    top_production_companies_df = pd.DataFrame({'Société de production': production_companies_counts.index,
                                                'Nombre de films': production_companies_counts.values})

    top_production_companies_df = top_production_companies_df.head(10)

    fig11 = sns.barplot(top_production_companies_df, x='Société de production', y='Nombre de films', palette='viridis')
    fig11.set_title("TOP 10 des sociétés de production")
    fig11.set_ylabel("Occurence")
    fig11.set_xlabel(None)
    fig11.set_xticklabels(fig11.get_xticklabels(), rotation=45, horizontalalignment='right')

    st.pyplot()
    



def graph_real(df_film:pd.DataFrame, df_name:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 réalisateurs les plus fréquents dans les films d'un DataFrame.

    Parameters:
    df_film (pd.DataFrame): Le DataFrame contenant les données des films.
                            Doit inclure la colonne 'directors'.
    df_name (pd.DataFrame): Le DataFrame contenant les données des noms des réalisateurs.
                            Doit inclure les colonnes 'nconst' et 'primaryName'.

    Returns:
    None
    """

    # Filtrer les valeurs indésirables
    filtered_director = df_film['directors'].dropna().explode()

    # Obtenir les 10 valeurs les plus fréquentes
    top_director = filtered_director.value_counts().head(10)

    # Extraire les valeurs uniques de 'nconst' et 'primaryName' de BDD_clean_avant_ML_name
    nconst_primaryName_mapping = df_name[['nconst', 'primaryName']].set_index('nconst')['primaryName'].to_dict()

    # Remplacer les 'nconst' par 'primaryName'
    top_director_names = top_director.rename(index=nconst_primaryName_mapping).reset_index()
    top_director_names.columns = ['Réalisateur', "Nombre d'occurrences"]

    # Créer un dégradé de couleur
    colors = sns.color_palette("viridis", len(top_director_names))

    # Créer un graphique à barres
    plt.figure(figsize=(10, 6))
    fig7 = sns.barplot(top_director_names, x='Réalisateur', y= "Nombre d'occurrences", palette='viridis')
    fig7.set_title("TOP 10 des réalisateurs les plus présent")
    fig7.set_ylabel("Occurence")
    fig7.set_xlabel(None)
    fig7.set_xticklabels(fig7.get_xticklabels(), rotation=45, horizontalalignment='right')

    st.pyplot()




def graph_film_genres(df:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 genres de films les plus fréquents dans un DataFrame.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films.
                       Doit inclure la colonne 'genres'.

    Returns:
    None
    """

    genres_series = df['genres'].explode()

    genre_counts = genres_series.value_counts()

    top_genres_df = pd.DataFrame({'Genre': genre_counts.index, 'Nombre de films': genre_counts.values})

    top_genres_df = top_genres_df.head(10)

    fig10 = sns.barplot(top_genres_df, x='Genre', y='Nombre de films', palette='viridis')
    fig10.set_title("TOP 10 des genres de films")
    fig10.set_ylabel("Occurence")
    fig10.set_xlabel(None)
    fig10.set_xticklabels(fig10.get_xticklabels(), rotation=45, horizontalalignment='right')

    st.pyplot()



def graph_paysProd(df:pd.DataFrame)->None:
    """
    Affiche un graphique à barres des 10 pays de production les plus fréquents dans un DataFrame.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films.
                       Doit inclure la colonne 'production_countries'.

    Returns:
    None
    """
    countries_series = df['production_countries'].explode()
    top_countries = countries_series.value_counts().head(10)

    top_countries_df = top_countries.reset_index()
    top_countries_df.columns = ['Pays', 'Nombre de films']

    fig9 = sns.barplot(top_countries_df, x='Pays', y='Nombre de films', palette='viridis')
    fig9.set_title("TOP 10 des pays de production")
    fig9.set_ylabel("Occurence")
    fig9.set_xlabel(None)
    fig9.set_xticklabels(fig9.get_xticklabels(), rotation=45, horizontalalignment='right')

    st.pyplot()

   



def graph_duree_film(df:pd.DataFrame)->None:
    """
    Affiche un histogramme de la distribution de la durée des films dans un DataFrame.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films.
                       Doit inclure la colonne 'runtime'.

    Returns:
    None
    """

    fig1 = sns.histplot(df, x= 'runtime', bins=10, kde=True)

    fig1.set_title('Distribution de la durée des films')
    fig1.set_xlabel('Durée en minutes')
    fig1.set_ylabel('Fréquence')


    st.pyplot()



def graph_note_moyenne(df:pd.DataFrame)->None:
    """
    Affiche un histogramme de la distribution des notes moyennes dans un DataFrame.

    Parameters:
    df (pd.DataFrame): Le DataFrame contenant les données des films.
                       Doit inclure la colonne 'averageRating'.

    Returns:
    None
    """

    filtered_ratings = df['averageRating'].dropna()

    # Créer un graphique de distribution
    fig6 = sns.histplot(filtered_ratings, kde=True, bins=30)

    # Ajouter des titres et des labels
    fig6.set_title('Distribution des notes moyennes')
    fig6.set_xlabel('Note moyenne')
    fig6.set_ylabel('Fréquence')

    st.pyplot()



