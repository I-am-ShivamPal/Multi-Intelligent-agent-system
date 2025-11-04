# Day 2: Cloud Deployment Guide

## 🚀 Render Deployment Steps

### 1. Dashboard Deployment
```bash
# Create new web service on Render
Repository: https://github.com/I-am-ShivamPal/Multi-Intelligent-agent-system.git
Build Command: pip install -r requirements.txt
Start Command: streamlit run dashboard/dashboard.py --server.port=$PORT --server.address=0.0.0.0
```

### 2. MCP Endpoints Deployment
```bash
# Create second web service for MCP endpoints
Repository: https://github.com/I-am-ShivamPal/Multi-Intelligent-agent-system.git
Build Command: pip install -r requirements.txt
Start Command: python mcp_endpoints.py
Environment Variables:
  MCP_HOST=0.0.0.0
  MCP_PORT=$PORT
```

## 🧪 Testing Endpoints

### Public MCP Endpoints
- **Health Check**: `https://your-mcp-service.onrender.com/health`
- **Outbox**: `https://your-mcp-service.onrender.com/mcp_outbox`
- **Inbox**: `https://your-mcp-service.onrender.com/mcp_inbox` (POST)

### Test Commands
```bash
# Test health endpoint
curl https://your-mcp-service.onrender.com/health

# Test outbox
curl https://your-mcp-service.onrender.com/mcp_outbox

# Test inbox
curl -X POST https://your-mcp-service.onrender.com/mcp_inbox \
  -H "Content-Type: application/json" \
  -d '{"type":"test","content":"deployment test"}'

# Run validation script
python test_endpoints.py https://your-mcp-service.onrender.com
```

## 🔄 Main.py Flow Validation

### End-to-End Test
1. **Data Simulation** - Modify student_scores.csv
2. **Issue Detection** - Trigger anomaly detection
3. **Deployment** - Execute dashboard deployment
4. **Healing** - Auto-heal agent activation
5. **RL Learning** - Q-table updates
6. **MCP Integration** - Message bus communication

### Expected Flow
```
main.py → agents → issue_detector → auto_heal → rl_optimizer → mcp_bridge
```

## 📊 Monitoring

### Dashboard URL
- **Public Dashboard**: `https://your-dashboard.onrender.com`
- **Manual Override**: Available in sidebar and main area
- **Real-time Data**: Auto-refresh enabled

### Validation Checklist
- [ ] Dashboard loads successfully
- [ ] MCP endpoints respond correctly
- [ ] Main.py completes without errors
- [ ] Logs are generated properly
- [ ] Manual override functions work
- [ ] All tabs display data

## 🛠️ Troubleshooting

### Common Issues
1. **Port conflicts**: Ensure $PORT is used correctly
2. **File permissions**: Check log directory access
3. **Dependencies**: Verify requirements.txt completeness
4. **Environment**: Set proper environment variables

### Debug Commands
```bash
# Check service logs
render logs --service your-service-name

# Test locally first
docker-compose up --build
python test_endpoints.py http://localhost:8080
```