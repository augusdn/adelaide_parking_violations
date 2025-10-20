# Adelaide Parking Violations Map 🚗📍

A comprehensive interactive web application that visualizes Adelaide's parking violation data on an interactive map. Built with React, TypeScript, and Leaflet for a cost-effective, static deployment.

![Screenshot](https://via.placeholder.com/800x400/3b82f6/ffffff?text=Adelaide+Parking+Map)

## ✨ Features

### 🗺️ Interactive Map
- **Visual Overview**: Color-coded street markers showing violation density
- **Click to Explore**: Interactive street selection with detailed popup information
- **Smart Scaling**: Circle sizes represent fine amounts, colors show relative density
- **Free Mapping**: Uses OpenStreetMap (no API keys required)

### 📊 Comprehensive Analytics
- **Street-Level Insights**: Total fines, violation counts, payment compliance
- **Temporal Analysis**: Patterns by time, day, month, and year
- **Violation Types**: Breakdown of most common parking offences
- **Payment Status**: Outstanding vs. paid fine tracking

### 🔍 Advanced Filtering
- **Search Functionality**: Find specific streets instantly
- **Top 10 View**: Focus on highest violation streets
- **Real-time Filtering**: Dynamic data updates without page refresh

### 💰 Financial Insights
- **Revenue Tracking**: Total fines collected and outstanding amounts
- **Compliance Rates**: Payment success rates by street
- **Average Fine Analysis**: Cost patterns across different areas

## 🏗️ Architecture

This project uses a **static-first architecture** optimized for low-cost deployment:

```
Raw CSV Data → Python Processing → Static JSON → React Frontend → Free Hosting
```

### Why This Approach?
- **Cost Effective**: $0 hosting on GitHub Pages/Netlify
- **High Performance**: Pre-processed data loads instantly
- **No Backend**: Eliminates server costs and complexity
- **Scalable**: CDN distribution for global performance

## 🚀 Tech Stack

### Frontend
- **React 18** with TypeScript - Modern, type-safe UI
- **Vite** - Lightning-fast build tool and dev server
- **Leaflet** - Open-source mapping (no API costs)
- **Tailwind CSS** - Utility-first styling
- **Chart.js** - Data visualizations

### Data Processing
- **Python** with Pandas - CSV processing and analysis
- **Nominatim** - Free geocoding via OpenStreetMap

### Deployment
- **GitHub Pages** - Free static hosting
- **GitHub Actions** - Automated CI/CD pipeline

## 📋 Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.8+ with pip
- **Git** for version control

## ⚡ Quick Start

### 1. Clone & Install
```bash
git clone <your-repo-url>
cd fine_map
npm install
```

### 2. Install Python Dependencies
```bash
cd scripts
pip install -r requirements.txt
cd ..
```

### 3. Process Data (First Time Only)
```bash
# This processes the CSV and generates optimized JSON files
npm run process-data
```

### 4. Start Development Server
```bash
npm run dev
```

Visit `http://localhost:3000` to see your application!

## 📊 Data Processing

The Python script (`scripts/process_data.py`) transforms the raw CSV into optimized JSON files:

- **streets.json** - Street-level aggregated data with coordinates
- **summary.json** - Overall statistics and metadata
- **temporal.json** - Time-based analysis data
- **offences.json** - Violation type breakdowns

### Processing Features:
- **Geocoding**: Converts street names to coordinates using free Nominatim API
- **Caching**: Geocoding results cached to avoid re-processing
- **Data Cleaning**: Handles malformed CSV entries and missing data
- **Aggregation**: Pre-calculates all statistics for fast frontend loading

## 🌐 Deployment

### Quick Deployment
```bash
# Use the deployment script (recommended)
./deploy.sh
```

### Manual GitHub Pages Deployment
```bash
# 1. Build for production
npm run build

# 2. Commit and push
git add .
git commit -m "Deploy Adelaide Parking Violations Map"
git push origin main

# 3. Enable GitHub Pages in repository settings
```

### Other Hosting Services
```bash
# Build for production
npm run build

# Upload the 'dist' folder to:
# - Netlify (drag & drop dist folder)
# - Vercel (connect GitHub repo)
# - Any static hosting service
```

### Automated Deployment
The included GitHub Actions workflow automatically:
1. Processes new CSV data
2. Builds the application
3. Deploys to GitHub Pages

## 📁 Project Structure

```
fine_map/
├── src/
│   ├── components/          # React components
│   │   ├── MapView.tsx      # Main map interface
│   │   └── StreetDetails.tsx # Detailed street modal
│   ├── services/            # Data management
│   │   └── dataService.ts   # API and utility functions
│   ├── types/               # TypeScript definitions
│   └── App.tsx              # Main application
├── public/
│   └── data/                # Processed JSON files
├── scripts/
│   ├── process_data.py      # Data processing script
│   └── requirements.txt     # Python dependencies
├── data/                    # Original CSV files
└── dist/                    # Built application (generated)
```

## 🔧 Configuration

### Update Repository Name
In `vite.config.ts`, update the `base` URL to match your GitHub repository:
```typescript
export default defineConfig({
  base: '/your-repository-name/',  // Update this
  // ... other config
})
```

### Processing Custom Data
To use different CSV data:
1. Place CSV file in `data/` directory
2. Update `CSV_PATH` in `scripts/process_data.py`
3. Run `npm run process-data`

## 📈 Performance Optimizations

- **Code Splitting**: Automatic chunking for faster loading
- **Image Optimization**: Responsive images and lazy loading
- **Caching**: Aggressive browser caching for static assets
- **Compression**: Gzip compression in production builds
- **Tree Shaking**: Removes unused code automatically

## 🔒 Security & Privacy

- **No Backend**: Eliminates server-side vulnerabilities
- **Static Files**: All data pre-processed and publicly available
- **No Personal Data**: Only aggregate violation statistics
- **HTTPS**: Secure delivery via GitHub Pages/Netlify

## 🎯 Future Enhancements

- **Data Visualization Dashboard**: Charts and graphs for temporal analysis
- **Export Functionality**: PDF reports and CSV downloads
- **Mobile App**: React Native version for mobile users
- **Real-time Updates**: Webhook integration for automatic data updates
- **Advanced Filtering**: Date ranges, violation types, amount thresholds

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **City of Adelaide** - For providing open parking violation data
- **OpenStreetMap** - Free mapping tiles and geocoding services
- **React Community** - For excellent documentation and tools
- **Leaflet** - For the powerful, open-source mapping library

---

**Built with ❤️ for data transparency and public awareness**