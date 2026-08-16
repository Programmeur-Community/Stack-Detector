# Stack Detector

Stack Detector est une application web permettant de détecter les technologies utilisées par un site web, comme les frameworks frontend/backend, les CMS, les services d'infrastructure et les outils analytiques.

L'application analyse les éléments visibles sur une page web, tels que les en-têtes HTTP, les cookies, les balises meta, les scripts (balises script), les liens (balises link), les classes HTML et les attributs, puis affiche les technologies identifiées dans un tableau de résultats.

## Fonctionnalités

- Détection des stacks frontend et backend
- Identification des frameworks tels que Next.js, Vue, Angular, Express.js, Bootstrap, Tailwind, etc.
- Détection des CMS comme WordPress
- Analyse de l'infrastructure et des services tiers
- Historique des recherches récentes

## Stack technique

- Python 3
- Flask
- httpx
- beautifulsoup4
- Tailwind CSS

## Prérequis

Avant de lancer le projet, assurez-vous d'avoir installé :

- Python 3.9 ou plus
- pip
- Git

## Installation

1. Clonez le dépôt :

```bash
git clone https://github.com/programmeur-community/stack-detector.git
cd stack-detector
```

2. Créez un environnement virtuel :

```bash
python -m venv venv
```

3. Activez l'environnement virtuel :

- Sur Windows :

```bash
./venv/Scripts/activate
```

- Sur macOS/Linux :

```bash
source venv/bin/activate
```

4. Installez les dépendances :

```bash
pip install -r requirements.txt
```

5. Créer un fichier `.env` à la racine du projet avec la valeur suivante :

```txt
FLASK_SECRET_KEY=votre_cle_secrete_ici
```

6. Lancez l'application :

```bash
python app.py
```

7. Ouvrez votre navigateur et accédez à :

```text
http://127.0.0.1:5000/
```

## Utilisation

1. Saisissez l'URL d'un site web dans le formulaire.
2. Cliquez sur le bouton d'analyse.
3. La plateforme détecte automatiquement les technologies utilisées.

## Structure du projet

```text
Stack-Detector/
├── app.py
├── detector.py
├── routes.py
├── utils.py
├── requirements.txt
├── signatures.json
├── static/
│   ├── scripts.js
│   └── styles.css
├── templates/
│   ├── _footer.html
│   ├── _header.html
│   ├── _history.html
│   ├── index.html
│   └── result.html
└── README.md
```

## Auteur

Développé par [Programmeur](https://www.programmeur-community.com/).

## Licence

Ce projet est sous licence MIT.
