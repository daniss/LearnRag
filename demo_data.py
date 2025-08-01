"""
Demo data generator for French Legal RAG system
Creates sample legal documents for demonstrations
"""

import os
from datetime import datetime

def create_sample_legal_documents():
    """Create sample French legal documents for demo purposes"""
    
    # Create demo_docs directory
    demo_dir = "/root/LearnRag/demo_docs"
    os.makedirs(demo_dir, exist_ok=True)
    
    # Sample French legal documents
    documents = {
        "contrat_bail_commercial.txt": """
CONTRAT DE BAIL COMMERCIAL

Entre les soussignés :
Monsieur Jean MARTIN, propriétaire
Et la société ABC SARL, locataire

ARTICLE 1 - DÉSIGNATION DES LOCAUX
Les locaux loués sont situés au 123 Avenue de la République, 69003 Lyon.
Surface : 150 m² au rez-de-chaussée avec vitrine.

ARTICLE 2 - DURÉE DU BAIL
Le présent bail est consenti pour une durée de 9 ans à compter du 1er janvier 2024.

ARTICLE 3 - LOYER ET CHARGES
Le loyer mensuel est fixé à 2 500 euros hors taxes.
Les charges communes s'élèvent à 300 euros par mois.

ARTICLE 4 - OBLIGATIONS DU BAILLEUR
- Délivrer les locaux en bon état de réparations locatives
- Assurer la jouissance paisible des lieux
- Effectuer les grosses réparations selon l'article 606 du Code civil
- Maintenir les parties communes en bon état

ARTICLE 5 - OBLIGATIONS DU LOCATAIRE  
- Payer le loyer et les charges aux échéances convenues
- Souscrire une assurance responsabilité civile et incendie
- Utiliser les locaux conformément à leur destination commerciale
- Effectuer les réparations locatives

ARTICLE 6 - CLAUSE RÉSOLUTOIRE
À défaut de paiement du loyer à l'échéance, le présent bail sera automatiquement résilié de plein droit si le locataire n'a pas remédié à ce manquement dans les 30 jours suivant une mise en demeure restée infructueuse.

ARTICLE 7 - RÉVISION DU LOYER
Le loyer sera révisé tous les 3 ans selon l'indice du coût de la construction publié par l'INSEE.

Fait à Lyon, le 15 décembre 2023
Signatures des parties
""",

        "contrat_travail_cdi.txt": """
CONTRAT DE TRAVAIL À DURÉE INDÉTERMINÉE

EMPLOYEUR : Société TECH SOLUTIONS SAS
Siège social : 45 Rue de la Paix, 75002 Paris
SIRET : 12345678901234

SALARIÉ : Madame Marie DUBOIS
Domicile : 12 Rue des Fleurs, 92100 Boulogne

ARTICLE 1 - ENGAGEMENT
Madame DUBOIS est engagée en qualité de Développeuse Senior à compter du 2 janvier 2024.

ARTICLE 2 - FONCTIONS
Le salarié exercera les fonctions de :
- Développement d'applications web
- Architecture technique des projets
- Encadrement d'équipe de 3 développeurs junior
- Participation aux choix technologiques

ARTICLE 3 - RÉMUNÉRATION
Le salaire brut mensuel est fixé à 4 500 euros.
Le salarié bénéficie de tickets restaurant d'une valeur de 9 euros par jour travaillé.

ARTICLE 4 - DURÉE DU TRAVAIL
La durée hebdomadaire de travail est fixée à 35 heures réparties du lundi au vendredi.
Horaires : 9h00 - 17h30 avec 1h30 de pause déjeuner.

ARTICLE 5 - CONGÉS PAYÉS
Le salarié a droit aux congés payés légaux soit 2,5 jours ouvrables par mois travaillé.

ARTICLE 6 - PÉRIODE D'ESSAI
La période d'essai est fixée à 4 mois renouvelable une fois.

ARTICLE 7 - CONFIDENTIALITÉ
Le salarié s'engage à respecter la confidentialité absolue sur tous les projets de l'entreprise et les informations dont il aura connaissance.

ARTICLE 8 - CLAUSE DE NON-CONCURRENCE
Pendant une durée de 12 mois après la rupture du contrat, le salarié s'interdit d'exercer une activité concurrente dans un rayon de 50 km autour de Paris.
Cette clause ouvre droit à une indemnité égale à 50% du salaire mensuel brut.

Fait à Paris, le 20 décembre 2023
Signatures des parties
""",

        "jugement_tribunal_commerce.txt": """
TRIBUNAL DE COMMERCE DE LYON
3ème Chambre

JUGEMENT DU 15 NOVEMBRE 2023

DEMANDEUR : SAS ALPHA DISTRIBUTION
Représentée par Maître BERNARD, avocat au barreau de Lyon

DÉFENDEUR : SARL BETA SERVICES  
Représentée par Maître LAURENT, avocat au barreau de Lyon

OBJET : Demande de paiement de factures impayées

LE TRIBUNAL :

Vu les conclusions déposées par les parties ;
Vu les pièces produites ;

SUR LA DEMANDE PRINCIPALE :

ATTENDU que la société ALPHA DISTRIBUTION réclame le paiement de factures d'un montant total de 45 000 euros ;

ATTENDU que ces factures correspondent à des prestations de conseil effectivement réalisées entre janvier et juin 2023 ;

ATTENDU que la société BETA SERVICES ne conteste pas la réalité des prestations mais invoque des difficultés financières temporaires ;

ATTENDU que les difficultés financières ne constituent pas un motif d'exonération du paiement des dettes certaines, liquides et exigibles ;

SUR LES INTÉRÊTS ET PÉNALITÉS :

ATTENDU que les factures étaient payables à 30 jours ;
ATTENDU que le retard de paiement ouvre droit aux intérêts légaux et à l'indemnité forfaitaire de 40 euros par facture ;

PAR CES MOTIFS :

CONDAMNE la SARL BETA SERVICES à payer à la SAS ALPHA DISTRIBUTION :
- La somme de 45 000 euros en principal
- Les intérêts légaux à compter de l'échéance de chaque facture
- L'indemnité forfaitaire de 200 euros (5 factures × 40 euros)
- La somme de 1 500 euros au titre de l'article 700 du CPC

CONDAMNE la SARL BETA SERVICES aux dépens.

Le Président : Monsieur MARTIN
Le Greffier : Madame DURAND
""",

        "procedure_civile_assignation.txt": """
ASSIGNATION DEVANT LE TRIBUNAL JUDICIAIRE

L'AN DEUX MILLE VINGT-QUATRE
Le 10 janvier

À la requête de :
Monsieur Pierre MOREAU
Demeurant 25 Avenue Victor Hugo, 13001 Marseille

Ayant pour avocat :
Maître Sophie BLANC
Avocat au Barreau de Marseille

J'ai Jean-Claude PETIT, Huissier de justice à Marseille, signifié à :

Madame Claire VINCENT  
Demeurante 78 Boulevard Michelet, 13008 Marseille

QU'ELLE AIT À COMPARAÎTRE devant le Tribunal Judiciaire de Marseille
Audience du mardi 15 mars 2024 à 14h00

POUR S'ENTENDRE CONDAMNER À :

1°) PAYER la somme de 25 000 euros correspondant aux dommages-intérêts pour rupture abusive de compromis de vente

2°) PAYER les intérêts légaux à compter de la mise en demeure du 15 octobre 2023

3°) PAYER la somme de 3 000 euros sur le fondement de l'article 700 du Code de procédure civile

4°) SUPPORTER les dépens de l'instance

MOTIFS DE LA DEMANDE :

ATTENDU QUE par compromis de vente du 1er septembre 2023, Madame VINCENT s'était engagée à vendre à Monsieur MOREAU un appartement situé à Marseille 6ème pour le prix de 350 000 euros ;

ATTENDU QUE la vente devait être réalisée le 15 novembre 2023 ;

ATTENDU QUE Madame VINCENT a refusé de signer l'acte de vente sans motif légitime ;

ATTENDU QUE cette rupture abusive a causé un préjudice à Monsieur MOREAU qui avait déjà engagé des frais et perdu d'autres opportunités d'achat ;

ATTENDU QUE l'article 1142 du Code civil dispose que toute obligation de faire se résout en dommages-intérêts en cas d'inexécution ;

PIÈCES INVOQUÉES :
- Compromis de vente du 1er septembre 2023
- Correspondances entre les parties
- Attestation du notaire
- Justificatifs des frais engagés

FAIT ET SIGNIFIÉ à Marseille, les jour, mois et an que dessus

Jean-Claude PETIT
Huissier de Justice
""",

        "statuts_sarl.txt": """
STATUTS DE LA SOCIÉTÉ À RESPONSABILITÉ LIMITÉE
"INNOVATION TECH SARL"

ARTICLE 1 - CONSTITUTION
Il est constitué par les présents statuts une société à responsabilité limitée régie par les dispositions des articles L223-1 et suivants du Code de commerce.

ARTICLE 2 - DÉNOMINATION SOCIALE
La société a pour dénomination sociale : "INNOVATION TECH SARL"

ARTICLE 3 - SIÈGE SOCIAL  
Le siège social est fixé à : 15 Rue de la République, 69001 Lyon
Il peut être transféré par décision de l'assemblée générale extraordinaire.

ARTICLE 4 - OBJET SOCIAL
La société a pour objet :
- Le développement de logiciels informatiques
- La création d'applications mobiles et web
- Le conseil en systèmes d'information
- La formation en nouvelles technologies
Et généralement toutes opérations se rattachant directement ou indirectement à cet objet.

ARTICLE 5 - DURÉE
La durée de la société est de 99 années à compter de son immatriculation au RCS.

ARTICLE 6 - CAPITAL SOCIAL
Le capital social est fixé à 10 000 euros divisé en 100 parts de 100 euros chacune.

ARTICLE 7 - RÉPARTITION DES PARTS
Les parts sont réparties comme suit :
- Monsieur Thomas MARTIN : 60 parts (6 000 euros)
- Madame Julie BERNARD : 40 parts (4 000 euros)

ARTICLE 8 - GÉRANCE
La société est gérée par Monsieur Thomas MARTIN, associé, nommé pour une durée illimitée.

Le gérant a les pouvoirs les plus étendus pour agir au nom de la société dans tous les actes de la vie civile et commerciale.

ARTICLE 9 - DÉCISIONS COLLECTIVES
Les décisions collectives sont prises en assemblée générale ou par consultation écrite.

Les décisions ordinaires sont prises à la majorité simple des parts présentes ou représentées.
Les décisions extraordinaires nécessitent la majorité des 2/3 des parts.

ARTICLE 10 - COMPTES SOCIAUX
L'exercice social commence le 1er janvier et finit le 31 décembre.

Les comptes annuels sont arrêtés par le gérant et approuvés par l'assemblée générale dans les 6 mois de la clôture.

ARTICLE 11 - RÉPARTITION DES BÉNÉFICES
Le bénéfice distribuable est réparti entre les associés proportionnellement à leurs parts.

Fait à Lyon, le 1er octobre 2023
Signatures des associés
"""
    }
    
    # Write each document to a file
    for filename, content in documents.items():
        filepath = os.path.join(demo_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    print(f"✅ Created {len(documents)} demo legal documents in {demo_dir}")
    return demo_dir

def get_demo_queries():
    """Return sample queries that work well with the demo documents"""
    return [
        "Quelles sont les obligations du bailleur dans le contrat de bail commercial ?",
        "Quelle est la durée de la période d'essai dans le contrat de travail ?",
        "Quel est le montant réclamé dans le jugement du tribunal de commerce ?",
        "Qui sont les associés de la SARL Innovation Tech ?",
        "Quels sont les motifs de l'assignation devant le tribunal ?",
        "Quelle est la clause résolutoire du bail commercial ?",
        "Combien coûte l'appartement dans le compromis de vente ?",
        "Quel est l'objet social de la SARL ?",
        "Quelles sont les pénalités en cas de retard de paiement ?",
        "Quelle est la répartition des parts sociales ?"
    ]

if __name__ == "__main__":
    create_sample_legal_documents()
    print("Demo legal documents created successfully!")
    print("\nSample queries to test:")
    for query in get_demo_queries():
        print(f"- {query}")