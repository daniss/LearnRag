#!/usr/bin/env python3
"""
Test script for French Legal RAG Demo
"""

from simple_demo import SimpleFrenchLegalRAG, create_sales_report

def test_queries():
    """Test the demo with sample queries"""
    print("🧪 TESTING FRENCH LEGAL RAG DEMO")
    print("=" * 50)
    
    rag = SimpleFrenchLegalRAG()
    
    print(f"📁 Documents loaded: {len(rag.demo_documents)}")
    
    # Test queries
    test_queries = [
        "Quelles sont les obligations du bailleur ?",
        "Période d'essai contrat travail",
        "Montant réclamé jugement", 
        "Associés SARL Innovation Tech",
        "Clause résolutoire bail commercial",
        "Question générale sur les contrats"  # Should trigger fallback
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n🔍 TEST {i}: {query}")
        print("-" * 40)
        
        result = rag.analyze_query(query)
        
        if result["success"]:
            print(f"✅ Confiance: {result['confidence']*100:.0f}%")
            print(f"⏱️  Temps: {result['processing_time']}")
            print(f"📄 Documents: {result['documents_analyzed']}")
            print("\n📝 Réponse:")
            print(result["answer"][:200] + "..." if len(result["answer"]) > 200 else result["answer"])
            print(f"\n📚 Sources: {', '.join(result['sources'])}")
        else:
            print(f"❌ Échec: {result.get('error', 'Erreur inconnue')}")
    
    print("\n" + "=" * 50)
    print("🎉 Tests terminés avec succès!")
    
    # Generate sales report
    print("\n📊 Génération du rapport de vente...")
    create_sales_report()

if __name__ == "__main__":
    test_queries()