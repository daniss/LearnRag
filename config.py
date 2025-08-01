"""
Configuration file for French Legal RAG Assistant
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp-free")

# RAG Configuration
RAG_CONFIG = {
    "chunk_size": 500,
    "chunk_overlap": 50,
    "top_k_results": 5,
    "embedding_model": "text-embedding-ada-002",
    "chat_model": "gpt-3.5-turbo",
    "temperature": 0.1,
    "max_tokens": 800
}

# Pinecone Configuration
PINECONE_CONFIG = {
    "index_name": "french-legal-docs",
    "dimension": 1536,
    "metric": "cosine"
}

# Supported file types
SUPPORTED_FILE_TYPES = [
    "application/pdf",
    "text/plain",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
]

# French legal document types
LEGAL_DOCUMENT_TYPES = {
    "contrat": "Contrats et conventions",
    "bail": "Baux commerciaux et d'habitation", 
    "societe": "Actes de société",
    "travail": "Contrats de travail",
    "jugement": "Décisions de justice",
    "procedure": "Procédures civiles",
    "fiscal": "Documents fiscaux",
    "immobilier": "Transactions immobilières"
}

# Demo data for sales presentations
DEMO_METRICS = {
    "time_saved_per_search": "15 minutes",
    "accuracy_rate": "95%",
    "documents_per_second": "100+",
    "languages_supported": ["Français", "English"],
    "annual_savings": "€15,000"
}

# Pricing configuration (in EUR)
PRICING_TIERS = {
    "starter": {
        "setup_fee": 5000,
        "monthly_fee": 1500,
        "max_documents": 1000,
        "support": "Email",
        "features": ["Document analysis", "Basic search", "PDF export"]
    },
    "professional": {
        "setup_fee": 8000,
        "monthly_fee": 2500,
        "max_documents": 5000,
        "support": "Phone + Email",
        "features": ["All Starter features", "Custom integration", "Advanced analytics", "Team training"]
    },
    "enterprise": {
        "setup_fee": "Sur devis",
        "monthly_fee": "Sur devis",
        "max_documents": "Illimités",
        "support": "Dedicated account manager",
        "features": ["All Professional features", "API access", "Custom development", "SLA guarantee"]
    }
}

# French business outreach data
TARGET_CITIES = [
    "Lyon", "Marseille", "Toulouse", "Nice", "Nantes", 
    "Montpellier", "Strasbourg", "Bordeaux", "Lille", "Rennes"
]

# Email templates
EMAIL_TEMPLATES = {
    "cold_outreach": """
Objet: Cabinet {firm_name} - 70% moins de temps sur la recherche juridique

Bonjour {first_name},

J'ai vu que votre cabinet traite beaucoup de dossiers {specialty}.

Question rapide : combien d'heures par semaine votre équipe passe-t-elle à chercher des précédents dans vos archives ?

Notre outil IA peut réduire ce temps de 70% en trouvant instantanément les bonnes réponses avec citations exactes.

Intéressé par une démo de 15 minutes cette semaine ?

Cordialement,
{sender_name}

P.S. Garantie satisfait ou remboursé - comme {reference_firm} qui économise déjà 15h/semaine
""",
    
    "follow_up": """
Objet: Suivi - Démo IA juridique pour {firm_name}

Bonjour {first_name},

Je vous avais contacté la semaine dernière concernant notre assistant IA qui fait gagner 15h/semaine aux cabinets d'avocats.

Bonne nouvelle : nous avons une nouvelle case study avec un cabinet de {city} qui économise maintenant €1,200/mois en temps de recherche.

Toujours intéressé par une démo rapide ?

Cordialement,
{sender_name}
""",
    
    "demo_invitation": """
Objet: [URGENT] Places limitées - Démo gratuite assistant juridique IA

Bonjour {first_name},

Seulement 3 places restantes cette semaine pour notre démo exclusive.

Ce que vous verrez en 15 minutes :
✓ Analyse instantanée de vos contrats
✓ Réponses précises avec sources citées  
✓ ROI calculé pour votre cabinet

Réservez votre créneau : [CALENDLY_LINK]

Cordialement,
{sender_name}
"""
}

# Legal specialties for targeting
LEGAL_SPECIALTIES = [
    "droit des affaires",
    "droit immobilier", 
    "droit du travail",
    "droit de la famille",
    "droit pénal",
    "droit commercial",
    "droit fiscal",
    "droit des contrats"
]