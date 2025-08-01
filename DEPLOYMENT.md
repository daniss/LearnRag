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
docker run -p 8501:8501 \
  -e OPENAI_API_KEY=your_key \
  -e PINECONE_API_KEY=your_key \
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