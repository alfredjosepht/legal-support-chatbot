# 🚀 Getting Started - Legal Support Chatbot

## ⚡ Quick Start (5 minutes)

### Option 1: Automated Setup (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/legal-support-chatbot.git
cd legal-support-chatbot

# 2. Run setup script
bash setup.sh

# 3. Run start script (in one terminal)
bash start.sh

# 4. Open browser
# Visit: http://localhost:3001
```

### Option 2: Manual Setup

**Terminal 1 - Backend Setup & Run**
```bash
# Navigate to project
cd legal-support-chatbot

# Install dependencies
pip install -r requirements.txt

# Start backend
python -m uvicorn app:app --reload --port 8000
```

**Terminal 2 - Frontend Setup & Run**
```bash
# Navigate to frontend
cd legal-support-chatbot/frontend

# Install dependencies
npm install

# Start frontend
PORT=3001 npm start
```

**Then Open**
```
http://localhost:3001
```

## ✅ Verification

Once running, you should see:

1. **Backend Terminal**: 
   ```
   INFO:     Uvicorn running on http://127.0.0.1:8000
   INFO:     Application startup complete
   ```

2. **Frontend Terminal**:
   ```
   webpack compiled successfully
   Compiled successfully!
   ```

3. **Browser**:
   - Dark/Light themed chat interface
   - Text input field
   - "Legal Consultation" header
   - Logo (⚖️)

## 🧪 Test It

Try these queries in the browser:

1. **Physical Assault**
   ```
   my senior punched me
   ```
   Expected: Category = physical_assault, 6+ laws shown

2. **Sexual Assault (Minor)**
   ```
   I am 16 and my uncle touched me
   ```
   Expected: POCSO framework triggered, warning shown

3. **Discrimination**
   ```
   I face discrimination because of my caste
   ```
   Expected: Category = caste_discrimination, 8+ steps shown

4. **Cybercrime**
   ```
   my intimate photos were shared online without consent
   ```
   Expected: Category = cyber_sexual_crime, resources provided

## 📖 Understanding the Response

Each response includes:

```
🏷️ Case Category: PHYSICAL_ASSAULT
📊 Confidence: 28%

🔍 Other Possible Issues:
   • verbal_abuse (15%)

⚖️ Applicable Legal Frameworks:
   • Indian Penal Code (IPC)

📜 Applicable Laws & Sections:
   • 323 (IPC): Voluntarily causing hurt
   • 324 (IPC): Causing hurt by poison
   • 325 (IPC): Voluntarily causing grievous hurt
   ... (3 more laws)

📋 Steps to File Case (14 steps total):
   1. File FIR at police station
   2. Provide identification
   3. Give written statement
   ... (11 more steps)

📞 Support Resources:
   • Police Station: [Address]
   • Legal Aid: [Contact]
   • NGOs: [Details]

⚠️ Important Notes:
   • This is guidance, not legal advice
   • Consult a lawyer for your case

▶ Show Full Details  (Click to expand everything)
```

## 🛠️ Troubleshooting

### "Cannot connect to backend"

**Problem**: Frontend shows "NetworkError when attempting to fetch"

**Solutions**:
```bash
# Check if backend is running
curl http://localhost:8000/

# If not, restart backend
pkill -f "uvicorn app:app"
python -m uvicorn app:app --reload --port 8000
```

### "Port 8000 already in use"

**Solutions**:
```bash
# Find and kill process using port 8000
fuser -k 8000/tcp

# OR use different port
python -m uvicorn app:app --port 8001
```

### "Port 3001 already in use"

**Solutions**:
```bash
# Use different port
cd frontend
PORT=3002 npm start
```

### "npm not found"

**Solution**: Install Node.js from https://nodejs.org/

### "Python module not found"

**Solutions**:
```bash
# Reinstall dependencies
pip install --upgrade pip
pip install -r requirements.txt

# If still failing, use virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### "React app won't compile"

**Solutions**:
```bash
# Clear node modules and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Try again
npm start
```

## 📋 What to Do Next

### If It Works! ✅
1. Try different queries to explore all 20 crime categories
2. Check the expanded details view
3. Read through legal steps
4. Contact resources for real cases

### To Customize

**Add more training examples:**
```bash
# 1. Edit data/dataset.csv
# 2. Add rows: text,label
# 3. Retrain model
python nlp/train_classifier.py
# 4. Restart backend
```

**Add new laws:**
```bash
# 1. Edit data/law_mapping_enhanced.json
# 2. Add law entries with section, title, description
# 3. Restart backend
```

## 📚 Project Files Overview

| File | Purpose |
|------|---------|
| `app.py` | FastAPI backend |
| `frontend/src/App.js` | React frontend |
| `data/dataset.csv` | 1,557 training examples |
| `models/legal_textcat/` | Trained NLP model |
| `data/law_mapping_enhanced.json` | 50+ Indian laws |
| `nlp/train_classifier.py` | Model training script |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |

## 🆘 Getting Help

1. **Check README.md** - Full documentation with API reference
2. **Check logs**:
   ```bash
   tail -50 /tmp/backend.log
   tail -50 /tmp/frontend.log
   ```
3. **Test API directly**:
   ```bash
   curl -X POST http://localhost:8000/chat \
     -H "Content-Type: application/json" \
     -d '{"message":"my senior punched me"}'
   ```

## 🚀 Production Deployment

To deploy online:

1. **Using Heroku**:
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

2. **Using AWS/GCP**: See README.md for Dockerfile

3. **Using Docker Locally**:
   ```bash
   docker-compose up
   ```

---

**Ready to help students?** 🎉

Start the system and begin providing legal guidance!
