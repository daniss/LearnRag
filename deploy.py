#!/usr/bin/env python3
"""
Deployment script for French Legal RAG Assistant
Supports Railway, Heroku, and other cloud platforms
"""

import os
import json
import subprocess
import sys
from datetime import datetime

def create_railway_config():
    """Create Railway deployment configuration"""
    
    # railway.json
    railway_config = {
        "build": {
            "builder": "NIXPACKS"
        },
        "deploy": {
            "restartPolicyType": "ON_FAILURE",
            "restartPolicyMaxRetries": 10
        }
    }
    
    with open('railway.json', 'w') as f:
        json.dump(railway_config, f, indent=2)
    
    # Procfile for Railway/Heroku
    procfile_content = "web: streamlit run app.py --server.port $PORT --server.address 0.0.0.0"
    with open('Procfile', 'w') as f:
        f.write(procfile_content)
    
    print("✅ Railway configuration created")

def create_dockerfile():
    """Create Docker configuration"""
    
    dockerfile_content = """
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    build-essential \\
    curl \\
    software-properties-common \\
    git \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements_simple.txt .
RUN pip3 install -r requirements_simple.txt

# Copy application code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run the application
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
"""
    
    with open('Dockerfile', 'w') as f:
        f.write(dockerfile_content.strip())
    
    # .dockerignore
    dockerignore_content = """
.git
.gitignore
README.md
Dockerfile
.dockerignore
venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
.pytest_cache/
.coverage
*.log
"""
    
    with open('.dockerignore', 'w') as f:
        f.write(dockerignore_content.strip())
    
    print("✅ Docker configuration created")

def create_vercel_config():
    """Create Vercel deployment configuration"""
    
    vercel_config = {
        "builds": [
            {
                "src": "app.py",
                "use": "@vercel/python"
            }
        ],
        "routes": [
            {
                "src": "/(.*)",
                "dest": "app.py"
            }
        ]
    }
    
    with open('vercel.json', 'w') as f:
        json.dump(vercel_config, f, indent=2)
    
    print("✅ Vercel configuration created")

def create_environment_template():
    """Create comprehensive environment template"""
    
    env_template = """
# API Configuration
OPENAI_API_KEY=your_openai_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_ENVIRONMENT=us-west1-gcp-free

# Application Settings
APP_TITLE=Assistant Juridique IA
APP_DESCRIPTION=Votre Expert Légal Instantané
APP_URL=https://your-app-url.com

# Business Configuration
BUSINESS_EMAIL=contact@assistant-juridique-ia.fr
BUSINESS_PHONE=+33 6 12 34 56 78
BUSINESS_NAME=Assistant Juridique IA

# Sales Configuration
DEMO_MODE=true
PRICING_TIER_STARTER=5000
PRICING_TIER_PRO=8000
MONTHLY_STARTER=1500
MONTHLY_PRO=2500

# Analytics (Optional)
GOOGLE_ANALYTICS_ID=your_ga_id_here
HOTJAR_ID=your_hotjar_id_here

# Feature Flags
ENABLE_API_RAG=false
ENABLE_DEMO_MODE=true
ENABLE_PAYMENTS=false
"""
    
    with open('.env.production', 'w') as f:
        f.write(env_template.strip())
    
    print("✅ Production environment template created")

