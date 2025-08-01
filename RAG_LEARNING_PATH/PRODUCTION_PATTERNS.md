# 🏭 Production RAG Patterns - Error Handling & Deployment Automation

## 🎯 Overview

This guide contains battle-tested patterns for deploying RAG systems to production. These patterns are extracted from successful €40k+/month RAG implementations and focus on reliability, scalability, and maintainability.

---

## 🛡️ Error Handling Patterns

### **1. Circuit Breaker Pattern**

```python
import time
from enum import Enum
from typing import Optional, Callable, Any

class CircuitState(Enum):
    CLOSED = "closed"      # Normal operation
    OPEN = "open"          # Failing, reject requests
    HALF_OPEN = "half_open" # Testing recovery

class CircuitBreaker:
    """Prevent cascading failures in RAG systems"""
    
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = None
        self.state = CircuitState.CLOSED
    
    def call(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection"""
        
        if self.state == CircuitState.OPEN:
            if self._should_attempt_reset():
                self.state = CircuitState.HALF_OPEN
            else:
                raise Exception("Circuit breaker is OPEN - service unavailable")
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
            
        except Exception as e:
            self._on_failure()
            raise e
    
    def _on_success(self):
        """Reset circuit breaker on successful call"""
        self.failure_count = 0
        self.state = CircuitState.CLOSED
    
    def _on_failure(self):
        """Handle failure and update circuit state"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self) -> bool:
        """Check if enough time has passed to attempt recovery"""
        return (time.time() - self.last_failure_time) >= self.recovery_timeout

# Usage in RAG system
class ProductionRAG:
    def __init__(self):
        self.openai_circuit = CircuitBreaker(failure_threshold=3, recovery_timeout=30)
        self.pinecone_circuit = CircuitBreaker(failure_threshold=5, recovery_timeout=60)
    
    async def search_with_protection(self, query: str):
        """Search with circuit breaker protection"""
        try:
            # Protected OpenAI call
            embedding = self.openai_circuit.call(
                self._generate_embedding, query
            )
            
            # Protected Pinecone call
            results = self.pinecone_circuit.call(
                self._vector_search, embedding
            )
            
            return results
            
        except Exception as e:
            # Fallback to cached responses or error message
            return self._fallback_response(query, str(e))
    
    def _fallback_response(self, query: str, error: str):
        """Provide graceful degradation"""
        return {
            "query": query,
            "answer": "Service temporairement indisponible. Nos équipes travaillent à résoudre le problème.",
            "sources": ["Cache système"],
            "error": error,
            "fallback": True
        }
```

### **2. Retry Pattern with Exponential Backoff**

```python
import asyncio
import random
from functools import wraps
from typing import Type, Tuple

def async_retry(
    max_attempts: int = 3,
    backoff_base: float = 1.0,
    backoff_factor: float = 2.0,
    jitter: bool = True,
    exceptions: Tuple[Type[Exception], ...] = (Exception,)
):
    """Async retry decorator with exponential backoff"""
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return await func(*args, **kwargs)
                    
                except exceptions as e:
                    last_exception = e
                    
                    if attempt == max_attempts - 1:
                        # Last attempt failed, raise the exception
                        raise e
                    
                    # Calculate backoff time
                    backoff_time = backoff_base * (backoff_factor ** attempt)
                    
                    # Add jitter to prevent thundering herd
                    if jitter:
                        backoff_time *= (0.5 + random.random() * 0.5)
                    
                    print(f"Attempt {attempt + 1} failed: {e}. Retrying in {backoff_time:.2f}s...")
                    await asyncio.sleep(backoff_time)
            
            raise last_exception
        
        return wrapper
    return decorator

# Usage in RAG operations
class RobustRAG:
    @async_retry(max_attempts=3, backoff_base=1.0, exceptions=(openai.error.RateLimitError,))
    async def generate_embedding(self, text: str):
        """Generate embedding with automatic retry"""
        import openai
        response = await openai.Embedding.acreate(
            model="text-embedding-ada-002",
            input=text
        )
        return response['data'][0]['embedding']
    
    @async_retry(max_attempts=5, backoff_base=0.5, exceptions=(ConnectionError, TimeoutError))
    async def vector_search(self, embedding: list, top_k: int = 5):
        """Vector search with automatic retry"""
        results = await self.pinecone_index.query(
            vector=embedding,
            top_k=top_k,
            include_metadata=True
        )
        return results
```

