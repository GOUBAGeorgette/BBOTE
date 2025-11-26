# bank_intents.py (Données d'entraînement pour les intentions)

intents_data = [
    {
        "intent": "solde_compte",
        "examples": [
            "quel est mon solde",
            "solde du compte courant",
            "combien il me reste",
            "montant sur mon compte épargne"
        ],
        "responses": [
            "Quel compte souhaitez-vous consulter (courant ou épargne) ?",
        ]
    },
    {
        "intent": "virement",
        "examples": [
            "faire un virement",
            "transférer de l'argent",
            "virer 100 euros",
            "virer de l'argent à Alice"
        ],
        "responses": [
            "Quel montant souhaitez-vous transférer ?"
        ]
    },
    {
        "intent": "salutation",
        "examples": [
            "bonjour",
            "salut",
            "coucou",
            "hello"
        ],
        "responses": [
            "Bonjour. Comment puis-je vous aider aujourd'hui ?"
        ]
    },
    {
        "intent": "remerciement",
        "examples": [
            "merci",
            "c'est gentil",
            "merci beaucoup",
            "super"
        ],
        "responses": [
            "Avec plaisir. Y a-t-il autre chose que je puisse faire ?",
            "Je suis là pour ça !"
        ]
    },
    {
        "intent": "inconnu",
        "examples": [],
        "responses": [
            "Je n'ai pas compris votre demande. Pouvez-vous la reformuler ?",
            "Mon intention n'est pas claire. Pouvez-vous essayer d'utiliser des mots-clés différents ?"
        ]
    }
]