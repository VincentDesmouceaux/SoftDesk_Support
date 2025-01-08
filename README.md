# 🚀 SoftDesk Support - Guide de démarrage

Bienvenue dans le projet **SoftDesk Support** ! Ce dépôt contient une API Django REST permettant de gérer des utilisateurs, des projets, des contributeurs, des tickets (Issues) et des commentaires.

Ce **README** vous explique pas à pas comment installer et configurer l’application afin de pouvoir la lancer et la tester localement.

## 📦 Prérequis

1.  **Python 3.9+** (ou version supérieure)
2.  **Pipenv** (si vous ne l’avez pas déjà, installez-le avec `pip install --user pipenv`)
3.  **Git** (pour cloner le dépôt)

## ⏬ Installation du projet

### 1) Récupérer le dépôt


git clone https://github.com/VincentDesmouceaux/SoftDesk_Support.git

cd SoftDesk\_Support


### 2) Créer et activer l’environnement virtuel avec Pipenv

pipenv install --dev

pipenv shell

-   `**pipenv install --dev**` va installer toutes les dépendances (de production et de développement) décrites dans le fichier `Pipfile`.

-   `**pipenv shell**` active l’environnement virtuel pour votre session terminal actuelle.


### 3) Configurer vos variables d’environnement

Créez (ou éditez) un fichier `.env` à la racine du projet pour y placer vos clés secrètes. Par exemple :

SECRET\_KEY="votre\_cle\_secrete\_django"
DEBUG=True

_(Vous pouvez définir_ `_DEBUG=False_` _en production.)_

### 4) Effectuer les migrations

python manage.py migrate

Ceci va créer les tables nécessaires dans la base de données (SQLite par défaut).

### 5) (Optionnel) Créer un super-utilisateur Django


python manage.py createsuperuser

Cela vous permettra d’accéder à l’interface d’administration Django avec votre identifiant et mot de passe.

### 6) Lancer le serveur de développement


python manage.py runserver

Vous pouvez maintenant accéder à l’API en ouvrant un navigateur à l’adresse suivante :

http://127.0.0.1:8000/api/

## 📖 Documentation & Routes

### Documentation Swagger

Vous pouvez consulter la documentation interactive (Swagger) à l’URL suivante :

http://127.0.0.1:8000/api/docs/

Toutes les routes y sont décrites et vous pouvez même tester les requêtes directement dans cette interface.

### Fichier d’export Postman

Si vous désirez importer les routes et requêtes prédéfinies dans **Postman**, vous pouvez :

1.  Récupérer le fichier `.json` (collection Postman exportée) fourni dans le dépôt.

2.  Dans Postman, cliquez sur **Import** et sélectionnez le fichier `.json`.

3.  Vous aurez ainsi toutes les requêtes configurées (URL, headers, etc.) prêtes à être utilisées.

_(Si le fichier d’export Postman n’est pas présent, vous pouvez tout de même créer vos propres requêtes Postman en vous aidant des routes exposées par la documentation Swagger.)_

## 💡 Fonctionnalités principales

-   **Authentification JWT** :

-   Pour récupérer un token, envoyez une requête POST à `/api/token/` avec vos identifiants (username/password).
-   Exemple de body :

json

{
  "username": "votre\_username",
  "password": "votre\_mot\_de\_passe"
}

-   Le token obtenu est à inclure dans le header de vos futures requêtes :
-   `Authorization: Bearer <votre_token_jwt>`
-   **Gestion des projets** (CRUD)
-   **Gestion des contributeurs** (ajout, suppression, rôles)
-   **Gestion des tickets (issues)** (CRUD)
-   **Gestion des commentaires** (CRUD)

## 🎉 Conclusion

Vous êtes désormais prêt à utiliser l’API **SoftDesk Support** !

N’hésitez pas à nous contacter en cas de question ou à ouvrir des **issues** sur le dépôt GitHub pour signaler des problèmes ou proposer des améliorations.

**Bon développement !** 💻✨