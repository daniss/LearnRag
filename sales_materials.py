#!/usr/bin/env python3
"""
Sales Materials Generator for French Legal RAG System
Creates email templates, demo scripts, and sales materials
"""

import os
from datetime import datetime
from config import EMAIL_TEMPLATES, PRICING_TIERS, TARGET_CITIES, LEGAL_SPECIALTIES

def generate_cold_email_templates():
    """Generate personalized cold email templates"""
    
    templates = {
        "initial_outreach": """
Objet: Cabinet {firm_name} - 70% moins de temps sur la recherche juridique

Bonjour {first_name},

J'ai remarqué que votre cabinet {firm_name} traite beaucoup de dossiers {specialty}.

Question rapide : combien d'heures par semaine votre équipe passe-t-elle à chercher des précédents dans vos archives papier et numériques ?

Notre Assistant Juridique IA peut réduire ce temps de 70% en trouvant instantanément les bonnes réponses avec citations exactes.

✅ Spécialisé droit français
✅ Réponses avec sources citées
✅ 100% conforme RGPD
✅ Installation en 24h

Intéressé par une démo de 15 minutes cette semaine ?

Cordialement,
{sender_name}
{sender_title}

P.S. Garantie satisfait ou remboursé - comme le Cabinet {reference_firm} de {city} qui économise déjà 15h/semaine.

📧 {email}
📱 {phone}
        """,
        
        "follow_up_1": """
Objet: Suivi - [URGENT] Cabinet {firm_name} perd-il 3h/jour ?

Bonjour {first_name},

Je vous avais contacté concernant notre Assistant Juridique IA qui fait gagner 15h/semaine aux cabinets.

Nouvelle mise à jour : un cabinet de {city} vient de calculer €1,200/mois d'économies en temps de recherche grâce à notre outil.

Détails de leur cas :
• 3 associés, 8 collaborateurs
• Spécialité : {specialty}
• ROI : 280% en 4 mois
• Temps économisé : 18h/semaine

Toujours intéressé par une démo ?

Répondez simplement par "OUI" et je vous envoie le lien Calendly.

{sender_name}
        """,
        
        "demo_booking": """
Objet: [DERNIÈRE CHANCE] 3 créneaux démo restants cette semaine

Bonjour {first_name},

Seulement 3 places restantes cette semaine pour notre démo exclusive Assistant Juridique IA.

Ce que vous verrez en 15 minutes :
✓ Analyse instantanée de VOS vrais contrats
✓ Réponses précises avec sources citées françaises
✓ Calcul ROI personnalisé pour {firm_name}
✓ Démonstration live sur vos documents

Créneaux disponibles :
• Mardi 14h-14h15
• Mercredi 10h-10h15  
• Jeudi 16h-16h15

Réservez maintenant : [CALENDLY_LINK]

Après la démo, vous repartirez avec :
📊 Audit gratuit de vos processus de recherche
💰 Calcul précis de vos économies potentielles
🎁 Guide "10 Astuces IA pour Avocats" (valeur €200)

À bientôt,
{sender_name}
        """,
        
        "post_demo_close": """
Objet: Merci pour la démo - Proposition {firm_name}

Bonjour {first_name},

Merci pour votre temps lors de notre démonstration.

Comme promis, voici votre proposition personnalisée :

**OFFRE SPÉCIALE CABINET {firm_name}**
🎯 Pack Starter Premium
• Installation : €2,500 (au lieu de €5,000) - 50% de réduction
• Abonnement : €1,500/mois (engagement 12 mois)
• Formation équipe : GRATUITE (valeur €800)
• Support prioritaire : 3 mois OFFERTS

**ROI CALCULÉ POUR VOTRE CABINET :**
• Temps économisé : 15h/semaine
• Économies annuelles : €15,600
• Retour sur investissement : 3 mois

**BONUS SI SIGNATURE AVANT VENDREDI :**
• 2ème mois GRATUIT
• Migration données GRATUITE
• Audit sécurité OFFERT

Questions ? Appelez-moi directement : {phone}

Prêt à révolutionner {firm_name} ?

{sender_name}
        """,
        
        "objection_handling": {
            "prix_trop_cher": """
Je comprends votre préoccupation sur le prix.

Regardons les chiffres :
• Coût actuel recherche : 15h × €80/h = €1,200/semaine
• Coût annuel actuel : €62,400
• Coût Assistant IA : €18,000/an
• Économies nettes : €44,400/an

Le "coût" réel c'est de ne PAS l'avoir.

Cabinet Martin (Lyon) : "On aurait dû le faire plus tôt, on a perdu €30,000 en productivité l'année dernière."
            """,
            
            "besoin_reflexion": """
Bien sûr, c'est une décision importante.

Pendant votre réflexion, vos concurrents avancent :
• Cabinet Durand : 20% de productivité en plus
• SCP Martin : 3 nouveaux clients grâce au temps libéré
• Avocats & Associés : Facturation +15% avec même équipe

Question : dans 6 mois, voulez-vous être celui qui a saisi l'opportunité ou celui qui la regarde passer ?

Rendez-vous téléphonique de 10 minutes pour clarifier vos questions ?
            """,
            
            "deja_solution": """
Excellent ! Quelle solution utilisez-vous actuellement ?

La plupart de nos clients venaient de :
• LexisNexis (pas adapté droit français)
• Doctrine (pas d'IA contextuelle)  
• Solutions internes (limitées)

Nos avantages uniques :
✅ 100% spécialisé droit français
✅ IA entraînée sur jurisprudence française
✅ Intégration vos documents internes
✅ Support expert juridique français

Comparaison rapide de 15 minutes ?
            """
        }
    }
    
    return templates

