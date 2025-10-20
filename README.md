# Adelaide Parking Violations Map

An interactive web application that visualizes parking violation data across Adelaide's Central Business District (CBD). This project aggregates and maps parking fines by street, providing insights into parking enforcement patterns and revenue generation.

## 🚀 Live Demo

**[View the Interactive Map](https://augusdn.github.io/adelaide_parking_violations/)**

## 📊 Key Features

- **Interactive Street-Level Mapping**: Explore 576 streets with color-coded fine aggregations
- **Comprehensive Data Visualization**: View $23.7M+ in total parking fines
- **High-Precision Geocoding**: 100% accuracy for Adelaide CBD street positioning
- **Revenue Analytics**: Identify top revenue-generating streets and areas
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Real-time Filtering**: Search and filter streets by name or fine amounts

## 🗺️ Data Overview

- **979,347** parking violation records processed
- **576** unique streets mapped in Adelaide CBD
- **$23.7M+** total fines visualized
- **Perfect geocoding accuracy** with strict CBD boundaries

### Top Revenue Streets:
- King William Street: $2.03M
- Flinders Street: $2.03M
- Angas Street: $1.71M
- Grenfell Street: $1.42M
- Rundle Mall: $1.15M

## 🛠️ Technology Stack

- **Frontend**: React 18 + TypeScript
- **Mapping**: Leaflet + React-Leaflet
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Data Processing**: Python + Pandas
- **Geocoding**: Nominatim with enhanced CBD boundaries
- **Deployment**: GitHub Pages with GitHub Actions

## 📁 Project Structure

```
adelaide_parking_violations/
├── src/                          # React application source
│   ├── components/              # React components
│   │   ├── MapView.tsx         # Main map interface
│   │   └── StreetDetails.tsx   # Street detail panels
│   ├── services/               # Data services
│   └── types/                  # TypeScript definitions
├── public/data/                # Processed data files
│   ├── streets.json           # Street-level aggregated data
│   ├── summary.json           # Overall statistics
│   ├── temporal.json          # Time-based analysis
│   └── offences.json          # Offense type breakdown
├── scripts/                   # Data processing scripts
│   ├── process_data.py        # Main data processor
│   └── requirements.txt       # Python dependencies
├── data/                      # Raw data storage
└── .github/workflows/         # CI/CD automation
```

## 🚀 Getting Started

### Prerequisites

- Node.js 18+ and npm
- Python 3.11+
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/augusdn/adelaide_parking_violations.git
   cd adelaide_parking_violations
   ```

2. **Install Node.js dependencies**
   ```bash
   npm install
   ```

3. **Set up Python environment**
   ```bash
   cd scripts
   pip install -r requirements.txt
   cd ..
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:3000`

## 📊 Adding New Dataset

### Method 1: Local Processing (Recommended)

This method processes data locally and only commits the processed JSON files, avoiding large file issues:

1. **Replace the CSV file**
   ```bash
   # Place your new CSV file in the data/ directory
   cp /path/to/new/Parking_Expiations.csv data/
   ```

2. **Process the data locally**
   ```bash
   # Activate Python environment if needed
   python scripts/process_data.py
   ```

3. **Verify the processed data**
   ```bash
   # Check the generated JSON files
   ls -la public/data/
   ```

4. **Test locally**
   ```bash
   npm run dev
   # Verify the map loads correctly with new data
   ```

5. **Commit only the processed data**
   ```bash
   git add public/data/*.json
   git commit -m "Update parking violations data - [DATE]"
   git push
   ```

6. **Automatic deployment**
   - GitHub Actions will automatically build and deploy
   - Check the Actions tab for deployment status
   - Site updates in 2-3 minutes

### Method 2: Git LFS (For Automation)

If you want to automate the entire process and store large CSV files:

1. **Set up Git LFS (one-time)**
   ```bash
   git lfs install
   git lfs track "data/*.csv"
   git add .gitattributes
   git commit -m "Add LFS tracking for CSV files"
   ```

2. **Add new CSV and push**
   ```bash
   cp /path/to/new/Parking_Expiations.csv data/
   git add data/Parking_Expiations.csv
   git commit -m "Add new parking data via LFS"
   git push
   ```

3. **GitHub Actions handles the rest**
   - Automatically processes data
   - Builds and deploys the application

## 🔧 Data Processing Details

The `process_data.py` script includes several advanced features:

### Enhanced Geocoding
- **Strict CBD Boundaries**: Ensures all streets are within Adelaide CBD coordinates
- **Specific Street Coordinates**: Pre-defined coordinates for major streets
- **Fallback Mechanisms**: Multiple geocoding strategies for accuracy
- **Cache Management**: Efficient caching to avoid redundant API calls

### Data Aggregation
- **Street-level totals**: Aggregates fines by street name
- **Temporal analysis**: Monthly and yearly trends
- **Offense categorization**: Groups by violation types
- **Revenue calculations**: Converts penalty units to dollar amounts

### Quality Assurance
- **Coordinate validation**: Ensures all coordinates are within Adelaide CBD
- **Data consistency checks**: Validates penalty amounts and dates
- **Duplicate handling**: Removes or merges duplicate records

## 🏗️ Building and Deployment

### Local Build
```bash
npm run build
npm run preview  # Test the production build
```

### Manual Deployment
```bash
npm run deploy  # Uses gh-pages package
```

### Automatic Deployment (Current Setup)
- **Trigger**: Push to `main` branch
- **Process**: GitHub Actions builds and deploys automatically
- **URL**: https://augusdn.github.io/adelaide_parking_violations/

## 📈 Data Sources

The application processes data from:
- **Parking_Expiations.csv**: Main parking violation records
- **Parking_Expiations_Field_Values.csv**: Field definitions and penalty rates

### Expected CSV Format
```csv
Date Issued,Street Name,Penalty Amount,Offense Code,...
2023-01-01,King William Street,200,123,...
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Adelaide City Council for providing the parking violation data
- OpenStreetMap community for geographic data
- Nominatim service for geocoding capabilities

## 🐛 Troubleshooting

### Common Issues

1. **Map not loading**
   - Check browser console for errors
   - Verify data files exist in `public/data/`
   - Ensure correct base path in `vite.config.ts`

2. **Geocoding issues**
   - Run `python scripts/process_data.py` to reprocess
   - Check internet connection for Nominatim API
   - Verify coordinate boundaries in processing script

3. **Deployment failures**
   - Check GitHub Actions logs
   - Ensure all dependencies are listed in package.json
   - Verify build process with `npm run build`

### Support

For issues or questions:
- Open an issue on GitHub
- Check the Actions tab for deployment logs
- Review the console output during local development

---

**Made with ❤️ for Adelaide's parking transparency**