def create_deployment_docs():
    """Create deployment documentation"""
    
    deployment_docs = """
# 🚀 Deployment Guide - French Legal RAG Assistant

## Quick Deploy Options

### 🚂 Railway (Recommended - Free Tier)
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login and deploy
railway login
railway link [your-project-id]
railway up

# 3. Set environment variables
railway variables set OPENAI_API_KEY=your_key
railway variables set PINECONE_API_KEY=your_key
```

### 🟦 Heroku
```bash
# 1. Install Heroku CLI
# 2. Create app
heroku create your-app-name

# 3. Set environment variables  
heroku config:set OPENAI_API_KEY=your_key
heroku config:set PINECONE_API_KEY=your_key

# 4. Deploy
git push heroku main
```

### 🐳 Docker
```bash
# Build image
docker build -t french-legal-rag .

# Run container
docker run -p 8501:8501 \\
  -e OPENAI_API_KEY=your_key \\
  -e PINECONE_API_KEY=your_key \\
  french-legal-rag
```

### ▲ Vercel
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy
vercel --prod

# 3. Set environment variables in dashboard
```

## Environment Variables

Required for production:
- `OPENAI_API_KEY` - OpenAI API key ($200 credit recommended)
- `PINECONE_API_KEY` - Pinecone API key (free tier sufficient)
- `PINECONE_ENVIRONMENT` - Pinecone environment (us-west1-gcp-free)

Optional:
- `APP_TITLE` - Custom app title
- `BUSINESS_EMAIL` - Contact email for leads
- `BUSINESS_PHONE` - Contact phone for sales

## Production Checklist

### Before Deployment:
- [ ] API keys obtained and tested
- [ ] Demo documents customized for target market
- [ ] Contact information updated in config.py
- [ ] Pricing tiers configured
- [ ] Demo script personalized

### After Deployment:
- [ ] Health check URL working
- [ ] Demo flow tested end-to-end  
- [ ] Contact forms working
- [ ] Analytics configured (optional)
- [ ] SSL certificate active

## Custom Domain Setup

### Railway:
1. Go to Railway dashboard
2. Settings → Domains
3. Add custom domain
4. Update DNS records

### Heroku:
```bash
heroku domains:add your-domain.com
# Configure DNS with provided target
```

## Performance Optimization

### For High Traffic:
- Enable Redis caching
- Add CDN (Cloudflare)
- Optimize images and assets
- Implement rate limiting

### Cost Management:
- Monitor API usage daily
- Set up billing alerts
- Cache frequent queries
- Implement request queuing

## Security Checklist

- [ ] HTTPS enabled
- [ ] Environment variables secured
- [ ] API keys rotated regularly
- [ ] Error messages sanitized
- [ ] Rate limiting implemented
- [ ] GDPR compliance verified

## Monitoring & Analytics

### Essential Metrics:
- Demo completion rate
- Contact form submissions
- API response times
- Error rates
- User flow analysis

### Tools:
- Google Analytics (traffic)
- Hotjar (user behavior)
- Sentry (error tracking)
- Railway/Heroku logs (system)

## Scaling Strategy

### Month 1 (MVP):
- Single instance
- Basic monitoring
- Manual sales follow-up

### Month 2-3 (Growth):
- Auto-scaling enabled
- Analytics dashboard
- CRM integration

### Month 6+ (Scale):
- Multi-region deployment
- Advanced caching
- Custom integrations

## Support & Maintenance

### Daily:
- Check error logs
- Monitor API usage
- Review contact submissions

### Weekly:
- Update demo content
- Analyze user metrics
- Test all features

### Monthly:
- Security updates
- Performance optimization
- Feature enhancements

## Backup Strategy

### Critical Data:
- Demo documents (Git)
- Configuration files (Git)
- Client contact data (CRM)
- Analytics data (Export)

### Recovery Plan:
1. Redeploy from Git
2. Restore environment variables
3. Test all functionality
4. Verify integrations

---

Ready to deploy? Choose your platform and follow the guide above.

🎯 **Goal**: Get your demo live in 30 minutes, start booking demos today.
"""
    
    with open('DEPLOYMENT.md', 'w') as f:
        f.write(deployment_docs.strip())
    
    print("✅ Deployment documentation created")