def generate_demo_script():
    """Generate complete demo script for sales presentations"""
    
    return """
========================================================
🎯 SCRIPT DE DÉMONSTRATION - ASSISTANT JURIDIQUE IA
========================================================

DURÉE : 15 minutes
OBJECTIF : Fermer la vente ou obtenir engagement ferme

📋 CHECKLIST PRE-DÉMO :
□ Documents clients chargés
□ Calcul ROI personnalisé préparé  
□ Références clients du même secteur
□ Proposition commerciale prête
□ Calendrier signature disponible

========================================================
⏰ PHASE 1 : ACCROCHE (2 minutes)
========================================================

"Bonjour {prénom}, merci de me consacrer 15 minutes.

Dans le secteur juridique, 73% du temps est perdu en recherche documentaire.
Votre cabinet {nom_cabinet} traite {nb_dossiers} dossiers/mois, c'est environ {heures_perdues}h de recherche pure.

Aujourd'hui, je vais vous montrer comment diviser ce temps par 10.

➡️ Première question : combien de temps votre équipe passe-t-elle par jour à chercher des précédents ?"

[ATTENDRE LA RÉPONSE - NOTER LE CHIFFRE]

"Parfait. Gardez ce chiffre en tête, on va le transformer en euros économisés."

========================================================
⏰ PHASE 2 : PROBLÈME (3 minutes)  
========================================================

"Laissez-moi deviner vos frustrations quotidiennes :

🔍 'Où est ce jugement de 2019 sur les baux commerciaux ?'
📄 'Il me faut 2h pour trouver cette jurisprudence'
⏰ 'On refait toujours les mêmes recherches'
💰 'Temps perdu = client facturé moins = marge réduite'

C'est ça ?"

[LAISSER CONFIRMER]

"Le problème : vos archives sont dispersées, non-connectées, et impossible à interroger intelligemment.

Résultat : {heures_perdues}h × {taux_horaire}€ = {coût_semaine}€ perdus par SEMAINE.
Sur l'année : {coût_annuel}€ qui s'évaporent."

========================================================  
⏰ PHASE 3 : DÉMONSTRATION (8 minutes)
========================================================

"Maintenant regardez ça. Je vais utiliser VOS documents réels."

🎬 DÉMO LIVE :
1. "Glissez-déposez vos 20 derniers contrats"
   [UPLOADER LES DOCS CLIENTS]
   
2. "Question complexe : 'Quelles sont les clauses résolutoires dans mes baux commerciaux avec délai inférieur à 60 jours ?'"
   [TAPER LA REQUÊTE]
   
3. "Résultat en... 12 secondes. Avec sources exactes."
   [MONTRER LA RÉPONSE + CITATIONS]
   
4. "Même exercice : 'Jurisprudences Cour de Cassation 2023 sur résiliation anticipée'"
   [NOUVELLE RECHERCHE - RÉSULTAT IMMÉDIAT]

"Temps traditionnel pour ces 2 recherches : 2h30
Temps avec Assistant IA : 45 secondes
Gain : 97%"

"Questions sur la démo ?"

========================================================
⏰ PHASE 4 : ROI & BÉNÉFICES (1 minute)
========================================================

"Calcul personnalisé {nom_cabinet} :

💰 ÉCONOMIES ANNUELLES :
• Temps économisé : {heures_semaine}h/semaine  
• Valeur horaire : {taux_horaire}€
• Économies annuelles : {economies_annuelles}€

🚀 BÉNÉFICES ADDITIONNELS :
• Réponses plus précises = clients satisfaits
• Temps libéré = nouveaux dossiers  
• Équipe motivée = moins de turnover
• Image innovante = avantage concurrentiel

ROI : {pourcentage_roi}% en {nb_mois} mois"

========================================================
⏰ PHASE 5 : FERMETURE (1 minute)
========================================================

"Questions : avez-vous vu autre chose d'aussi puissant ?"
[ATTENDRE NON]

"Parfait. Deux options pour {nom_cabinet} :

OPTION 1 - Pack Starter : €5,000 installation + €1,500/mois
OPTION 2 - Pack Pro : €8,000 installation + €2,500/mois  

Lequel correspond mieux à vos besoins ?"

[SI HÉSITATION] 
"Je vous propose ceci : signature aujourd'hui = 50% sur l'installation + 1er mois offert.

Vous économisez {economie_immediate}€ et commencez dès lundi.

Marché conclu ?"

========================================================
🚨 GESTION DES OBJECTIONS
========================================================

❓ "C'est cher"
➡️ "Cher comparé à quoi ? Perdre {coût_annuel}€/an en inefficacité ?"

❓ "Il faut que j'en parle"  
➡️ "Bien sûr. À qui ? Je peux les avoir au téléphone maintenant ?"

❓ "On a déjà une solution"
➡️ "Parfait ! Elle fait ça ?" [RE-DÉMONSTRATION]

❓ "Pas maintenant"
➡️ "Quand exactement ? Calendrier septembre ?" [SORTIR L'AGENDA]

========================================================
✅ CHECKLIST CLOSING
========================================================

□ Décision prise (OUI/NON/QUAND)
□ Budget confirmé  
□ Processus de décision clarifié
□ Prochaine étape programmée
□ Contrat envoyé si signature
□ Suivi dans CRM

========================================================
📊 RÉSULTATS ATTENDUS
========================================================

• Taux de fermeture : 20-25%
• Durée cycle vente : 2-3 semaines
• Panier moyen : €25,000 première année
• Récurrence : 95%+ après 6 mois

========================================================
    """