### **3. Graceful Degradation Pattern**

```python
from typing import Dict, Any, Optional
import logging

class GracefulRAG:
    """RAG system with multiple fallback layers"""
    
    def __init__(self):
        self.cache = {}
        self.fallback_responses = self.load_fallback_responses()
        self.logger = logging.getLogger(__name__)
    
    async def query(self, question: str, client_id: str) -> Dict[str, Any]:
        """Multi-layered query processing with graceful degradation"""
        
        # Layer 1: Try full RAG pipeline
        try:
            return await self._full_rag_pipeline(question, client_id)
        except Exception as e:
            self.logger.warning(f"Full RAG pipeline failed: {e}")
        
        # Layer 2: Try cached results
        try:
            cached_result = self._get_cached_response(question)
            if cached_result:
                cached_result["source"] = "cache"
                cached_result["degraded"] = True
                return cached_result
        except Exception as e:
            self.logger.warning(f"Cache lookup failed: {e}")
        
        # Layer 3: Try keyword matching with fallback responses
        try:
            return self._keyword_fallback(question)
        except Exception as e:
            self.logger.warning(f"Keyword fallback failed: {e}")
        
        # Layer 4: Generic error response (always works)
        return self._generic_error_response(question)
    
    def _keyword_fallback(self, question: str) -> Dict[str, Any]:
        """Simple keyword matching for basic queries"""
        question_lower = question.lower()
        
        # Check for common keywords
        for keywords, response in self.fallback_responses.items():
            if any(keyword in question_lower for keyword in keywords.split("|")):
                return {
                    "query": question,
                    "answer": response["answer"],
                    "sources": response["sources"],
                    "confidence": 0.7,
                    "source": "keyword_fallback",
                    "degraded": True
                }
        
        # No keyword match found
        raise Exception("No keyword match found")
    
    def _generic_error_response(self, question: str) -> Dict[str, Any]:
        """Last resort response that never fails"""
        return {
            "query": question,
            "answer": """
            Je rencontre actuellement des difficultés techniques pour traiter votre demande.
            
            Nos équipes travaillent à résoudre le problème dans les plus brefs délais.
            
            En attendant, vous pouvez :
            • Reformuler votre question plus simplement
            • Contacter notre support technique
            • Consulter notre documentation en ligne
            
            Nous nous excusons pour ce désagrément temporaire.
            """,
            "sources": ["Système"],
            "confidence": 1.0,
            "source": "error_handler",
            "degraded": True,
            "support_contact": "support@votreentreprise.fr"
        }
    
    def load_fallback_responses(self) -> Dict[str, Dict]:
        """Load pre-computed responses for common queries"""
        return {
            "tva|taxe|vat": {
                "answer": "Le taux normal de TVA en France est de 20%. Pour des questions spécifiques, consultez le Code Général des Impôts.",
                "sources": ["CGI Art. 278"]
            },
            "prix|tarif|coût": {
                "answer": "Nos tarifs sont personnalisés selon vos besoins. Contactez notre équipe commerciale pour un devis gratuit.",
                "sources": ["Grille tarifaire"]  
            },
            "aide|help|support": {
                "answer": "Notre équipe support est disponible du lundi au vendredi de 9h à 18h. Email: support@exemple.fr",
                "sources": ["Support client"]
            }
        }
```

---

## 🚀 Deployment Automation Patterns

### **1. Blue-Green Deployment with Health Checks**

