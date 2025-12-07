from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import spacy
import random
from bank_response import RESPONSES

app = Flask(__name__)
app.secret_key = os.urandom(24)

# --- PostgreSQL configuration ---
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:mondieujetaime@localhost/banque_chatbot_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# --- Table Client ---
class Client(db.Model):
    __tablename__ = 'client'
    id_client = db.Column(db.Integer, primary_key=True)
    prenom = db.Column(db.String(50), nullable=False)
    nom = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

# --- Table Messages ---
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id_client'), nullable=False)
    role = db.Column(db.String(10))
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.now())

# --- Création des tables ---
with app.app_context():
    db.create_all()

# --- Chargement du modèle spaCy ---
nlp = spacy.load(r"C:\Users\Pc\Desktop\DATA ANALYSE\CHATBOT_BANQUE\model\model_orabank")

# --- Fonction intention spaCy ---
def find_intent(user_message, client_id=None):
    doc = nlp(user_message)

    if not hasattr(doc, 'cats') or not doc.cats:
        return "Je n'ai pas pu comprendre votre demande.", ""

    intent = max(doc.cats, key=lambda k: doc.cats[k])

    # Récupération des réponses
    resp_list = RESPONSES.get(intent, ["Désolé, je ne sais pas répondre à cette demande."])

    # Sélection aléatoire si liste
    if isinstance(resp_list, list):
        response = random.choice(resp_list)
    else:
        response = resp_list

    return response, intent

# --- Route du chat ---
@app.route('/chat', methods=['POST'])
def chat():
    if not session.get('logged_in'):
        return jsonify({"response": "Vous devez être connecté pour utiliser le chat.", "intent": ""}), 401

    client_id = session.get('id_client')
    user_message = request.json.get('message', '')

    bot_response, intent = find_intent(user_message, client_id)

    # Enregistrer le message utilisateur
    msg_user = Message(client_id=client_id, role="user", content=user_message)
    db.session.add(msg_user)

    # Enregistrer la réponse du bot
    msg_bot = Message(client_id=client_id, role="bot", content=bot_response)
    db.session.add(msg_bot)

    db.session.commit()

    return jsonify({"response": bot_response, "intent": intent})

# --- Page home ---
@app.route('/')
def home():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    full_name = f"{session.get('prenom', 'Utilisateur')} {session.get('nom', '')}"
    return render_template('index.html', username=full_name)

# --- Login ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    success_message = request.args.get('success')
    if request.method == 'POST':
        email = request.form.get('email', '').lower()
        password = request.form.get('password')

        user = Client.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['logged_in'] = True
            session['prenom'] = user.prenom
            session['nom'] = user.nom
            session['id_client'] = user.id_client
            return redirect(url_for('home'))
        
        return render_template('login.html', error="Identifiants incorrects.", success=None)

    return render_template('login.html', error=None, success=success_message)

# --- Register ---
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        prenom = request.form.get('prenom', '').capitalize()
        nom = request.form.get('nom', '').capitalize()
        email = request.form.get('email', '').lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            return render_template('register.html', error="Les mots de passe ne correspondent pas.")
        
        if Client.query.filter_by(email=email).first():
            return render_template('register.html', error="Cet email est déjà enregistré.")
        
        hashed_password = generate_password_hash(password)
        new_user = Client(prenom=prenom, nom=nom, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login', success="Inscription réussie ! Veuillez vous connecter."))

    return render_template('register.html', error=None)

# --- Logout ---
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# --- Health Check ---
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok"}), 200

# --- Historique du chat ---
@app.route('/chat/history', methods=['GET'])
def chat_history():
    if not session.get('logged_in'):
        return jsonify([]), 401

    client_id = session.get('id_client')
    messages = Message.query.filter_by(client_id=client_id).order_by(Message.timestamp.asc()).all()

    return jsonify([{"role": m.role, "content": m.content} for m in messages])

# --- RUN ---
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='127.0.0.1', port=port)