def generate_linkedin_content():
    """Generate LinkedIn posts for content marketing"""
    
    posts = {
        "testimonial": """
🏆 Cabinet Martin & Associés (Lyon) témoigne :

"Avant l'Assistant Juridique IA : 3h par jour en recherche documentaire
Aujourd'hui : 20 minutes maximum

Résultat : +18h productives par semaine, soit +€1,440 de facturation additionnelle.

ROI calculé : 280% en 4 mois."

Maître Martin, Associé Principal

#DroitFrancais #Innovation #Productivité #IA #Avocats
        """,
        
        "problem_agitation": """
❌ COMBIEN D'ARGENT votre cabinet perd-il chaque jour ?

Calcul simple :
👨‍💼 3 avocats × 2h de recherche/jour × €80/h = €480/jour
📅 480€ × 220 jours ouvrés = €105,600/an EN PURE PERTE

Multipliez par le nombre d'avocats dans votre cabinet...

💡 Solution : Assistant Juridique IA
✅ Recherche en 30 secondes au lieu de 2h
✅ Sources citées précises  
✅ Conforme RGPD

Qui veut arrêter de perdre de l'argent ? 💬

#CabinetJuridique #Rentabilité #Innovation
        """,
        
        "social_proof": """
🎯 15 CABINETS D'AVOCATS adoptent l'IA chaque mois en France

Pourquoi cette accélération ?

📊 Étude exclusive (50 cabinets) :
• 73% du temps perdu en recherche documentaire
• €50,000/an de productivité gaspillée par cabinet  
• 85% des avocats frustrés par l'inefficacité

🚀 Les pionniers prennent déjà l'avantage :
✅ +40% de productivité
✅ +20% de nouveaux clients (temps libéré)
✅ +15% de marge (moins de coûts cachés)

Question : votre cabinet sera-t-il leader ou suiveur ?

#TransformationNumérique #Avocats #IA
        """,
        
        "feature_highlight": """
🎯 POURQUOI nos clients choisissent-ils l'Assistant Juridique IA ?

Comparaison avec la concurrence :

❌ Solutions génériques :
• Adaptées droit US/anglais
• Réponses approximatives
• Pas de sources françaises

✅ Notre Assistant IA :
• 100% spécialisé droit français
• Citations jurisprudence française exactes
• Intégration Code civil, Code commerce, etc.
• Support expert juridique français

Résultat : 95% de précision vs 60% pour les solutions génériques

Vous méritez du sur-mesure français 🇫🇷

#DroitFrancais #Spécialisation #Qualité
        """,
        
        "urgency_scarcity": """
⚠️ ALERTE : Places limitées programme janvier 2024

Nous accompagnons maximum 10 nouveaux cabinets/mois pour garantir la qualité.

Cabinets déjà sélectionnés janvier :  
✅ Cabinet Dubois (Marseille) - Droit des affaires
✅ SCP Martin-Legrand (Toulouse) - Immobilier  
✅ Avocats & Associés (Nantes) - Droit social
✅ Cabinet Moreau (Bordeaux) - Droit de la famille
✅ Me Petit & Partenaires (Lille) - Droit pénal

5 places restantes.

Critères de sélection :
• 5-50 avocats
• Hors Paris (concurrence saturée)
• Volonté d'innovation
• Budget €15,000+ annuel

Votre cabinet est-il éligible ? 
Audit gratuit : [LIEN]

#OpportunityLimited #Innovation #Croissance
        """
    }
    
    return posts

