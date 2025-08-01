# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a French RAG (Retrieval-Augmented Generation) system designed to help French law firms with legal document analysis. It includes a complete business-in-a-box solution with demo systems, sales materials, and learning paths for different verticals.

## Architecture

### Core RAG System
- **`rag_utils.py`** - Main RAG engine with FrenchLegalRAG class
  - Uses OpenAI text-embedding-ada-002 for embeddings
  - Pinecone for vector storage  
  - RecursiveCharacterTextSplitter for document chunking (500 chars, 50 overlap)
  - Optimized for French legal terminology

- **`app.py`** - Streamlit demo application
  - Sales-ready interface with French UI
  - Cached RAG system initialization 
  - Mock file objects for demo documents
  - Integrates with config.py for pricing/metrics

- **`simple_demo.py`** - Standalone demo system
  - Works without external APIs for sales presentations
  - Pre-built response database with intelligent keyword matching
  - French legal document analysis simulation

### Demo Data
- **`demo_docs/`** - French legal documents for testing
- **`demo_data.py`** - Structured demo data loader
- **`config.py`** - Centralized configuration (pricing, metrics, document types)

### Sales Materials
- **`sales_package/`** - Complete sales arsenal
  - Email templates, LinkedIn content, pricing sheets
  - Demo scripts with 15-minute close methodology
  - Prospect targeting data

### Learning Paths
- **`RAG_LEARNING_PATH/`** - 3-week structured learning program
  - Week 1: Medical RAG (€8k setup + €2k/month)
  - Week 2: Real Estate RAG (€6k + €1.8k/month)  
  - Week 3: Accounting RAG (€5k + €1.5k/month)

- **`RAG_TEMPLATES/`** - Production-ready templates
  - `quick_start.py` - 50-line RAG template for any vertical
  - `production_patterns.py` - Battle-tested scaling patterns
  - `deployment_guide.md` - 30-minute production deployment

## Common Commands

### Development Setup
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Testing & Demo
```bash
# Test demo system without APIs
python3 test_demo.py

# Run interactive standalone demo
python3 simple_demo.py

# Generate sales materials
python3 sales_materials.py
```

### Application Launch
```bash
# Start Streamlit demo app
streamlit run app.py

# Quick RAG template for different verticals
python3 RAG_TEMPLATES/quick_start.py medical
python3 RAG_TEMPLATES/quick_start.py legal
python3 RAG_TEMPLATES/quick_start.py realestate
python3 RAG_TEMPLATES/quick_start.py accounting
```

### Production Deployment
```bash
# Test production setup
python3 deploy.py

# Docker deployment
docker build -t french-rag .
docker run -p 8501:8501 french-rag
```

## Environment Configuration

### Required Environment Variables
```bash
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
PINECONE_ENVIRONMENT=us-west1-gcp-free
DEMO_MODE=false  # Set to true for API-free demos
```

### Demo Mode
When `DEMO_MODE=true` or APIs unavailable:
- Uses pre-built response database in `simple_demo.py`
- Simulates vector embeddings with hash-based fake embeddings
- Perfect for sales presentations without API costs

## Multi-Vertical System

The codebase supports multiple verticals through:
- Domain-specific demo data in `RAG_TEMPLATES/quick_start.py`
- Vertical-specific implementations in learning path folders
- Configurable pricing tiers in `config.py`
- Market-specific sales materials

### Adding New Verticals
1. Create new demo data in `quick_start.py`
2. Add domain-specific response patterns to `simple_demo.py`
3. Create vertical folder in `RAG_LEARNING_PATH/`
4. Update pricing in `config.py`

## File Processing
- PDF: Uses PyMuPDF (fitz) for text extraction
- TXT: Direct UTF-8 reading
- Chunk size: 500 characters with 50 character overlap
- French language optimization built-in

## Business Logic
- Target market: French law firms (10-50 employees)
- Pricing: €5k-8k setup + €1.5k-2k/month recurring
- Sales cycle: 2-3 weeks with 5% conversion rate
- Revenue target: €40k/month by month 6

## Key Integration Points
- OpenAI API for embeddings and completions
- Pinecone for vector storage and similarity search
- Streamlit for demo interfaces
- LangChain for text processing utilities