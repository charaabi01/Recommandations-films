![Flixoucreuse](https://github.com/Dim2960/flixoucreuse/blob/main/img/Flixoucreuse.png)
# Système de recommandation de film 

## Description
Bienvenue sur le dépôt GitHub de notre projet de groupe réalisé pendant notre formation en Data Analyse avec la World code School. Ce projet a été mené par Aikel, Victoria et moi dans le cadre de notre cursus, et il porte sur la création d'un système de recommandation de films.

Le projet s'est déroulé en plusieurs étapes :

* Analyse des Données : Explorer les données pour identifier les tendances et les caractéristiques des films (acteurs les plus présents, période de sortie, durée des films, âge des acteurs, etc.).
* Jointures et Nettoyage : Effectuer des jointures entre les datasets, nettoyer les données et rechercher des corrélations.
* Système de Recommandation : Utiliser des algorithmes de machine learning pour recommander des films en fonction de ceux appréciés par le spectateur.
* Affichage et Interface : Afficher les recommandations et les KPI sur une interface utilisateur, ainsi que des images de films récupérées depuis une base complémentaire de TMDB.


## Table des matières
- [Sources](#sources)
- [Livrables](#livrables)
- [Installation](#installation)
- [Equipe](#equipe)
- [Remerciements](#remerciements)
- [Technologies](#technologies)

## Sources
Les données mise en oeuvres pour ce projets ont été collecté sur [IMDB](https://www.imdb.com/) et [TMDB](https://www.themoviedb.org/)      
![imdb](img/imdb-color.svg) ([Notice](https://developer.imdb.com/non-commercial-datasets/)) :  https://datasets.imdbws.com/  
![tmdb](img/themoviedatabase-color.svg) ([Notice et API](https://developer.themoviedb.org/docs/image-basics/)) : https://drive.google.com/file/d/1VB5_gl1fnyBDzcIOXZ5vUSbCY68VZN1v/view/
    
## Livrables

* Nettoyage, exploration, visualisation des données : ouvrez les notebooks correspondants dans Jupyter ou Google Colab : [Notebook](https://github.com/Dim2960/flixoucreuse/exploration_visualisation).
* Application : ouvrez à partir de l'url suivante : [appli-streamlit](https://flixoucreuse.streamlit.app/)

## Installation
0. Prérequis d'installation
    
    ![Flixoucreuse](img/python-color.svg) Python >= 2.12
    
1. Clonez le dépôt:
    ```sh
    git clone https://github.com/Dim2960/flixoucreuse.git
    ```
2. Allez dans le répertoire du projet:
    ```sh
    cd flixoucreuse
    ```
3. Installez les dépendances:
    ```sh
    pip install -r requirements.txt
    ```
4. Ajouter la clé API tmdb pour utilisation en local:  
    ```
    Copier votre clé API tmdb dans le fichier api.txt
    ```
5. Lancer l'application en local:
    ```sh
    streamlit run index.py
    ```

## Equipe

[victoria-1989](https://github.com/victoria-1989)  
[charaabi01](https://github.com/charaabi01)  
[Dim2960](https://github.com/Dim2960)

## Remerciements

- Merci à [Romain Lejeune](https://github.com/Vaelastraszz) pour l'aide apportée durant ce projet.

## Technologies
| Languages | Librairies python | Outils |
|-----------|------------------|--------|
| ![python](img/python-color.svg) Python | ![numpy](img/numpy-color.svg) numpy | ![jupiter](img/jupyter-color.svg) Jupiter Notebook |
| ![html](img/html5-color.svg) HTML | ![pandas](img/pandas-color.svg) pandas | ![github](img/github-color.svg) Github |
| ![css](img/css3-color.svg) css | ![matplotlib](img/python-color.svg) matplotlib | ![vscode](img/visualstudiocode-color.svg) VS code |
| | ![seaborn](img/python-color.svg) seaborn | ![colab](img/googlecolab-color.svg) google colab |
| | ![scikit-learn](img/scikitlearn-color.svg) scitkit-learn | ![discord](img/discord-color.svg) Discord |
| | ![streamlit](img/streamlit-color.svg) streamlit | |
