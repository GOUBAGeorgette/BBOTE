DATABASE = {
    101: {
        "courant": 5000.00,
        "épargne": 1250.75
    }
}

def get_account_balance(client_id, account_type):
    """Récupère le solde d'un type de compte pour un client donné."""
    if client_id in DATABASE and account_type in DATABASE[client_id]:
        return DATABASE[client_id][account_type]
    return None



def execute_transfer(client_id, account_type, amount):
    """
    Placeholder pour la fonction de virement. 
    Pour l'instant, elle retourne toujours True pour simuler le succès.
    """
    
    return True

def execute_transfer(client_id, source_account, amount):
    """
    Simule l'exécution d'un virement en débitant le compte source.
    Retourne True si le débit est effectué, False sinon (solde insuffisant).
    """
    
    if client_id not in DATABASE:
        return False
        
    if source_account is None:
        source_account = "courant"
        
    if source_account not in DATABASE[client_id]:
        return False
        
    current_balance = DATABASE[client_id][source_account]
    
    if current_balance >= amount:
        # ACTION CRUCIALE : Débiter le montant
        DATABASE[client_id][source_account] -= amount
        print(f"DEBUG: Compte {source_account} débité de {amount}€. Nouveau solde: {DATABASE[client_id][source_account]}")
        return True
    else:
        return False