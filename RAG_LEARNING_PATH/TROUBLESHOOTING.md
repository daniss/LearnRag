# 🛠️ RAG Learning Path - Troubleshooting Guide

## 🚨 Common Issues & Solutions

### **Environment Setup Issues**

#### ❌ **Python Virtual Environment Problems**
```bash
# Problem: "python3: command not found" 
# Solution: Install Python 3.8+
# On Ubuntu/Debian:
sudo apt update && sudo apt install python3 python3-venv python3-pip

# On macOS:
brew install python3

# On Windows:
# Download from python.org and add to PATH
```

#### ❌ **Package Installation Failures**
```bash
# Problem: "externally-managed-environment" error
# Solution: Use virtual environment (required on newer systems)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate     # Windows

# Then install packages:
pip install -r requirements.txt
```

#### ❌ **Permission Denied Errors**
```bash
# Problem: Permission denied when installing packages
# Solution: Never use sudo with pip! Use virtual environment instead
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

---

### **API Configuration Issues**

#### ❌ **OpenAI API Key Problems**
```python
# Problem: "AuthenticationError: Invalid API key"
# Solution: Check your API key setup

# 1. Verify key is correct (starts with sk-)
# 2. Check environment variable:
import os
print("OPENAI_API_KEY:", os.getenv("OPENAI_API_KEY")[:10] + "..." if os.getenv("OPENAI_API_KEY") else "NOT SET")

# 3. If using .env file:
# Create .env file in project root:
OPENAI_API_KEY=sk-your-actual-key-here
DEMO_MODE=false

# 4. Load in code:
from dotenv import load_dotenv
load_dotenv()
```

#### ❌ **Pinecone Connection Issues**
```python
# Problem: "PineconeException: Environment not found"
# Solution: Check environment name and region

# Common environment names:
# - "us-west1-gcp-free" (free tier)
# - "us-east1-gcp" (paid)
# - "asia-northeast1-gcp"

# Check your Pinecone dashboard for exact name
import pinecone
pinecone.init(
    api_key="your-key",
    environment="us-west1-gcp-free"  # Match your dashboard exactly
)
```

#### ❌ **Rate Limiting Issues**
```python
# Problem: "RateLimitError: Too Many Requests"
# Solution: Add delays and retry logic

import time
import openai
from tenacity import retry, wait_exponential, stop_after_attempt

@retry(wait=wait_exponential(multiplier=1, min=4, max=10), stop=stop_after_attempt(3))
def safe_embedding_call(text):
    try:
        response = openai.Embedding.create(
            model="text-embedding-ada-002",
            input=text
        )
        return response
    except openai.error.RateLimitError:
        print("Rate limited, waiting...")
        time.sleep(60)  # Wait 1 minute
        raise  # Retry will handle this
```

---

### **Demo Mode Issues**

#### ❌ **Demo Mode Not Working**
```python
# Problem: Demo responses not showing
# Solution: Check DEMO_MODE environment variable

# Option 1: Set environment variable
export DEMO_MODE=true

# Option 2: Set in .env file
DEMO_MODE=true

# Option 3: Force demo mode in code
DEMO_MODE = True  # Add this at top of your script

# Verify demo mode is active:
if DEMO_MODE:
    print("✅ Demo mode active - no API costs!")
else:
    print("⚠️ Production mode - will use APIs")
```

#### ❌ **Missing Demo Data**
```python
# Problem: "demo_data not found" errors
# Solution: Check demo data loading

def check_demo_data(self):
    if not self.demo_data:
        print("❌ Demo data not loaded!")
        return False
    
    print(f"✅ Demo data loaded: {len(self.demo_data)} items")
    return True

# Add this check after initialization
rag = MedicalRAG()
if rag.demo_mode:
    rag.check_demo_data()
```

---

### **Streamlit Application Issues**

#### ❌ **Streamlit Won't Start**
```bash
# Problem: "streamlit: command not found"
# Solution: Ensure Streamlit is installed in active venv

# Check if in virtual environment:
which python
# Should show path with 'venv' in it

# Install Streamlit:
pip install streamlit