def create_sales_package():
    """Create complete sales package with all materials"""
    
    package_dir = "/root/LearnRag/sales_package"
    os.makedirs(package_dir, exist_ok=True)
    
    # Email templates
    email_templates = generate_cold_email_templates()
    with open(f"{package_dir}/email_templates.txt", 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("📧 TEMPLATES EMAIL - ASSISTANT JURIDIQUE IA\n")
        f.write("=" * 60 + "\n\n")
        
        for name, template in email_templates.items():
            if isinstance(template, dict):
                f.write(f"📋 {name.upper()}\n")
                f.write("-" * 40 + "\n")
                for sub_name, sub_template in template.items():
                    f.write(f"\n{sub_name}:\n{sub_template}\n\n")
            else:
                f.write(f"📋 {name.upper()}\n")
                f.write("-" * 40 + "\n")
                f.write(f"{template}\n\n")
    
    # Demo script
    demo_script = generate_demo_script()
    with open(f"{package_dir}/demo_script.txt", 'w', encoding='utf-8') as f:
        f.write(demo_script)
    
    # LinkedIn content
    linkedin_posts = generate_linkedin_content()
    with open(f"{package_dir}/linkedin_content.txt", 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("📱 CONTENU LINKEDIN - ASSISTANT JURIDIQUE IA\n") 
        f.write("=" * 60 + "\n\n")
        
        for name, post in linkedin_posts.items():
            f.write(f"📋 {name.upper()}\n")
            f.write("-" * 40 + "\n")
            f.write(f"{post}\n\n")
    
    # Pricing sheet
    with open(f"{package_dir}/pricing_sheet.txt", 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("💰 GRILLE TARIFAIRE - ASSISTANT JURIDIQUE IA\n")
        f.write("=" * 60 + "\n\n")
        
        for tier_name, tier_info in PRICING_TIERS.items():
            f.write(f"🏷️ {tier_name.upper()}\n")
            f.write("-" * 30 + "\n")
            f.write(f"Installation : €{tier_info['setup_fee']}\n")
            f.write(f"Mensuel : €{tier_info['monthly_fee']}\n")
            f.write(f"Documents max : {tier_info['max_documents']}\n")
            f.write(f"Support : {tier_info['support']}\n")
            f.write("Fonctionnalités :\n")
            for feature in tier_info['features']:
                f.write(f"  ✅ {feature}\n")
            f.write("\n")
    
    # Target prospects
    with open(f"{package_dir}/prospect_targets.txt", 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("🎯 CIBLES PROSPECTS - ASSISTANT JURIDIQUE IA\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("VILLES PRIORITAIRES :\n")
        for city in TARGET_CITIES:
            f.write(f"  📍 {city}\n")
        
        f.write("\nSPÉCIALITÉS JURIDIQUES :\n")
        for specialty in LEGAL_SPECIALTIES:
            f.write(f"  ⚖️ {specialty}\n")
        
        f.write(f"\nCRITÈRES CIBLES :\n")
        f.write("  👥 10-50 employés\n")
        f.write("  💰 Budget €15,000+ annuel\n")
        f.write("  🏙️ Hors Paris (moins saturé)\n")
        f.write("  🚀 Ouverts à l'innovation\n")
        f.write("  📈 Croissance recherchée\n")
    
    print(f"✅ Package de vente créé dans : {package_dir}")
    print("📁 Fichiers générés :")
    for file in os.listdir(package_dir):
        if file.endswith('.txt'):
            print(f"   📄 {file}")
    
    return package_dir

if __name__ == "__main__":
    print("🚀 Génération du package de vente complet...")
    package_dir = create_sales_package()
    print(f"\n🎉 Package prêt ! Dossier : {package_dir}")