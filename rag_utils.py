import os
import pinecone
import openai
from typing import List, Dict, Any, Tuple
import pandas as pd
import numpy as np
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
import fitz  # PyMuPDF
import json
from dotenv import load_dotenv

load_dotenv()

class FrenchLegalRAG:
    """
    RAG system optimized for French legal documents
    """
    
    def __init__(self):
        self.openai_client = None
        self.pinecone_index = None
        self.embeddings = None
        self.text_splitter = None
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize all RAG components"""
        try:
            # OpenAI setup
            openai.api_key = os.getenv("OPENAI_API_KEY")
            self.embeddings = OpenAIEmbeddings(
                model="text-embedding-ada-002",
                openai_api_key=os.getenv("OPENAI_API_KEY")
            )
            
            # Pinecone setup
            pinecone.init(
                api_key=os.getenv("PINECONE_API_KEY"),
                environment=os.getenv("PINECONE_ENVIRONMENT")
            )
            
            # Text splitter optimized for legal documents
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,  # Smaller chunks for legal precision
                chunk_overlap=50,
                separators=["\n\n", "\n", ". ", " ", ""]
            )
            
            print("✅ RAG components initialized successfully")
            
        except Exception as e:
            print(f"❌ Error initializing RAG: {str(e)}")
            raise
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extract text from PDF file"""
        try:
            doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            return text
        except Exception as e:
            print(f"Error extracting PDF text: {str(e)}")
            return ""
    
    def process_documents(self, uploaded_files) -> List[Dict]:
        """Process uploaded documents and create embeddings"""
        documents = []
        
        for file in uploaded_files:
            try:
                # Extract text based on file type
                if file.type == "application/pdf":
                    text = self.extract_text_from_pdf(file)
                elif file.type == "text/plain":
                    text = str(file.read(), "utf-8")
                else:
                    continue  # Skip unsupported files
                
                # Split text into chunks
                chunks = self.text_splitter.split_text(text)
                
                # Create document objects
                for i, chunk in enumerate(chunks):
                    doc = {
                        "id": f"{file.name}_{i}",
                        "content": chunk,
                        "source": file.name,
                        "chunk_index": i,
                        "metadata": {
                            "filename": file.name,
                            "chunk_size": len(chunk),
                            "file_type": file.type
                        }
                    }
                    documents.append(doc)
                    
            except Exception as e:
                print(f"Error processing {file.name}: {str(e)}")
                continue
        
        return documents
    
    def store_embeddings(self, documents: List[Dict], index_name: str = "french-legal-docs"):
        """Store document embeddings in Pinecone"""
        try:
            # Create index if it doesn't exist
            if index_name not in pinecone.list_indexes():
                pinecone.create_index(
                    name=index_name,
                    dimension=1536,  # OpenAI ada-002 dimension
                    metric="cosine"
                )
            
            # Connect to index
            self.pinecone_index = pinecone.Index(index_name)
            
            # Create embeddings and upsert
            vectors_to_upsert = []
            
            for doc in documents:
                # Get embedding
                embedding = self.embeddings.embed_query(doc["content"])
                
                # Prepare vector for upsert
                vector = {
                    "id": doc["id"],
                    "values": embedding,
                    "metadata": {
                        "content": doc["content"],
                        "source": doc["source"],
                        "chunk_index": doc["chunk_index"],
                        **doc["metadata"]
                    }
                }
                vectors_to_upsert.append(vector)
                
                # Batch upsert every 100 vectors
                if len(vectors_to_upsert) >= 100:
                    self.pinecone_index.upsert(vectors_to_upsert)
                    vectors_to_upsert = []
            
            # Upsert remaining vectors
            if vectors_to_upsert:
                self.pinecone_index.upsert(vectors_to_upsert)
            
            print(f"✅ Stored {len(documents)} document chunks in Pinecone")
            return True
            
        except Exception as e:
            print(f"❌ Error storing embeddings: {str(e)}")
            return False
    
    def search_documents(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search for relevant documents using semantic similarity"""
        try:
            if not self.pinecone_index:
                return []
            
            # Get query embedding
            query_embedding = self.embeddings.embed_query(query)
            
            # Search in Pinecone
            search_results = self.pinecone_index.query(
                vector=query_embedding,
                top_k=top_k,
                include_metadata=True
            )
            
            # Format results
            relevant_docs = []
            for match in search_results.matches:
                doc = {
                    "content": match.metadata.get("content", ""),
                    "source": match.metadata.get("source", ""),
                    "score": match.score,
                    "chunk_index": match.metadata.get("chunk_index", 0)
                }
                relevant_docs.append(doc)
            
            return relevant_docs
            
        except Exception as e:
            print(f"❌ Error searching documents: {str(e)}")
            return []
    
    def generate_answer(self, query: str, relevant_docs: List[Dict]) -> str:
        """Generate answer using OpenAI with retrieved context"""
        try:
            # Prepare context from relevant documents
            context = "\n\n".join([
                f"Document: {doc['source']}\nContenu: {doc['content']}"
                for doc in relevant_docs
            ])
            
            # French legal prompt template
            prompt = f"""
Tu es un assistant juridique expert spécialisé dans le droit français. 
Réponds à la question en te basant UNIQUEMENT sur les documents fournis.

CONTEXTE:
{context}

QUESTION: {query}

INSTRUCTIONS:
1. Réponds en français professionnel
2. Cite tes sources précisément (nom du document)
3. Si l'information n'est pas dans les documents, dis-le clairement
4. Structure ta réponse avec des puces si nécessaire
5. Reste factuel et précis

RÉPONSE:
"""
            
            # Call OpenAI
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,  # Low temperature for factual responses
                max_tokens=800
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"❌ Error generating answer: {str(e)}")
            return "Désolé, une erreur s'est produite lors de la génération de la réponse."
    
    def analyze_legal_document(self, query: str, uploaded_files) -> Dict[str, Any]:
        """Complete RAG pipeline for legal document analysis"""
        try:
            # Process documents
            documents = self.process_documents(uploaded_files)
            if not documents:
                return {"error": "Aucun document traitable trouvé"}
            
            # Store embeddings
            success = self.store_embeddings(documents)
            if not success:
                return {"error": "Erreur lors du stockage des embeddings"}
            
            # Search relevant documents
            relevant_docs = self.search_documents(query)
            if not relevant_docs:
                return {"error": "Aucun document pertinent trouvé"}
            
            # Generate answer
            answer = self.generate_answer(query, relevant_docs)
            
            # Prepare response
            response = {
                "answer": answer,
                "sources": [
                    {
                        "document": doc["source"],
                        "relevance_score": round(doc["score"], 3),
                        "excerpt": doc["content"][:200] + "..."
                    }
                    for doc in relevant_docs[:3]  # Top 3 sources
                ],
                "documents_processed": len(documents),
                "total_files": len(uploaded_files)
            }
            
            return response
            
        except Exception as e:
            print(f"❌ Error in RAG pipeline: {str(e)}")
            return {"error": f"Erreur d'analyse: {str(e)}"}

# French legal document templates for demo
DEMO_LEGAL_QUERIES = [
    "Quelles sont les obligations du bailleur dans un contrat de bail commercial ?",
    "Identifiez les clauses résolutoires dans ce contrat",
    "Quels sont les délais de préavis pour la résiliation ?",
    "Analysez les risques juridiques de ce document",
    "Trouvez les références aux articles du Code civil"
]

DEMO_RESPONSES = {
    "obligations bailleur": """
**Obligations principales du bailleur:**
• Délivrance du bien en bon état
• Garantie de jouissance paisible  
• Entretien et réparations nécessaires
• Respect des normes de sécurité

**Sources:** Contrat_bail_commercial.pdf, Article 1719 Code civil
""",
    "clauses résolutoires": """
**Clauses résolutoires identifiées:**
• Non-paiement des loyers (délai de grâce: 30 jours)
• Défaut d'assurance du locataire
• Changement d'activité sans autorisation
• Sous-location interdite non respectée

**Source:** Section 4.2 du contrat analysé
"""
}