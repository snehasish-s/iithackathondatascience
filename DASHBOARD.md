# Web Dashboard - Causal Chat Analysis

This directory contains the web frontend for the Causal Chat Analysis system.

## 📁 Directory Structure

```
├── api.py                      # Flask backend API server
├── run.py                      # Startup script (recommended)
├── templates/
│   └── index.html             # Main dashboard HTML
└── static/
    ├── css/
    │   └── style.css          # Dashboard styling
    └── js/
        ├── api.js             # API client functions
        ├── charts.js          # Chart.js initialization
        └── app.js             # Main application logic
```

## 🚀 Quick Start

### Method 1: Using Startup Script (Recommended)

```bash
python run.py
```

This will:
1. Check all dependencies
2. Start the Flask API server
3. Automatically open the dashboard in your browser

### Method 2: Manual Startup

First, install Flask dependencies:
```bash
pip install flask flask-cors
```

Then start the API server:
```bash
python api.py
```

Then open your browser and navigate to:
```
http://localhost:5000
```

## 🛠 API Endpoints

The Flask backend provides the following endpoints:

- `GET /` - Main dashboard HTML
- `GET /api/stats` - Overall statistics
- `GET /api/causes` - Causal analysis results
- `GET /api/signals` - Signal extraction results
- `GET /api/warnings` - Early warning detection results
- `GET /api/domains` - Domain breakdown
- `GET /api/intents` - Intent breakdown
- `GET /api/transcript/<id>` - Specific transcript details
- `GET /api/health` - Health check

## 📊 Dashboard Features

### 1. Overview Tab
- Key metrics (total conversations, turns, escalation rate)
- Escalation breakdown chart
- Top domains visualization
- Top intents analysis

### 2. Causes Tab
- Root cause analysis with percentages
- Evidence and examples from conversations
- Cause distribution chart

### 3. Signals Tab
- Signal type breakdown
- Keyword detection summary
- Signal extraction metrics

### 4. Early Warnings Tab
- High-risk conversations count
- Multi-signal and single-signal warnings
- Warning distribution chart
- Detection thresholds configuration

### 5. Insights Tab
- Priority-ranked recommendations
- Actionable insights based on analysis
- Implementation metrics (Impact vs Effort)

## 🎨 Frontend Technology Stack

- **HTML5** - Semantic markup
- **CSS3** - Modern styling with CSS variables
- **JavaScript (ES6+)** - Dynamic interactivity
- **Chart.js** - Interactive data visualization
- **Font Awesome** - Icon library

## 🔧 Configuration

### API Base URL

To change the API server address, edit `static/js/api.js`:

```javascript
const API = {
    BASE_URL: 'http://localhost:5000/api',
    // ... rest of API client
```

### Charts Configuration

Charts are configured in `static/js/charts.js`. You can customize:
- Colors
- Chart types
- Responsive behavior
- Animation options

### Styling

All styles are in `static/css/style.css`. Key variables:

```css
:root {
    --primary-color: #2563eb;
    --danger-color: #dc2626;
    --success-color: #16a34a;
    /* ... more colors */
}
```

## 📱 Responsive Design

The dashboard is fully responsive and works on:
- Desktop (1920px+)
- Laptop (1200px - 1920px)
- Tablet (768px - 1200px)
- Mobile (< 768px)

## 🐛 Troubleshooting

### Issue: "Connection refused" error

**Solution**: Make sure the Flask API server is running:
```bash
python api.py
```

### Issue: Charts not loading

**Solution**: Check browser console for errors. Make sure Chart.js library loaded:
- Verify internet connection (CDN access)
- Check browser console (F12)

### Issue: No data appears

**Solution**: 
1. Check API server logs for errors
2. Verify data file exists: `data/Conversational_Transcript_Dataset.json`
3. Open browser console to see API error responses

### Issue: CORS errors

**Solution**: These are handled by Flask-CORS. If you see CORS errors:
1. Verify Flask-CORS is installed: `pip install flask-cors`
2. Restart the Flask server

## 🌐 Browser Support

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## 📖 Code Structure

### api.js
Provides API client with methods:
- `API.getStats()` - Get overall statistics
- `API.getCauses()` - Get causal analysis
- `API.getSignals()` - Get signal extraction
- `API.getWarnings()` - Get early warnings
- `API.getDomains()` - Get domain data
- `API.getIntents()` - Get intent data

### charts.js
Initializes Chart.js charts:
- `Charts.initEscalationChart()`
- `Charts.initDomainsChart()`
- `Charts.initIntentsChart()`
- `Charts.initCausesChart()`
- `Charts.initSignalsChart()`
- `Charts.initWarningsChart()`

### app.js
Main application controller:
- `CausalChatApp` class handles all UI logic
- Tab switching
- Data loading and refresh
- Real-time updates

## 🔒 Security

The dashboard is designed for internal use. For production deployment:

1. **Enable authentication** in `api.py`
2. **Use HTTPS** instead of HTTP
3. **Implement rate limiting** on API endpoints
4. **Add input validation** for all API requests
5. **Deploy with a production WSGI server** (Gunicorn, uWSGI)

## 📊 Performance

- Data is loaded once on page load
- Chart rendering is automatically optimized
- CSS and JavaScript are minimal
- Responsive design uses CSS Grid and Flexbox

## 🔄 Refresh Data

To refresh data without reloading:
1. Click any tab
2. Wait for "Loading data..." indicator
3. Charts and stats update automatically

## 📚 Additional Resources

- [Chart.js Documentation](https://www.chartjs.org/)
- [Font Awesome Icons](https://fontawesome.com/icons)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [MDN Web Docs](https://developer.mozilla.org/)

## 📝 License

This project is provided as-is for educational and analytical purposes.

---

**Last Updated**: February 6, 2026
**Version**: 1.0.0
