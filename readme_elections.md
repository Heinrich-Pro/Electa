# 🗳️ Système de Gestion des Résultats Électoraux

Application Django complète pour le calcul et l'affichage en temps réel des résultats d'élections locales.

![Django](https://img.shields.io/badge/Django-4.2+-green.svg)
![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 📋 Table des Matières

- [Fonctionnalités](#-fonctionnalités)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Utilisation](#-utilisation)
- [Structure du Projet](#-structure-du-projet)
- [API Admin](#-api-admin)
- [Captures d'écran](#-captures-décran)
- [Technologies](#-technologies)
- [Contribution](#-contribution)
- [Licence](#-licence)

## ✨ Fonctionnalités

### 🎯 Gestion des Données
- ✅ Gestion des candidats (nom, prénom, parti, numéro)
- ✅ Organisation hiérarchique : Centres → Bureaux de vote
- ✅ Saisie des résultats par bureau
- ✅ Calculs automatiques en temps réel

### 📊 Affichage des Résultats
- ✅ **Résultats globaux** : Vue d'ensemble avec classement des candidats
- ✅ **Résultats par centre** : Détails pour chaque centre de vote
- ✅ **Résultats par bureau** : Vue complète de tous les bureaux
- ✅ **Détails d'un bureau** : Résultats spécifiques d'un bureau

### 🔢 Calculs Automatiques
- ✅ Total des voix par candidat
- ✅ Pourcentages globaux et par bureau
- ✅ Taux de participation
- ✅ Classement automatique
- ✅ Identification du gagnant par bureau

### 🎨 Interface Utilisateur
- ✅ Design moderne et responsive
- ✅ Barres de progression animées
- ✅ Code couleur pour les classements (🥇🥈🥉)
- ✅ Barre de recherche en temps réel
- ✅ Navigation intuitive

### ⚙️ Administration
- ✅ Interface admin Django personnalisée
- ✅ Édition inline (modification rapide dans les listes)
- ✅ Boutons de modification visibles
- ✅ Statistiques en temps réel
- ✅ Saisie groupée des résultats

## 🏗️ Architecture

```
┌─────────────────────────────────────────┐
│           Interface Publique            │
│  (Consultation des résultats)           │
├─────────────────────────────────────────┤
│  - Résultats globaux                    │
│  - Résultats par centre                 │
│  - Résultats par bureau                 │
│  - Détails bureau spécifique            │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│         Django Backend (MVT)            │
├─────────────────────────────────────────┤
│  Models:                                │
│    - Candidat                           │
│    - CentreVote                         │
│    - BureauVote                         │
│    - Resultat                           │
├─────────────────────────────────────────┤
│  Views:                                 │
│    - resultats_globaux()                │
│    - resultats_par_centre()             │
│    - resultats_par_bureau()             │
│    - detail_bureau()                    │
├─────────────────────────────────────────┤
│  Templates:                             │
│    - base.html                          │
│    - resultats_globaux.html             │
│    - resultats_par_centre.html          │
│    - resultats_par_bureau.html          │
│    - detail_bureau.html                 │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│        Interface Admin Django           │
│     (Saisie des données)                │
├─────────────────────────────────────────┤
│  - Gestion des candidats                │
│  - Gestion des centres                  │
│  - Gestion des bureaux                  │
│  - Saisie des résultats                 │
└─────────────────────────────────────────┘
                    ↕
┌─────────────────────────────────────────┐
│          Base de Données SQLite         │
└─────────────────────────────────────────┘
```

## 🚀 Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)
- virtualenv (recommandé)

### Étape 1 : Cloner le projet

```bash
git clone https://github.com/votre-username/election-system.git
cd election-system
```

### Étape 2 : Créer un environnement virtuel

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### Étape 3 : Installer les dépendances

```bash
pip install django pillow
```

### Étape 4 : Créer le projet Django

```bash
# Créer le projet principal
django-admin startproject election_project
cd election_project

# Créer l'application
python manage.py startapp elections
```

### Étape 5 : Configuration

Modifiez `election_project/settings.py` :

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'elections',  # ← Ajouter cette ligne
]

# Configuration des médias (pour les photos des candidats)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Langue et fuseau horaire
LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Africa/Libreville'  # Ajustez selon votre région
```

### Étape 6 : Copier les fichiers

Copiez tous les fichiers fournis dans l'artifact dans leurs emplacements respectifs :

- `models.py` → `elections/models.py`
- `views.py` → `elections/views.py`
- `admin.py` → `elections/admin.py`
- `urls.py` (elections) → `elections/urls.py`
- `urls.py` (principal) → `election_project/urls.py`
- Templates → `elections/templates/elections/`

### Étape 7 : Créer la base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

### Étape 8 : Créer un superutilisateur

```bash
python manage.py createsuperuser
# Suivez les instructions pour définir username, email et password
```

### Étape 9 : Lancer le serveur

```bash
python manage.py runserver
```

🎉 **L'application est maintenant accessible !**

## 🔧 Configuration

### Structure des dossiers

```
election_project/
├── election_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── elections/
│   ├── migrations/
│   ├── templates/
│   │   └── elections/
│   │       ├── base.html
│   │       ├── resultats_globaux.html
│   │       ├── resultats_par_centre.html
│   │       ├── resultats_par_bureau.html
│   │       └── detail_bureau.html
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── media/
│   └── candidats/
├── manage.py
└── db.sqlite3
```

## 📖 Utilisation

### 1. Accéder à l'administration

**URL** : `http://localhost:8000/admin/`

Connectez-vous avec vos identifiants de superutilisateur.

### 2. Saisir les données

#### Étape A : Ajouter les candidats

1. Allez dans **Elections → Candidats**
2. Cliquez sur **Ajouter candidat**
3. Remplissez :
   - Numéro du candidat
   - Nom et prénom
   - Parti politique
   - Photo (optionnel)
4. Cliquez sur **Enregistrer**

#### Étape B : Créer les centres de vote

1. Allez dans **Elections → Centres de vote**
2. Cliquez sur **Ajouter centre de vote**
3. Remplissez :
   - Nom du centre
   - Adresse
   - Commune
4. Cliquez sur **Enregistrer**

#### Étape C : Ajouter les bureaux de vote

**Méthode 1** : Depuis un centre
1. Ouvrez un centre de vote existant
2. Dans la section "Bureaux", ajoutez les bureaux inline
3. Pour chaque bureau : numéro + nombre d'inscrits
4. Enregistrez

**Méthode 2** : Directement
1. Allez dans **Elections → Bureaux de vote**
2. Ajoutez chaque bureau individuellement

#### Étape D : Saisir les résultats

**Méthode recommandée** : Saisie par bureau
1. Allez dans **Elections → Bureaux de vote**
2. Cliquez sur **✏️ Modifier** du bureau concerné
3. Dans la section **Resultats** en bas :
   - Sélectionnez le candidat
   - Entrez le nombre de voix
   - Cliquez sur le **+** pour ajouter le candidat suivant
4. Enregistrez → Les calculs se font automatiquement !

**Méthode alternative** : Modification rapide
1. Allez dans **Elections → Résultats**
2. Modifiez directement les voix dans la liste
3. Cliquez sur **Enregistrer** en bas

### 3. Consulter les résultats

#### Résultats Globaux
**URL** : `http://localhost:8000/`

Affiche :
- Total des inscrits, votants et taux de participation
- Classement complet des candidats
- Pourcentages et barres de progression

#### Résultats par Centre
**URL** : `http://localhost:8000/centres/`

Affiche :
- Résultats détaillés pour chaque centre
- Classement des candidats dans chaque centre
- Liste des bureaux par centre

#### Résultats par Bureau
**URL** : `http://localhost:8000/bureaux/`

Affiche :
- Tous les bureaux avec leurs résultats
- Gagnant identifié pour chaque bureau
- Barre de recherche pour filtrer
- Statistiques (inscrits, votants, participation)

#### Détails d'un Bureau
**URL** : `http://localhost:8000/bureau/<id>/`

Affiche :
- Résultats complets d'un bureau spécifique
- Classement des candidats
- Statistiques du bureau

## 📁 Structure du Projet

### Models (Modèles de données)

```python
Candidat
├── numero (unique)
├── nom
├── prenom
├── parti
├── photo
└── Méthodes:
    ├── total_voix()
    └── pourcentage_global()

CentreVote
├── nom
├── adresse
├── commune
└── Méthodes:
    ├── total_voix()
    └── total_inscrits()

BureauVote
├── centre (ForeignKey)
├── numero
├── nombre_inscrits
└── Méthodes:
    ├── total_voix()
    └── taux_participation()

Resultat
├── candidat (ForeignKey)
├── bureau_vote (ForeignKey)
├── nombre_voix
└── Méthodes:
    └── pourcentage_bureau()
```

### Relations

```
CentreVote (1) ←→ (N) BureauVote
Candidat (1) ←→ (N) Resultat
BureauVote (1) ←→ (N) Resultat
```

## ⚙️ API Admin

### Fonctionnalités Admin Personnalisées

#### Édition Inline
- **Candidats** : Nom, prénom, parti modifiables directement
- **Centres** : Commune modifiable directement
- **Bureaux** : Nombre d'inscrits modifiable directement
- **Résultats** : Nombre de voix modifiable directement

#### Saisie Groupée
- Ajouter tous les bureaux d'un centre en une fois
- Saisir tous les résultats d'un bureau en une fois

#### Statistiques en Temps Réel
- Total des voix affiché automatiquement
- Pourcentages calculés à la volée
- Taux de participation mis à jour

#### Boutons d'Action
- Bouton "✏️ Modifier" sur chaque ligne
- Accès rapide aux détails

## 🖼️ Captures d'écran

### Page d'accueil - Résultats Globaux
```
┌──────────────────────────────────────────┐
│  🗳️ RÉSULTATS DES ÉLECTIONS              │
├──────────────────────────────────────────┤
│  📊 Résultats Globaux                    │
│                                          │
│  ┌────────┐ ┌────────┐ ┌────────┐      │
│  │12,500  │ │ 9,800  │ │ 78.4%  │      │
│  │Inscrits│ │Votants │ │  Part. │      │
│  └────────┘ └────────┘ └────────┘      │
│                                          │
│  🥇 Jean Dupont - 4,250 voix (43.4%)    │
│  ▓▓▓▓▓▓▓▓▓▓▓▓▓░░░░░░░ 43.4%            │
│                                          │
│  🥈 Marie Martin - 3,100 voix (31.6%)   │
│  ▓▓▓▓▓▓▓▓▓░░░░░░░░░░░ 31.6%            │
└──────────────────────────────────────────┘
```

### Interface Admin
```
┌──────────────────────────────────────────┐
│  🗳️ Administration des Élections         │
├──────────────────────────────────────────┤
│  Candidats                               │
│  ├─ 1. Jean Dupont (Parti A) ✏️         │
│  ├─ 2. Marie Martin (Parti B) ✏️        │
│  └─ 3. Paul Durand (Parti C) ✏️         │
│                                          │
│  Centres de vote                         │
│  ├─ Centre Municipal Nord ✏️             │
│  │   └─ 5 bureaux                       │
│  └─ École Primaire Sud ✏️               │
│      └─ 3 bureaux                       │
└──────────────────────────────────────────┘
```

## 🛠️ Technologies

- **Backend** : Django 4.2+
- **Base de données** : SQLite (par défaut)
- **Frontend** : HTML5, CSS3, JavaScript vanilla
- **Icons** : Emojis Unicode
- **Responsive** : CSS Grid & Flexbox

## 📊 Exemple de Données de Test

```python
# Candidats
Candidat 1: Jean Dupont - Parti Démocratique
Candidat 2: Marie Martin - Parti Républicain
Candidat 3: Paul Durand - Parti Socialiste

# Centres
Centre Municipal Nord - Libreville
École Primaire Sud - Owendo

# Bureaux
Bureau 001 - Centre Municipal Nord (500 inscrits)
Bureau 002 - Centre Municipal Nord (450 inscrits)
Bureau 003 - École Primaire Sud (380 inscrits)

# Résultats Bureau 001
Jean Dupont: 210 voix
Marie Martin: 180 voix
Paul Durand: 90 voix
```

## 🔐 Sécurité

### Recommandations pour la Production

```python
# settings.py - À modifier en production

# 1. Debug mode
DEBUG = False  # ← Mettre à False

# 2. Secret key
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')  # ← Utiliser variable d'environnement

# 3. Allowed hosts
ALLOWED_HOSTS = ['votre-domaine.com', 'www.votre-domaine.com']

# 4. Base de données
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # PostgreSQL en production
        'NAME': 'election_db',
        'USER': 'election_user',
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# 5. Sécurité HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## 🚀 Déploiement

### Sur un serveur Linux (Ubuntu/Debian)

```bash
# 1. Installer les dépendances
sudo apt update
sudo apt install python3-pip python3-venv nginx

# 2. Configurer Gunicorn
pip install gunicorn
gunicorn election_project.wsgi:application --bind 0.0.0.0:8000

# 3. Configurer Nginx
sudo nano /etc/nginx/sites-available/elections

# 4. Collecter les fichiers statiques
python manage.py collectstatic

# 5. Redémarrer les services
sudo systemctl restart nginx
```

## 📝 Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.

## 👥 Contribution

Les contributions sont les bienvenues ! Pour contribuer :

1. Forkez le projet
2. Créez une branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Pushez vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 🐛 Signaler un Bug

Utilisez la section [Issues](https://github.com/votre-username/election-system/issues) pour signaler des bugs.

## 📞 Contact

Votre Nom - [@votre_twitter](https://twitter.com/votre_twitter)

Email : [heinrichtechcraft@gmail.com]()

Lien du projet : [https://github.com/votre-username/election-system](https://github.com/votre-username/election-system)

## 🙏 Remerciements

- Django Framework
- La communauté open source
- Tous les contributeurs

---

**Fait avec ❤️ pour des élections transparentes et démocratiques**