```python
# deploy.py - Production deployment automation
import os
import time
import requests
import subprocess
from typing import Dict, Any

class BlueGreenDeployer:
    """Zero-downtime deployment for RAG systems"""
    
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.current_env = self._get_current_environment()
        self.target_env = "green" if self.current_env == "blue" else "blue"
    
    def deploy(self, version: str):
        """Execute blue-green deployment"""
        print(f"🚀 Starting deployment of version {version}")
        print(f"   Current: {self.current_env}, Target: {self.target_env}")
        
        try:
            # Step 1: Deploy to target environment
            self._deploy_to_environment(self.target_env, version)
            
            # Step 2: Run health checks
            if not self._health_check(self.target_env):
                raise Exception("Health checks failed")
            
            # Step 3: Run smoke tests
            if not self._smoke_tests(self.target_env):
                raise Exception("Smoke tests failed")
            
            # Step 4: Switch traffic
            self._switch_traffic(self.target_env)
            
            # Step 5: Final verification
            if not self._verify_production_traffic():
                self._rollback()
                raise Exception("Production verification failed")
            
            # Step 6: Cleanup old environment
            self._cleanup_old_environment(self.current_env)
            
            print(f"✅ Deployment successful! Now serving from {self.target_env}")
            
        except Exception as e:
            print(f"❌ Deployment failed: {e}")
            self._rollback()
            raise e
    
    def _deploy_to_environment(self, env: str, version: str):
        """Deploy application to specific environment"""
        print(f"   📦 Deploying version {version} to {env} environment")
        
        # Build Docker image
        subprocess.run([
            "docker", "build", 
            "-t", f"rag-system:{version}-{env}",
            "--build-arg", f"VERSION={version}",
            "."
        ], check=True)
        
        # Stop existing container
        subprocess.run([
            "docker", "stop", f"rag-{env}"
        ], capture_output=True)
        
        # Start new container
        port = self.config["ports"][env]
        subprocess.run([
            "docker", "run", "-d",
            "--name", f"rag-{env}",
            "-p", f"{port}:8000",
            "--env-file", f".env.{env}",
            f"rag-system:{version}-{env}"
        ], check=True)
        
        # Wait for startup
        time.sleep(30)
    
    def _health_check(self, env: str) -> bool:
        """Comprehensive health checks"""
        base_url = self.config["urls"][env]
        
        checks = [
            ("Basic Health", f"{base_url}/health"),
            ("Database", f"{base_url}/health/db"), 
            ("Vector Store", f"{base_url}/health/vector"),
            ("AI APIs", f"{base_url}/health/ai")
        ]
        
        print("   🏥 Running health checks...")
        
        for check_name, url in checks:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    print(f"   ✅ {check_name}: OK")
                else:
                    print(f"   ❌ {check_name}: Failed ({response.status_code})")
                    return False
            except Exception as e:
                print(f"   ❌ {check_name}: Error ({e})")
                return False
        
        return True
    
    def _smoke_tests(self, env: str) -> bool:
        """Critical functionality tests"""
        base_url = self.config["urls"][env]
        
        tests = [
            {
                "name": "Simple Query",
                "endpoint": f"{base_url}/api/query", 
                "payload": {"query": "test query", "client_id": "test"},
                "expected_fields": ["answer", "sources"]
            },
            {
                "name": "Document Processing",
                "endpoint": f"{base_url}/api/documents",
                "payload": {"documents": ["test document"]},
                "expected_fields": ["processed_count"]
            }
        ]
        
        print("   🧪 Running smoke tests...")
        
        for test in tests:
            try:
                response = requests.post(
                    test["endpoint"],
                    json=test["payload"],
                    timeout=30
                )
                
                if response.status_code != 200:
                    print(f"   ❌ {test['name']}: HTTP {response.status_code}")
                    return False
                
                data = response.json()
                for field in test["expected_fields"]:
                    if field not in data:
                        print(f"   ❌ {test['name']}: Missing field {field}")
                        return False
                
                print(f"   ✅ {test['name']}: OK")
                
            except Exception as e:
                print(f"   ❌ {test['name']}: Error ({e})")
                return False
        
        return True
    
    def _switch_traffic(self, target_env: str):
        """Switch load balancer to target environment"""
        print(f"   🔄 Switching traffic to {target_env}")
        
        # Update load balancer configuration
        nginx_config = self._generate_nginx_config(target_env)
        with open("/etc/nginx/sites-available/rag-system", "w") as f:
            f.write(nginx_config)
        
        # Reload nginx
        subprocess.run(["sudo", "nginx", "-s", "reload"], check=True)
        
        time.sleep(5)  # Allow traffic to switch
    
    def _generate_nginx_config(self, env: str) -> str:
        """Generate nginx configuration for environment"""
        port = self.config["ports"][env]
        
        return f"""
server {{
    listen 80;
    server_name {self.config['domain']};
    
    location / {{
        proxy_pass http://localhost:{port};
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_connect_timeout 30s;
        proxy_send_timeout 30s;
        proxy_read_timeout 30s;
    }}
    
    location /health {{
        proxy_pass http://localhost:{port}/health;
        access_log off;
    }}
}}
"""

# Deployment configuration
DEPLOYMENT_CONFIG = {
    "ports": {
        "blue": 8001,
        "green": 8002
    },
    "urls": {
        "blue": "http://localhost:8001",
        "green": "http://localhost:8002"
    },
    "domain": "rag-system.com"
}

# Usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python deploy.py <version>")
        sys.exit(1)
    
    version = sys.argv[1]
    deployer = BlueGreenDeployer(DEPLOYMENT_CONFIG)
    deployer.deploy(version)
```

