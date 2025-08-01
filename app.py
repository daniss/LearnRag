import streamlit as st
import os
from dotenv import load_dotenv
import openai
from typing import List, Dict, Any
import time
from rag_utils import FrenchLegalRAG
from config import DEMO_METRICS, PRICING_TIERS, LEGAL_DOCUMENT_TYPES
import glob

load_dotenv()

st.set_page_config(
    page_title="Assistant Juridique IA - Votre Expert Légal Instantané",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_resource
def initialize_rag_system():
    """Initialize RAG system (cached for performance)"""
    try:
        rag = FrenchLegalRAG()
        return rag
    except Exception as e:
        st.error(f"⚠️ Erreur d'initialisation du système RAG: {str(e)}")
        st.info("💡 Mode démo activé - les réponses seront simulées")
        return None

def load_demo_documents():
    """Load demo documents for testing"""
    demo_files = glob.glob("/root/LearnRag/demo_docs/*.txt")
    demo_file_objects = []
    
    for file_path in demo_files:
        class MockFile:
            def __init__(self, path):
                self.name = os.path.basename(path)
                self.type = "text/plain"
                self._content = None
                self._path = path
            
            def read(self):
                if self._content is None:
                    with open(self._path, 'r', encoding='utf-8') as f:
                        self._content = f.read().encode('utf-8')
                return self._content
        
        demo_file_objects.append(MockFile(file_path))
    
    return demo_file_objects

def demo_response(question: str, num_files: int):
    """Generate a demo response for showcase purposes"""
    time.sleep(1)  # Simulate processing
    
    st.success("✅ Analyse terminée (Mode Démo)")
    st.write("**🎯 Réponse:**")
    
    # Intelligent demo responses based on keywords
    question_lower = question.lower()
    
    if "obligation" in question_lower and "bailleur" in question_lower:
        response = """
**Obligations principales du bailleur selon le contrat de bail commercial :**

1. **Délivrance des locaux** - Livrer les locaux en bon état de réparations locatives
2. **Jouissance paisible** - Assurer la jouissance paisible des lieux loués
3. **Grosses réparations** - Effectuer les grosses réparations selon l'article 606 du Code civil
4. **Entretien des parties communes** - Maintenir les parties communes en bon état

Ces obligations sont détaillées dans l'Article 4 du contrat analysé.
"""
    elif "période" in question_lower and "essai" in question_lower:
        response = """
**Période d'essai dans le contrat de travail :**

- **Durée :** 4 mois renouvelable une fois
- **Statut :** Contrat à Durée Indéterminée (CDI)
- **Poste :** Développeuse Senior

La période d'essai est conforme à la durée légale pour un cadre (Article 6 du contrat).
"""
    elif "montant" in question_lower or "réclam" in question_lower:
        response = """
**Montants réclamés dans le jugement du Tribunal de Commerce :**

- **Principal :** 45 000 euros (factures impayées)
- **Intérêts légaux :** À compter de l'échéance de chaque facture  
- **Indemnité forfaitaire :** 200 euros (5 factures × 40 euros)
- **Article 700 CPC :** 1 500 euros
- **Total réclamé :** Environ 46 700 euros + intérêts

Jugement rendu le 15 novembre 2023 par le Tribunal de Commerce de Lyon.
"""
    else:
        response = f"""
Basé sur l'analyse de vos {num_files} documents juridiques, voici ma réponse à votre question :

"{question}"

**Analyse effectuée sur :**
• Contrats commerciaux et de travail
• Décisions de justice  
• Statuts de société
• Procédures civiles

**Méthodologie :** Recherche sémantique + analyse contextuelle française

*Note : Ceci est une démonstration. L'analyse complète nécessite la configuration des clés API.*
"""
    
    st.info(response)
    
    # Demo sources
    st.write("**📚 Sources citées :**")
    demo_sources = [
        {"name": "contrat_bail_commercial.txt", "score": 0.95, "excerpt": "Article 4 - Obligations du bailleur..."},
        {"name": "contrat_travail_cdi.txt", "score": 0.87, "excerpt": "Article 6 - Période d'essai fixée à 4 mois..."},
        {"name": "jugement_tribunal_commerce.txt", "score": 0.92, "excerpt": "Condamne à payer 45 000 euros..."}
    ]
    
    for source in demo_sources[:2]:  # Show top 2 sources
        with st.expander(f"📄 {source['name']} (Score: {source['score']})"):
            st.write(source["excerpt"])

def main():
    # Initialize RAG system
    rag_system = initialize_rag_system()
    
    # Header
    st.title("⚖️ Assistant Juridique IA")
    st.subheader("Transformez 3 heures de recherche en 30 secondes")
    
    # Demo mode toggle
    demo_mode = st.toggle("🎯 Mode Démo (utilisez nos documents de test)", value=True)
    
    # Sidebar for file upload
    with st.sidebar:
        st.header("📁 Documents Juridiques")
        
        if demo_mode:
            # Load demo documents
            demo_files = load_demo_documents()
            st.info(f"🎯 Mode démo: {len(demo_files)} documents chargés")
            uploaded_files = demo_files
            
            st.write("**Documents de démonstration:**")
            for file in demo_files:
                st.write(f"📄 {file.name}")
                
        else:
            uploaded_files = st.file_uploader(
                "Glissez-déposez vos documents",
                type=['pdf', 'txt', 'docx'],
                accept_multiple_files=True,
                help="Formats supportés: PDF, TXT, DOCX"
            )
            
            if uploaded_files:
                st.success(f"✅ {len(uploaded_files)} documents chargés")
                for file in uploaded_files:
                    st.write(f"📄 {file.name}")
        
        # Document types info
        st.subheader("📋 Types de documents supportés")
        for doc_type, description in LEGAL_DOCUMENT_TYPES.items():
            st.write(f"• {description}")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Posez vos questions juridiques")
        
        # Sample questions for demo
        st.subheader("🎯 Exemples de questions")
        sample_questions = [
            "Quelles sont les obligations du bailleur dans un contrat de bail ?",
            "Résumez les clauses de résiliation de ce contrat",
            "Trouvez les jurisprudences similaires à cette affaire",
            "Quels sont les risques juridiques dans ce document ?",
            "Comparez les termes de ces contrats de travail"
        ]
        
        for i, question in enumerate(sample_questions):
            if st.button(f"📝 {question}", key=f"sample_{i}"):
                st.session_state.current_question = question
        
        # Chat interface
        st.subheader("💭 Votre Question")
        user_question = st.text_input(
            "Tapez votre question ici...",
            value=st.session_state.get('current_question', ''),
            placeholder="Ex: Quelles sont les clauses résolutoires dans ce bail commercial ?"
        )
        
        if st.button("🔍 Analyser", type="primary"):
            if user_question:
                if not uploaded_files:
                    st.warning("⚠️ Veuillez d'abord charger vos documents dans la barre latérale")
                else:
                    with st.spinner("🔍 Recherche en cours..."):
                        if rag_system:
                            # Real RAG processing
                            try:
                                result = rag_system.analyze_legal_document(user_question, uploaded_files)
                                
                                if "error" in result:
                                    st.error(f"❌ {result['error']}")
                                else:
                                    st.success("✅ Analyse terminée")
                                    
                                    # Display answer
                                    st.write("**🎯 Réponse:**")
                                    st.info(result["answer"])
                                    
                                    # Display sources
                                    if result.get("sources"):
                                        st.write("**📚 Sources citées:**")
                                        for i, source in enumerate(result["sources"], 1):
                                            with st.expander(f"📄 {source['document']} (Score: {source['relevance_score']})"):
                                                st.write(source["excerpt"])
                                    
                                    # Display processing stats
                                    st.write("**📊 Statistiques de traitement:**")
                                    col_stat1, col_stat2 = st.columns(2)
                                    with col_stat1:
                                        st.metric("Documents traités", result.get("documents_processed", 0))
                                    with col_stat2:
                                        st.metric("Fichiers analysés", result.get("total_files", 0))
                                        
                            except Exception as e:
                                st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                                # Fallback to demo mode
                                st.info("🎯 Basculement en mode démonstration")
                                demo_response(user_question, len(uploaded_files))
                        else:
                            # Demo mode response
                            demo_response(user_question, len(uploaded_files))
            else:
                st.error("❌ Veuillez saisir une question")
    
    with col2:
        st.header("📊 Statistiques en Temps Réel")
        
        # Real-time metrics
        if uploaded_files:
            st.metric("Documents chargés", len(uploaded_files), f"+{len(uploaded_files)}")
            st.metric("Temps par recherche", DEMO_METRICS["time_saved_per_search"], "-85%")
        else:
            st.metric("Documents analysés", "0", "0")
            st.metric("Temps économisé", "0h", "0h")
        
        st.metric("Taux de précision", DEMO_METRICS["accuracy_rate"], "+5%")
        st.metric("Documents/seconde", DEMO_METRICS["documents_per_second"], "+50")
        
        st.header("🎯 Avantages Concurrentiels")
        st.success("✅ Réponses en français juridique")
        st.success("✅ Sources avec citations précises")
        st.success("✅ 100% conforme RGPD")
        st.success("✅ Données privées locales")
        st.success("✅ Support expert français")
        
        st.header("💰 ROI Immédiat")
        annual_savings = DEMO_METRICS["annual_savings"]
        st.info(f"""
        **Économies garanties :**
        - 🕐 15h/semaine économisées
        - 💰 {annual_savings}/an en productivité  
        - 📈 ROI: 300% dès la première année
        - ⚡ Retour sur investissement: 3 mois
        """)
        
        # Pricing quick view
        st.header("💸 Tarification Transparente")
        
        pricing_tab1, pricing_tab2 = st.tabs(["🏃‍♂️ Starter", "🚀 Pro"])
        
        with pricing_tab1:
            starter = PRICING_TIERS["starter"]
            st.write(f"**Setup:** €{starter['setup_fee']:,}")
            st.write(f"**Mensuel:** €{starter['monthly_fee']:,}")
            st.write(f"**Max docs:** {starter['max_documents']:,}")
            
        with pricing_tab2:
            pro = PRICING_TIERS["professional"]
            st.write(f"**Setup:** €{pro['setup_fee']:,}")
            st.write(f"**Mensuel:** €{pro['monthly_fee']:,}")
            st.write(f"**Max docs:** {pro['max_documents']:,}")
        
        # Call to action
        st.header("🚀 Prêt à Économiser 15h/Semaine ?")
        
        col_cta1, col_cta2 = st.columns(2)
        with col_cta1:
            if st.button("📞 Démo Gratuite", type="primary"):
                st.balloons()
                st.success("🎉 Calendrier ouvert !")
                st.info("📧 contact@assistant-juridique-ia.fr")
                
        with col_cta2:
            if st.button("💬 WhatsApp", type="secondary"):
                st.info("📱 +33 6 12 34 56 78")
        
        # Social proof
        st.header("🏆 Ils Nous Font Confiance")
        st.write("🏢 **Cabinet Martin & Associés** - 'Gain de temps incroyable'")
        st.write("⚖️ **SCP Dupont-Legal** - 'Précision remarquable'")  
        st.write("🏛️ **Avocats & Partners** - 'ROI en 2 mois'")
        
        # Urgency element
        st.error("⏰ **Offre limitée:** Première installation à -50% ce mois-ci !")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🔒 Vos données restent privées • Traitement local • Conforme RGPD</p>
        <p>Développé spécialement pour les cabinets d'avocats français</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()