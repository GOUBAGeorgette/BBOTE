import spacy
import random
from bank_intents import intents_data 
# Importation des fonctions de la base de données (lecture et écriture)
from db_core import get_account_balance, execute_transfer 

# --- DONNÉES DE VALIDATION (laissé pour référence, mais non utilisé) ---
VALID_RECIPIENTS = ["mon frère", "alice", "dupont"] 

# --- CONTEXTE GLOBAL DE CONVERSATION ---
conversation_context = {
    "last_intent": None, 
    "awaiting_entity": None,
    "amount": None 
}

# Charger le modèle linguistique
try:
    nlp = spacy.load("fr_core_news_sm")
except OSError:
    print("ATTENTION : Le modèle SpaCy 'fr_core_news_sm' n'est pas trouvé. Les similarités ne fonctionneront pas.")
    nlp = None 

# Définir le seuil de similarité
SIMILARITY_THRESHOLD = 0.65
CLIENT_ID = 101 

# --- FONCTIONS D'EXTRACTION D'ENTITÉS ---

def extract_account_type(message_lower):
    if "épargne" in message_lower:
        return "épargne"
    if "courant" in message_lower or "chèque" in message_lower:
        return "courant"
    return None

def extract_amount(user_message):
    message_lower = user_message.lower()
    if "euros" in message_lower:
        parts = message_lower.split('euros')
        part_before_euros = parts[0].strip() 
        amount_string = part_before_euros.split(' ')[-1]
        try:
            amount = float(amount_string)
            return amount
        except ValueError:
            return None
    return None

def extract_recipient(user_message):
    message_lower = user_message.lower()
    if " à " in message_lower:
        parts = message_lower.split(' à ', 1)
        recipient = parts[1].strip()
        if recipient:
            return recipient
    return None

# --- FONCTION PRINCIPALE ---
def find_intent(user_message, client_id): # <-- client_id est le nouvel argument
    global conversation_context
    if any(keyword in message_lower for keyword in ["bonjour", "salut", "coucou", "hello"]):
        return 'greeting',
    if nlp is None:
        return "Le moteur NLP est désactivé."
        
    doc_user = nlp(user_message.lower())
    best_intent = "inconnu"
    highest_similarity = SIMILARITY_THRESHOLD
    message_lower = user_message.lower()

    # --- 1. GESTION DU CONTEXTE (Tour 2+) ---
    
    # Logique solde_compte (attend account_type)
    if conversation_context["awaiting_entity"] == "account_type":
        account_type = extract_account_type(message_lower)
        if account_type:
            conversation_context["last_intent"] = None
            conversation_context["awaiting_entity"] = None
            best_intent = "solde_compte" 
        else:
            return "Veuillez spécifier 'courant' ou 'épargne'."

    # Logique virement
    elif conversation_context["awaiting_entity"] in ["amount", "recipient"]:
        best_intent = conversation_context["last_intent"] 

        # Si on attend le montant
        if conversation_context["awaiting_entity"] == "amount":
            amount = extract_amount(message_lower)
            if amount:
                conversation_context["amount"] = amount
                conversation_context["awaiting_entity"] = "recipient"
                return f"Vous souhaitez transférer {amount:.2f} €. À quel destinataire (nom ou alias) ?"
            else:
                return "Je n'ai pas compris le montant. Quel montant souhaitez-vous transférer ?"

        # Si on attend le destinataire
        elif conversation_context["awaiting_entity"] == "recipient":
            recipient = message_lower.strip() 
            
            if recipient:
                amount = conversation_context["amount"]
                
                # ⬅️ APPEL À L'EXÉCUTION DU VIREMENT RÉEL
                if execute_transfer(CLIENT_ID, "courant", amount):
                    # Nettoyage et confirmation de succès
                    conversation_context["last_intent"] = None
                    conversation_context["awaiting_entity"] = None
                    conversation_context["amount"] = None
                    return f"Confirmation : Virement de {amount:.2f} € à {recipient.upper()} effectué. ✅"
                else:
                    # Gérer l'échec (solde insuffisant)
                    conversation_context["last_intent"] = None
                    conversation_context["awaiting_entity"] = None
                    conversation_context["amount"] = None
                    return "Échec du virement. Votre solde est insuffisant pour effectuer cette transaction. ❌"
            else:
                return "Veuillez entrer un nom pour le destinataire."


    # Si le contexte est vide, détection de similarité classique
    if best_intent not in ["solde_compte", "virement"]:
        for intent_group in intents_data:
            for example in intent_group["examples"]:
                doc_example = nlp(example.lower())
                similarity = doc_user.similarity(doc_example)
                
                if similarity > highest_similarity:
                    highest_similarity = similarity
                    best_intent = intent_group["intent"]
    
    print(f"-> Intention détectée : {best_intent} (Score: {highest_similarity:.2f})")
    
    # --- 2. GÉRER LES INTENTIONS SPÉCIFIQUES ---

    # A. SOLDE DE COMPTE
    if best_intent == "solde_compte":
        account_type = extract_account_type(message_lower)
        
        if account_type is None:
            conversation_context["last_intent"] = "solde_compte"
            conversation_context["awaiting_entity"] = "account_type"
            return "Quel est le solde de quel compte (courant ou épargne) ?"

        balance = get_account_balance(CLIENT_ID, account_type) 
        if balance is not None:
            return f"Le solde de votre compte {account_type} (Client {CLIENT_ID}) est de {balance:.2f} €."
        else:
            return f"Je n'ai pas pu récupérer le solde de votre compte {account_type}. Veuillez vérifier que vous possédez ce type de compte."

    # B. VIREMENT (Gestion du Tour 1)
    elif best_intent == "virement":
        amount = extract_amount(message_lower)
        recipient = extract_recipient(message_lower)
        
        # Cas 1 : Tout est présent (Montant + Destinataire)
        if amount and recipient: 
            
            # ⬅️ APPEL À L'EXÉCUTION DU VIREMENT RÉEL
            if execute_transfer(CLIENT_ID, "courant", amount):
                # Nettoyage et confirmation de succès
                conversation_context["last_intent"] = None
                conversation_context["awaiting_entity"] = None
                return f"Confirmation : Virement de {amount:.2f} € à {recipient.upper()} effectué. ✅"
            else:
                # Gérer l'échec (solde insuffisant)
                return "Échec du virement. Votre solde est insuffisant pour effectuer cette transaction. ❌"
        
        # Cas 2 : Montant seul
        elif amount:
            conversation_context["last_intent"] = "virement"
            conversation_context["awaiting_entity"] = "recipient"
            conversation_context["amount"] = amount 
            return f"Vous souhaitez transférer {amount:.2f} €. À quel destinataire (nom ou alias) ?"

        # Cas 3 : Rien n'est présent
        else:
            conversation_context["last_intent"] = "virement"
            conversation_context["awaiting_entity"] = "amount"
            return "Quel montant souhaitez-vous transférer ?"


    # --- 3. RÉPONSES ALÉATOIRES ET NETTOYAGE DU CONTEXTE ---
    for intent_group in intents_data:
        if intent_group["intent"] == best_intent:
            conversation_context["last_intent"] = None
            conversation_context["awaiting_entity"] = None
            conversation_context["amount"] = None
            return random.choice(intent_group["responses"])
            
    # 4. Si l'intention est "inconnu" (score trop bas)
    return next(item["responses"] for item in intents_data if item["intent"] == "inconnu")[0]