### **2. Infrastructure as Code with Docker Compose**

```yaml
# docker-compose.production.yml
version: '3.8'

services:
  rag-blue:
    build:
      context: .
      dockerfile: Dockerfile.production
      args:
        VERSION: ${VERSION:-latest}
    container_name: rag-blue
    ports:
      - "8001:8000"
    environment:
      - ENVIRONMENT=production
      - COLOR=blue
    env_file:
      - .env.production
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - rag-network
    
  rag-green:
    build:
      context: .
      dockerfile: Dockerfile.production  
      args:
        VERSION: ${VERSION:-latest}
    container_name: rag-green
    ports:
      - "8002:8000"
    environment:
      - ENVIRONMENT=production
      - COLOR=green
    env_file:
      - .env.production
    volumes:
      - ./logs:/app/logs
      - ./data:/app/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 60s
    networks:
      - rag-network

  nginx:
    image: nginx:alpine
    container_name: rag-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
      - ./logs/nginx:/var/log/nginx
    depends_on:
      - rag-blue
      - rag-green
    restart: unless-stopped
    networks:
      - rag-network

  redis:
    image: redis:alpine
    container_name: rag-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped
    networks:
      - rag-network
    command: redis-server --appendonly yes

  prometheus:
    image: prom/prometheus
    container_name: rag-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus.yml:/etc/prometheus/prometheus.yml
      - prometheus-data:/prometheus
    restart: unless-stopped
    networks:
      - rag-network

  grafana:
    image: grafana/grafana
    container_name: rag-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin123
    volumes:
      - grafana-data:/var/lib/grafana
      - ./monitoring/grafana/dashboards:/etc/grafana/provisioning/dashboards
    restart: unless-stopped
    networks:
      - rag-network

volumes:
  redis-data:
  prometheus-data:
  grafana-data:

networks:
  rag-network:
    driver: bridge
```

### **3. Automated Testing Pipeline**

```python
# tests/integration_tests.py
import pytest
import asyncio
import requests
from typing import Dict, Any

class IntegrationTests:
    """Production-ready integration tests"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        
    def test_health_endpoint(self):
        """Test basic health check"""
        response = self.session.get(f"{self.base_url}/health")
        assert response.status_code == 200
        
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "uptime" in data
    
    def test_query_processing(self):
        """Test core RAG functionality"""
        payload = {
            "query": "What is the VAT rate in France?",
            "client_id": "test_client"
        }
        
        response = self.session.post(
            f"{self.base_url}/api/query",
            json=payload,
            timeout=30
        )
        
        assert response.status_code == 200
        
        data = response.json()
        assert "answer" in data
        assert "sources" in data
        assert "processing_time" in data
        assert data["success"] is True
    
    def test_concurrent_queries(self):
        """Test system under concurrent load"""
        import concurrent.futures
        
        def make_query(query_id: int):
            payload = {
                "query": f"Test query {query_id}",
                "client_id": f"test_client_{query_id}"
            }
            
            response = self.session.post(
                f"{self.base_url}/api/query",
                json=payload,
                timeout=30
            )
            
            return response.status_code == 200
        
        # Test with 10 concurrent queries
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_query, i) for i in range(10)]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
        
        # All queries should succeed
        assert all(results)
    
    def test_error_handling(self):
        """Test graceful error handling"""
        # Test invalid query
        response = self.session.post(
            f"{self.base_url}/api/query",
            json={"invalid": "payload"},
            timeout=30
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "error" in data
    
    def test_performance_requirements(self):
        """Test performance requirements"""
        import time
        
        payload = {
            "query": "Simple performance test query",
            "client_id": "perf_test"
        }
        
        start_time = time.time()
        response = self.session.post(
            f"{self.base_url}/api/query",
            json=payload,
            timeout=30
        )
        end_time = time.time()
        
        assert response.status_code == 200
        
        # Response should be under 5 seconds
        response_time = end_time - start_time
        assert response_time < 5.0, f"Response took {response_time:.2f}s, expected <5s"

# Run integration tests
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python integration_tests.py <base_url>")
        sys.exit(1)
    
    base_url = sys.argv[1]
    tests = IntegrationTests(base_url)
    
    test_methods = [
        tests.test_health_endpoint,
        tests.test_query_processing, 
        tests.test_concurrent_queries,
        tests.test_error_handling,
        tests.test_performance_requirements
    ]
    
    passed = 0
    failed = 0
    
    for test in test_methods:
        try:
            print(f"Running {test.__name__}...")
            test()
            print(f"✅ {test.__name__} PASSED")
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} FAILED: {e}")
            failed += 1
    
    print(f"\n📊 Test Results: {passed} passed, {failed} failed")
    
    if failed > 0:
        sys.exit(1)
```

