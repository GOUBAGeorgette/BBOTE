🟢 README.md — ORAFLEX Chatbot Bancaire
# ORAFLEX – Chatbot de Support Client Bancaire  
Projet Tutoré – Licence 3 Génie Logiciel – Analyse de Données  
Par : **GOUBA Georgette**


## 🎯 Présentation du Projet

ORAFLEX est un chatbot bancaire intelligent développé dans le cadre du Projet Tutoré.  
Il utilise le NLP (SpaCy) et un backend Flask pour comprendre les requêtes des utilisateurs et répondre automatiquement aux questions liées aux services bancaires.

Ce projet simule les services de la banque **ORABANK** du Burkina Faso.


## 🧠 Fonctionnalités Principales

- 🔍 Compréhension du langage naturel (NLP – SpaCy)
- 🏦 Consultation du solde
- 💸 Virement bancaire
- 💰 Dépôt d’argent
- 📜 Historique des transactions
- 📍 Localisation des agences
- 🆘 Support & Aide
- 🔐 OTP, cartes bancaires et blocage
- 💾 Sauvegarde des interactions en base PostgreSQL
- 💬 Interface web de chatbot (HTML/CSS + Flask)

## 🏗️ Architecture du Projet



Frontend (HTML/CSS)
↓
Backend Flask (Python)
↓
Modèle NLP SpaCy (TextCat)
↓
Base de données PostgreSQL


## 📦 Technologies Utilisées

### Backend
- Python 3.13.5  
- Flask  
- SpaCy  
- SQLAlchemy  

### Frontend
- HTML / CSS  
- JavaScript (pour les interactions du widget)

### Base de Données
- PostgreSQL  


## 📚 Structure du Dépôt



/model/ → Modèle SpaCy entraîné
/static/ → Fichiers CSS et JS
/templates/ → Interface HTML
app.py → Backend Flask
responses.py → Dictionnaire de réponses du chatbot
prepare_data.py → Préparation des données NLP
train_data.py → Entraînement du modèle SpaCy
README.md → Documentation du projet
rapport_oraflex.pdf → Rapport du projet (à ajouter)



## ▶️ Installation & Exécution

### 1. Cloner le projet
```bash
git clone  https://github.com/GOUBAGeorgette/CHATEBOT-BANCAIRE.git
cd CHATEBOT-BANCAIRE

2. Installer l’environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows

3. Installer les dépendances
pip install -r requirements.txt

4. Lancer l’application
python app.py


Le chatbot sera accessible sur :
👉 http://127.0.0.1:5000/

🗄️ Base de Données

Le projet utilise PostgreSQL.

Configurer les accès dans app.py :

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://user:password@localhost/oraflex_db"


Tables principales :

client

compte

message

👤 Auteur

GOUBA Georgette
Licence 3 Génie Logiciel – Analyse de Données
Université virtuelle de Ouagadougou

📌 Licence

Projet académique — Usage pédagogique uniquement.