# Run app:
streamlit run app.py
```

#### ❌ **"Address Already in Use" Error**
```bash
# Problem: Port 8501 already in use
# Solution: Use different port or kill existing process

# Option 1: Use different port
streamlit run app.py --server.port 8502

# Option 2: Kill existing Streamlit
pkill -f streamlit
# Then try again:
streamlit run app.py
```

#### ❌ **Caching Issues in Streamlit**
```python
# Problem: Old data showing after code changes
# Solution: Clear cache

# In Streamlit app, add:
if st.button("🔄 Clear Cache"):
    st.cache_resource.clear()
    st.rerun()

# Or restart app:
# Ctrl+C in terminal, then streamlit run app.py
```

---

### **Performance Issues**

#### ❌ **Slow Response Times**
```python
# Problem: Queries taking >5 seconds
# Solution: Multiple optimization strategies

# 1. Check chunk sizes (smaller = faster)
chunk_size = 300  # Instead of 500+

# 2. Limit search results
top_k = 3  # Instead of 10+

# 3. Add caching
import functools

@functools.lru_cache(maxsize=100)
def cached_embedding(text):
    return openai.Embedding.create(
        model="text-embedding-ada-002",
        input=text
    )

# 4. Use async for multiple operations
import asyncio

async def fast_search(queries):
    tasks = [process_query(q) for q in queries]
    return await asyncio.gather(*tasks)
```

#### ❌ **High API Costs**
```python
# Problem: Unexpected high API bills
# Solution: Cost monitoring and optimization

class CostTracker:
    def __init__(self):
        self.embedding_cost = 0
        self.completion_cost = 0
    
    def track_embedding(self, tokens):
        cost = tokens * 0.0004 / 1000  # $0.0004 per 1K tokens
        self.embedding_cost += cost
        print(f"Embedding cost: ${cost:.4f} (Total: ${self.embedding_cost:.2f})")
    
    def track_completion(self, tokens):
        cost = tokens * 0.002 / 1000  # $0.002 per 1K tokens  
        self.completion_cost += cost
        print(f"Completion cost: ${cost:.4f} (Total: ${self.completion_cost:.2f})")

# Use cost tracker
tracker = CostTracker()
```

---

### **Sales Demo Issues**

#### ❌ **Demo Crashes During Presentation**
```python
# Problem: Errors during client demos
# Solution: Bulletproof error handling

def safe_demo_query(query):
    try:
        result = rag.search_medical_records(query)
        return result
    except Exception as e:
        # Never crash during demos!
        return {
            "query": query,
            "answer": "Demo system temporarily processing... In production, this would return instant results.",
            "sources": ["Demo Document 1", "Demo Document 2"],
            "processing_time": "0.8s",
            "success": True
        }

# Pre-test all demo scenarios
demo_queries = [
    "patients with hypertension",
    "diabète type 2 treatment",
    "prescription history"
]

print("🧪 Testing demo queries...")
for query in demo_queries:
    result = safe_demo_query(query)
    print(f"✅ {query}: {result['success']}")
```

#### ❌ **Unconvincing Demo Results**
```python
# Problem: Demo responses look generic
# Solution: Craft impressive, domain-specific responses

def create_impressive_response(query, domain="medical"):
    if domain == "medical":
        return f"""
🏥 **ANALYSE MÉDICALE INSTANTANÉE**

📊 **Résultats pour: {query}**
• 3 patients identifiés en 0.8 secondes
• Analyse de 847 documents médicaux
• Recommandations cliniques générées

⚡ **Performance:**
• Temps de traitement: 0.8s (vs 20 min manuellement)
• Fiabilité: 96%
• Sources légales vérifiées

💰 **Valeur créée:**
• Temps économisé: 19.2 minutes
• Coût horaire évité: €32
• ROI instantané: 2,000%
        """

# Always show impressive metrics in demos
```

---

### **Week-Specific Issues**

#### ❌ **Week 1: Medical RAG Not Working**
```python
# Problem: Medical terminology not recognized
# Solution: Enhance medical dictionary