### **4. Monitoring and Alerting**

```python
# monitoring/metrics.py
import time
import psutil
import threading
from typing import Dict, Any
from dataclasses import dataclass
from collections import defaultdict, deque

@dataclass
class Metric:
    """Individual metric data point"""
    name: str
    value: float
    timestamp: float
    labels: Dict[str, str] = None

class MetricsCollector:
    """Production metrics collection for RAG systems"""
    
    def __init__(self):
        self.metrics = defaultdict(lambda: deque(maxlen=1000))
        self.counters = defaultdict(int)
        self.gauges = defaultdict(float)
        self.histograms = defaultdict(list)
        self.start_time = time.time()
        
        # Start background collection
        self._start_system_metrics_collection()
    
    def increment_counter(self, name: str, labels: Dict[str, str] = None):
        """Increment a counter metric"""
        key = self._make_key(name, labels)
        self.counters[key] += 1
        
        metric = Metric(name, self.counters[key], time.time(), labels)
        self.metrics[key].append(metric)
    
    def set_gauge(self, name: str, value: float, labels: Dict[str, str] = None):
        """Set a gauge metric"""
        key = self._make_key(name, labels)
        self.gauges[key] = value
        
        metric = Metric(name, value, time.time(), labels)
        self.metrics[key].append(metric)
    
    def record_histogram(self, name: str, value: float, labels: Dict[str, str] = None):
        """Record a histogram value"""
        key = self._make_key(name, labels)
        self.histograms[key].append(value)
        
        metric = Metric(name, value, time.time(), labels)
        self.metrics[key].append(metric)
    
    def get_summary(self) -> Dict[str, Any]:
        """Get comprehensive metrics summary"""
        now = time.time()
        uptime = now - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "counters": dict(self.counters),
            "gauges": dict(self.gauges),
            "histograms": self._summarize_histograms(),
            "system": self._get_system_metrics(),
            "timestamp": now
        }
    
    def _make_key(self, name: str, labels: Dict[str, str] = None) -> str:
        """Create a unique key for metric storage"""
        if not labels:
            return name
        
        label_str = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}{{{label_str}}}"
    
    def _summarize_histograms(self) -> Dict[str, Dict[str, float]]:
        """Calculate histogram summaries"""
        summaries = {}
        
        for key, values in self.histograms.items():
            if not values:
                continue
                
            values_sorted = sorted(values)
            count = len(values_sorted)
            
            summaries[key] = {
                "count": count,
                "sum": sum(values_sorted),
                "min": min(values_sorted),
                "max": max(values_sorted),
                "mean": sum(values_sorted) / count,
                "p50": values_sorted[int(count * 0.5)],
                "p95": values_sorted[int(count * 0.95)],
                "p99": values_sorted[int(count * 0.99)]
            }
        
        return summaries
    
    def _get_system_metrics(self) -> Dict[str, float]:
        """Get current system metrics"""
        return {
            "cpu_percent": psutil.cpu_percent(),
            "memory_percent": psutil.virtual_memory().percent,
            "disk_percent": psutil.disk_usage('/').percent,
            "network_bytes_sent": psutil.net_io_counters().bytes_sent,
            "network_bytes_recv": psutil.net_io_counters().bytes_recv
        }
    
    def _start_system_metrics_collection(self):
        """Start background thread for system metrics"""
        def collect_system_metrics():
            while True:
                try:
                    system_metrics = self._get_system_metrics()
                    
                    for metric_name, value in system_metrics.items():
                        self.set_gauge(f"system_{metric_name}", value)
                    
                    time.sleep(60)  # Collect every minute
                    
                except Exception as e:
                    print(f"Error collecting system metrics: {e}")
                    time.sleep(60)
        
        thread = threading.Thread(target=collect_system_metrics, daemon=True)
        thread.start()

# Usage in RAG application
class MonitoredRAG:
    """RAG system with comprehensive monitoring"""
    
    def __init__(self):
        self.metrics = MetricsCollector()
        self.setup_rag_system()
    
    async def process_query(self, query: str, client_id: str) -> Dict[str, Any]:
        """Process query with full monitoring"""
        start_time = time.time()
        
        # Increment request counter
        self.metrics.increment_counter(
            "rag_requests_total",
            {"client_id": client_id, "endpoint": "query"}
        )
        
        try:
            # Process the query
            result = await self._process_query_internal(query, client_id)
            
            # Record success
            self.metrics.increment_counter(
                "rag_requests_success_total",
                {"client_id": client_id}
            )
            
            return result
            
        except Exception as e:
            # Record error
            self.metrics.increment_counter(
                "rag_requests_error_total", 
                {"client_id": client_id, "error_type": type(e).__name__}
            )
            raise
            
        finally:
            # Record response time
            response_time = time.time() - start_time
            self.metrics.record_histogram(
                "rag_response_time_seconds",
                response_time,
                {"client_id": client_id}
            )
    
    def get_metrics_endpoint(self) -> Dict[str, Any]:
        """Metrics endpoint for monitoring systems"""
        return self.metrics.get_summary()

# Alerting configuration
ALERT_RULES = [
    {
        "name": "High Error Rate",
        "condition": "error_rate > 0.05",  # 5% error rate
        "severity": "critical",
        "channels": ["email", "slack"]
    },
    {
        "name": "Slow Response Time", 
        "condition": "p95_response_time > 5.0",  # 5 second p95
        "severity": "warning",
        "channels": ["slack"]
    },
    {
        "name": "High Memory Usage",
        "condition": "memory_percent > 85",
        "severity": "warning", 
        "channels": ["email"]
    },
    {
        "name": "Service Down",
        "condition": "uptime < 60",  # Less than 1 minute uptime
        "severity": "critical",
        "channels": ["email", "slack", "sms"]
    }
]
```