def create_launch_checklist():
    """Create comprehensive launch checklist"""
    
    checklist = f"""
# 🚀 LAUNCH CHECKLIST - French Legal RAG Assistant

Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 📋 Pre-Launch Technical Checklist

### ✅ Core System
- [ ] RAG system tested with demo documents
- [ ] Streamlit app runs without errors
- [ ] All sales materials generated
- [ ] Demo script finalized
- [ ] Pricing configured correctly

### ✅ API Integration  
- [ ] OpenAI API key configured ($200 credit)
- [ ] Pinecone account created (free tier)
- [ ] Both APIs tested successfully
- [ ] Rate limiting understood
- [ ] Error handling implemented

### ✅ Deployment
- [ ] Cloud platform chosen (Railway/Heroku/Vercel)
- [ ] App successfully deployed  
- [ ] Environment variables set
- [ ] Custom domain configured (optional)
- [ ] SSL certificate active

### ✅ Demo Content
- [ ] French legal documents loaded
- [ ] Sample queries tested
- [ ] Response quality verified
- [ ] Sources citation working
- [ ] Export functionality tested

## 📈 Pre-Launch Business Checklist

### ✅ Sales Materials
- [ ] Cold email templates ready
- [ ] LinkedIn messages prepared
- [ ] Demo script memorized
- [ ] Pricing sheets printed
- [ ] ROI calculator ready

### ✅ Target Market Research
- [ ] 100+ law firms identified
- [ ] Contact emails found/verified
- [ ] LinkedIn profiles researched
- [ ] Competitor analysis done
- [ ] Market positioning defined

### ✅ Lead Generation Setup
- [ ] Calendly booking link configured
- [ ] Email tracking setup (optional)
- [ ] CRM system chosen (Airtable/Notion)
- [ ] Phone number configured
- [ ] Professional email address

### ✅ Social Proof
- [ ] LinkedIn profile optimized
- [ ] Company/project website live
- [ ] Case study templates ready
- [ ] Testimonial collection plan
- [ ] Reference client identified

## 🎯 Launch Week Activities

### Day 1: Soft Launch
- [ ] Send 10 test emails to connections
- [ ] Post LinkedIn announcement
- [ ] Test demo booking flow
- [ ] Monitor system performance
- [ ] Collect initial feedback

### Day 2-3: Targeted Outreach
- [ ] Send 20 cold emails daily
- [ ] Connect with 10 prospects on LinkedIn
- [ ] Follow up previous contacts
- [ ] Book first demo calls
- [ ] Refine messaging based on responses

### Day 4-5: Demo Delivery
- [ ] Conduct first sales demos
- [ ] Collect detailed feedback
- [ ] Refine demo script
- [ ] Handle objections
- [ ] Schedule follow-up calls

### Weekend: Analysis & Optimization
- [ ] Review week's metrics
- [ ] Optimize low-performing elements
- [ ] Plan next week's strategy
- [ ] Update prospect list
- [ ] Prepare for scale

## 📊 Success Metrics (Week 1)

### Email Outreach:
- [ ] 70+ emails sent
- [ ] 10%+ open rate
- [ ] 2%+ response rate
- [ ] 5+ demo requests

### Demo Delivery:
- [ ] 3+ demos completed
- [ ] 1+ hot prospect identified
- [ ] Feedback collected from all
- [ ] Follow-up scheduled

### System Performance:
- [ ] 99%+ uptime
- [ ] <2 second response times
- [ ] 0 critical errors
- [ ] All features working

## 🚨 Emergency Contacts & Backup Plans

### Technical Issues:
- **Platform Down**: Switch to simple_demo.py standalone
- **API Failure**: Use demo mode responses
- **Performance Issues**: Contact platform support

### Sales Issues:
- **Low Response**: A/B test new email templates
- **Demo No-Shows**: Send reminder sequences
- **Price Objections**: Emphasize ROI calculation

### Quick Fixes:
- Demo not working? Run: `python3 test_demo.py`
- Site down? Check: Railway/Heroku logs
- API errors? Verify: Environment variables

## 🎉 Launch Day Protocol

### 9 AM: System Check
- [ ] App loading correctly
- [ ] Demo functionality tested
- [ ] All contact forms working
- [ ] Analytics tracking active

### 10 AM: First Outreach Batch
- [ ] 20 cold emails sent
- [ ] LinkedIn posts published
- [ ] Personal network notified
- [ ] Industry forums posted

### 2 PM: Response Monitoring
- [ ] Check email responses
- [ ] Reply to LinkedIn messages
- [ ] Book incoming demo requests
- [ ] Update prospect tracking

### 6 PM: Day Analysis
- [ ] Review all metrics
- [ ] Note lessons learned
- [ ] Plan tomorrow's activities
- [ ] Celebrate progress made!

## 💰 Revenue Targets

### Week 1:
- **Goal**: 5+ qualified demos
- **Stretch**: 1 hot prospect ready to buy

### Week 2:
- **Goal**: 10+ demos, 3+ proposals sent
- **Stretch**: First contract signed

### Week 3:  
- **Goal**: €5,000 first payment received
- **Stretch**: Second client in pipeline

### Month 1:
- **Goal**: €5,000+ recurring revenue
- **Stretch**: €10,000+ with 2 clients

---

## ✅ FINAL LAUNCH APPROVAL

Only proceed with launch when ALL critical items checked:

- [ ] Technical system 100% functional
- [ ] Sales materials complete and tested  
- [ ] Target prospect list ready (100+)
- [ ] Demo script memorized and practiced
- [ ] Emergency backup plans prepared
- [ ] Success metrics defined and trackable

**Launch Authorization**: _________________ Date: _________

🚀 **Ready to make money with French Legal RAG? Let's launch!**
"""
    
    with open('LAUNCH_CHECKLIST.md', 'w') as f:
        f.write(checklist.strip())
    
    print("✅ Launch checklist created")

def deploy_to_railway():
    """Deploy to Railway if CLI is available"""
    try:
        # Check if railway CLI is available
        result = subprocess.run(['railway', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("🚂 Railway CLI detected")
            
            # Initialize Railway project
            choice = input("Deploy to Railway now? (y/n): ").lower()
            if choice == 'y':
                subprocess.run(['railway', 'login'])
                subprocess.run(['railway', 'init'])
                subprocess.run(['railway', 'up'])
                print("🎉 Deployed to Railway!")
            else:
                print("ℹ️ Railway deployment skipped")
        else:
            print("ℹ️ Railway CLI not found - install with: npm install -g @railway/cli")
    except FileNotFoundError:
        print("ℹ️ Railway CLI not available - manual deployment required")

def main():
    """Main deployment setup function"""
    print("🚀 Setting up deployment for French Legal RAG Assistant")
    print("=" * 60)
    
    # Create deployment configurations
    create_railway_config()
    create_dockerfile() 
    create_vercel_config()
    create_environment_template()
    create_deployment_docs()
    create_launch_checklist()
    
    print("\n✅ All deployment files created!")
    print("\n📁 Files generated:")
    deployment_files = [
        'railway.json', 'Procfile', 'Dockerfile', '.dockerignore',
        'vercel.json', '.env.production', 'DEPLOYMENT.md', 'LAUNCH_CHECKLIST.md'
    ]
    
    for file in deployment_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
    
    print(f"\n🎯 Next steps:")
    print("1. Choose deployment platform (Railway/Heroku/Vercel)")
    print("2. Set up API keys (OpenAI + Pinecone)")
    print("3. Follow DEPLOYMENT.md guide")
    print("4. Complete LAUNCH_CHECKLIST.md")
    print("5. Start outreach and book demos!")
    
    # Optional: Deploy to Railway
    deploy_to_railway()

if __name__ == "__main__":
    main()