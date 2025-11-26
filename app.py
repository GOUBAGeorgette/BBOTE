from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from nlp_core import find_intent 
import os 
from urllib.parse import unquote 

# --- Base de Données Clients (CLEAN et COMPLET) ---
CLIENTS_DB = {
    "pierre.durand@mail.com": {
        "prenom": "Pierre",
        "nom": "Durand",
        "password": "pierre123",
        "id_client": "101"
    },
    "alice.dupont@mail.com": {
        "prenom": "Alice",
        "nom": "Dupont",
        "password": "alice123",
        "id_client": "102"
    },
    "georgette.gouba@mail.com": {
        "prenom": "Georgette",
        "nom": "Gouba",
        "password": "Geogeo123",
        "id_client": "103"
    }
}
# --------------------------------------------------------

app = Flask(__name__)
app.secret_key = os.urandom(24) 

# --- Route de Chatbot (FIX: Passage de l'ID Client) ---
@app.route('/chat', methods=['POST'])
def chat():
    # 🚨 FIX CRITIQUE : Récupération de l'ID client de la session 🚨
    if not session.get('logged_in'):
        return jsonify({"response": "Vous devez être connecté pour utiliser le chat."}), 401
    
    # L'ID client est stocké dans la session après la connexion
    client_id = session.get('id_client')
    user_message = request.json.get('message')
    
    # 🚨 FIX CRITIQUE : L'ID client est passé à find_intent 🚨
    # NOTE: L'ID client est stocké en chaîne, nous le convertissons en entier si nécessaire plus tard.
    bot_response = find_intent(user_message, int(client_id)) 
    
    return jsonify({"response": bot_response})


# --- Routes d'Authentification et de Navigation (Manquantes) ---

@app.route('/')
def home():
    """Affiche la page de chat, mais seulement si l'utilisateur est connecté."""
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    full_name = f"{session.get('prenom', 'Utilisateur')} {session.get('nom', '')}"
    return render_template('index.html', username=full_name)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Gère le processus de connexion."""
    success_message = request.args.get('success') 
    
    if request.method == 'POST':
        email_attempt = request.form.get('email', '').lower()
        prenom_attempt = request.form.get('prenom', '').capitalize()
        nom_attempt = request.form.get('nom', '').capitalize()
        password_attempt = request.form.get('password')

        if email_attempt in CLIENTS_DB:
            client_data = CLIENTS_DB[email_attempt]
            
            if (password_attempt == client_data['password'] and
                prenom_attempt == client_data['prenom'] and
                nom_attempt == client_data['nom']):
                
                # Succès : Enregistrement de la session
                session['logged_in'] = True
                session['prenom'] = client_data['prenom']
                session['nom'] = client_data['nom']
                # Stockage de l'ID client dans la session
                session['id_client'] = client_data['id_client'] 
                return redirect(url_for('home'))
        
        return render_template('login.html', error='Identifiants incorrects.')
            
    return render_template('login.html', error=None, success=success_message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Gère l'inscription des nouveaux utilisateurs avec confirmation du mot de passe."""
    # Le reste de ta logique /register est ici...
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        prenom = request.form.get('prenom', '').capitalize()
        nom = request.form.get('nom', '').capitalize()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # 1. Vérification de la confirmation du mot de passe
        if password != confirm_password:
            return render_template('register.html', error='Les mots de passe ne correspondent pas.')

        # 2. Vérification si l'utilisateur existe déjà
        if email in CLIENTS_DB:
            return render_template('register.html', error='Cet email est déjà enregistré.')

        # 3. Création du nouvel ID client et ajout
        last_id = max(int(data["id_client"]) for data in CLIENTS_DB.values()) if CLIENTS_DB else 100
        new_id = str(last_id + 1)
        
        CLIENTS_DB[email] = {
            "prenom": prenom,
            "nom": nom,
            "password": password,
            "id_client": new_id
        }
        
        return redirect(url_for('login', success='Inscription réussie ! Veuillez vous connecter.'))

    return render_template('register.html', error=None)


@app.route('/logout')
def logout():
    """Déconnecte l'utilisateur en vidant la session."""
    session.clear()
    return redirect(url_for('login')) 

# 🚨 LIGNE CRITIQUE MANQUANTE POUR LANCER LE SERVEUR 🚨
if __name__ == '__main__':
    app.run(debug=True)