---

## 🔧 Production Deployment Checklist

### **Pre-Deployment**
- [ ] All tests pass (unit, integration, load)
- [ ] Security scan completed
- [ ] Performance benchmarks meet requirements  
- [ ] Database migrations tested
- [ ] Configuration validated
- [ ] Monitoring dashboards configured
- [ ] Alert rules tested
- [ ] Rollback plan documented

### **Deployment**
- [ ] Blue-green deployment executed
- [ ] Health checks pass
- [ ] Smoke tests pass
- [ ] Traffic switched successfully
- [ ] Performance monitoring active
- [ ] Error rates within acceptable limits

### **Post-Deployment**
- [ ] Full functionality verified
- [ ] Performance metrics stable
- [ ] No alerts triggered
- [ ] Client usage patterns normal
- [ ] Team notified of successful deployment
- [ ] Documentation updated
- [ ] Lessons learned documented

---

## 📊 Key Production Metrics

### **Business Metrics**
- **Revenue per client:** Track monthly recurring revenue
- **Client satisfaction:** Response time and accuracy
- **Usage patterns:** Queries per client per day
- **Cost per query:** API costs and infrastructure

### **Technical Metrics**
- **Response time:** P50, P95, P99 latencies
- **Error rate:** Percentage of failed requests
- **Uptime:** System availability percentage
- **Cache hit rate:** Cost optimization metric

### **Infrastructure Metrics**
- **CPU usage:** Server utilization
- **Memory usage:** RAM consumption
- **Disk usage:** Storage capacity
- **Network I/O:** Bandwidth utilization

---

## 🚀 Conclusion

These production patterns have been battle-tested in high-revenue RAG systems. They provide:

1. **Reliability:** Circuit breakers and retry logic prevent cascading failures
2. **Scalability:** Blue-green deployment enables zero-downtime updates  
3. **Observability:** Comprehensive monitoring catches issues early
4. **Maintainability:** Clean patterns make systems easy to debug and extend

Implement these patterns progressively as your RAG system grows from prototype to €40k+/month production system. Focus on reliability first, then optimize for performance and cost.

**Remember:** Production systems that make money require production engineering practices. These patterns are your insurance policy against costly outages during critical client demos and daily operations.