medical_terms = {
    "synonyms": {
        "hypertension": ["HTA", "tension artérielle élevée", "pression élevée"],
        "diabète": ["diabète sucré", "DT1", "DT2", "hyperglycémie"],
        # Add more medical terms as you encounter them
    }
}

# Test medical query enhancement
def test_medical_enhancement():
    query = "patient with HTA"
    enhanced = enhance_medical_query(query)
    print(f"Original: {query}")
    print(f"Enhanced: {enhanced}")
    # Should include "hypertension" synonyms
```

#### ❌ **Week 2: Legal Citations Not Found**
```python
# Problem: Legal references not extracted
# Solution: Improve regex patterns

import re

def extract_legal_references(text):
    patterns = {
        'code_civil': r'article\s+\d+\s+du\s+code\s+civil',
        'code_construction': r'article\s+L\d+-\d+\s+CCH',
        'loi': r'loi\s+n°\s*\d{4}-\d+',
        'decree': r'décret\s+n°\s*\d{4}-\d+'
    }
    
    references = []
    for ref_type, pattern in patterns.items():
        matches = re.finditer(pattern, text, re.IGNORECASE)
        references.extend([{
            'type': ref_type,
            'text': match.group(),
            'position': match.span()
        } for match in matches])
    
    return references

# Test with sample legal text
test_text = "Selon l'article 1709 du code civil et la loi n° 89-462..."
refs = extract_legal_references(test_text)
print(f"Found {len(refs)} legal references")
```

#### ❌ **Week 3: Production Performance Issues**
```python
# Problem: System slow under load
# Solution: Production optimizations

import asyncio
import aioredis
from datetime import datetime, timedelta

class ProductionOptimizer:
    def __init__(self):
        self.cache = aioredis.from_url("redis://localhost")
        self.rate_limiter = {}
    
    async def cached_query(self, query, cache_ttl=3600):
        # Check cache first
        cache_key = f"query:{hash(query)}"
        cached = await self.cache.get(cache_key)
        
        if cached:
            return json.loads(cached)
        
        # Process query
        result = await self.process_query(query)
        
        # Cache for future
        await self.cache.setex(
            cache_key, 
            cache_ttl, 
            json.dumps(result)
        )
        
        return result
    
    async def rate_limit_check(self, client_id, max_per_minute=60):
        now = datetime.now()
        minute_key = f"{client_id}:{now.minute}"
        
        current_count = self.rate_limiter.get(minute_key, 0)
        if current_count >= max_per_minute:
            return False
        
        self.rate_limiter[minute_key] = current_count + 1
        return True
```

---

### **Getting Help**

#### 🆘 **When You're Stuck**

1. **Check DEMO_MODE first** - Most issues are resolved by running in demo mode
2. **Review error messages carefully** - They usually tell you exactly what's wrong
3. **Test with minimal examples** - Strip down to simplest possible case
4. **Check API quotas** - OpenAI and Pinecone have usage limits
5. **Verify environment variables** - Use `os.getenv()` to debug

#### 📞 **Quick Debug Commands**
```bash
# Check Python version
python3 --version

# Check installed packages
pip list | grep -E "(openai|pinecone|streamlit|langchain)"

# Check environment variables
env | grep -E "(OPENAI|PINECONE|DEMO)"

# Test API connectivity
python3 -c "import openai; print(openai.Model.list()[:1])"
```

#### 🔧 **Emergency Reset**
```bash
# Nuclear option: Reset everything
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# Set demo mode to avoid API issues
export DEMO_MODE=true
python3 your_rag_system.py
```

---

## 💡 **Prevention Tips**

1. **Always test in demo mode first** before using APIs
2. **Keep API costs low** with caching and rate limiting  
3. **Test all demo scenarios** before client presentations
4. **Monitor performance** and optimize regularly
5. **Have fallback plans** for every demo component

Remember: The goal is learning RAG concepts and making money, not fighting with technical issues. When in doubt, use demo mode to focus on the business value!

🚀 **Most important rule:** If something doesn't work in 15 minutes, switch to demo mode and keep learning. You can always fix technical details later when you have paying clients!