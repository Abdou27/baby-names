| Université Paris-Saclay |
| --- |
|
# Nom des bébés dans les Etats-Unis de 1880 à 2015

Module : Visualisation de données

Auteur : Abderrahim Benmelouka


# Table des matières

[1. Introduction](#_Toc121173419)

[2. Données brutes](#_Toc121173420)

[3. Transformation des données](#_Toc121173421)

[3.1. Jeu de données « Total Births »](#_Toc121173425)

[3.2. Jeu de données « Unique Names »](#_Toc121173426)

[3.3. Jeu de données « Name Records »](#_Toc121173427)

[3.4. Jeu de données « Unisex Names »](#_Toc121173428)

[4. Tableau de bord](#_Toc121173429)

[4.1. Total Births](#_Toc121173431)

[4.2. Unique Names](#_Toc121173432)

[4.3. Most Popular Names](#_Toc121173433)

[4.4. Unisex Names](#_Toc121173434)

[4.5. Name Analysis](#_Toc121173435)

[4.6. Name Ranking](#_Toc121173436)

[5. Conclusion](#_Toc121173437)

# 1.Introduction

Ce projet consiste à prendre un ensemble de données et à en tirer un aperçu à travers différentes visualisations. Il se décompose en deux grandes parties : pré-traiter les données brutes et développer le tableau de bord de visualisation.

Le tableau de bord a été créé à l'aide de Dash, un framework qui permet de créer des applications de données en Python pur (pas de JavaScript requis). Dash utilise Plotly sous le capot pour dessiner ses graphiques. Plus précisément, j'ai utilisé Plotly Express car il simplifie énormément le processus de création de figures.

Le code source de l'ensemble du projet se trouve sur [mon repo GitHub](https://github.com/Abdou27/baby-names). Pour lancer le serveur, clonez le repo dans un dossier local puis exécutez la commande ```python main.py```.

# 2.Données brutes

Le jeu de données utilisé s'appelle babyNamesUSYOB-full, il comporte 4 colonnes et 1858689 lignes. Ci-dessous les 5 premières lignes et 5 dernières lignes :

| **YearOfBirth** | **Name** | **Sex** | **Number** |
| --- | --- | --- | --- |
| **1880** | Mary | F | 7065 |
| **1880** | Anna | F | 2604 |
| **1880** | Emma | F | 2003 |
| **1880** | Elizabeth | F | 1939 |
| **1880** | Minnie | F | 1746 |
| … | … | … | … |
| **2015** | Zykell | M | 5 |
| **2015** | Zyking | M | 5 |
| **2015** | Zykir | M | 5 |
| **2015** | Zyrus | M | 5 |
| **2015** | Zyus | M | 5 |

# 3.Transformation des données

À l'aide du notebook dashboard.ipynb trouvé dans le dossier notebooks. Quatre nouveaux jeux de données ont été extraits en ajoutant des colonnes calculées et en agrégeant, filtrant et triant les données.

## 3.1. Jeu de données « Total Births »

Cet ensemble de données décrit le nombre de naissances masculines, féminines et totales chaque année, il a été créé en regroupant les données d'origine par YearOfBirth et Sex, puis en additionnant le nombre de naissances pour chaque groupe.

Avec ce DataFrame résultant, nous regroupons par YearOfBirth et ajoutons une troisième ligne qui additionne les naissances masculines et féminines pour chaque groupe, cette ligne représente le total des naissances par an sans distinction de sexe.

Ensuite, les résultats sont enregistrés dans data/total\_births.csv.

## 3.2. Jeu de données « Unique Names »

Cet ensemble de données décrit le nombre de noms uniques masculins, féminins et totaux chaque année, il a été créé en regroupant les données d'origine par YearOfBirth et Sex, puis en comptant le nombre de nombre de noms différents pour chaque groupe.

Pour calculer le nombre de prénoms uniques par an quel que soit le sexe, une simple addition des lignes masculines et féminines serait une erreur car il faudrait tenir compte des prénoms unisexes. Par conséquent, pour y parvenir, les colonnes Sex et Number ont été supprimées, puis les lignes en double ont été supprimées dans le DataFrame résultant, cela élimine les doublons dans les noms unisexes, après cela, le résultat est regroupé par année, puis le nombre de noms différents par an est compté.

Il ne reste plus qu'à ajouter les deux DataFrames et à renommer le colonne Name en Count.

Ensuite, les résultats sont enregistrés dans data/unique\_names.csv.

## 3.3. Jeu de données « Name Records »

Ce jeu de données est une version augmentée des données d'origine, il ajoute trois nouvelles colonnes calculées.

La première colonne est la proportion d'utilisation de chaque nom par an et par sexe. Cela a été calculée en regroupant par année et par sexe, puis en divisant chaque nombre par la somme des nombres des groupes résultants.

La deuxième colonne est la longueur du nom, cela a été facilement calculé en appliquant la fonction len de Python à chaque ligne du DataFrame.

La troisième colonne décrit la décennie à laquelle appartient l'année, cela a également été facilement calculé en divisant l'année de chaque ligne par 10, puis en prenant la partie entière de ce résultat et en la multipliant par 10.

Ce DataFrame est ensuite enregistré dans data/name\_records.csv.

## 3.4. Jeu de données « Unisex Names »

Ce jeu de données est un classement décroissant de tous les prénoms unisexes, c'est-à-dire des prénoms ayant été utilisés au moins une fois pour les deux sexes.

Le classement est basé sur le nombre minimum de fois que chaque nom a été utilisé par sexe, par exemple, le nom Willie a été utilisé au total 146 134 fois pour les bébés de sexe féminin et 448 091 fois pour les bébés de sexe masculin. Par conséquent, la valeur attribuée à ce nom est 146134. Les noms sont ensuite classés par ordre décroissant en fonction des valeurs qui leur sont attribuées. Le nom Willie est le premier dans le DataFrame résultant.

Le résultat est enregistré dans data/unisex\_names.csv.

# 4.Tableau de bord

Le tableau de bord est organisé en différents onglets (avec Dash) pour faciliter l'accès et la commutation entre les différents graphiques.

## 4.1. Total Births

Ce graphique linéaire montre l'évolution du nombre de naissances au fil des ans pour chaque sexe.

## 4.2. Unique Names

Ce graphique, également un Line Chart, montre comment le nombre de noms uniques a changé au fil du temps pour chaque sexe.

## 4.3. Most Popular Names

Ce Treemap montre les noms les plus populaires qui ont jamais été choisis, il y a un curseur pour changer dynamiquement le nombre de noms à afficher.

## 4.4. Unisex Names

Cette arborescence montre les noms unisexes les plus utilisés, il y a aussi un curseur pour changer dynamiquement le nombre de noms à afficher.

## 4.5. Name Analysis

Ces deux graphiques linéaires montrent l'utilisation et la proportion (popularité) d'un nom donné. Le champ de texte est utilisé pour changer le nom pour lequel afficher les graphiques. Comme indiqué, on peut aussi sélectionner un nom en cliquant dessus dans les deux graphes Treemaps précédents.

## 4.6. Name Ranking

Ce graphique de classement montre l'évolution du classement des noms au fil des décennies. Il y a un curseur pour sélectionner le nombre de noms principaux à afficher.

Il est à noter qu'en raison de l'indisponibilité d'un graphique de classement dans Plotly, ce graphique a été créé manuellement en superposant un nuage de points et un graphique linéaire.

# 5.Conclusion

Ce projet m'a aidé à développer mes compétences d'analyse de données à travers l'étape de prétraitement et mes compétences de visualisation à travers le processus de création de tableau de bord avec Dash.