import React, { useState, useEffect } from 'react';
import MapView from './components/MapView';
import StreetDetails from './components/StreetDetails';
import { StreetData, SummaryStats } from './types';
import { dataService } from './services/dataService';

const App: React.FC = () => {
  const [streets, setStreets] = useState<StreetData[]>([]);
  const [filteredStreets, setFilteredStreets] = useState<StreetData[]>([]);
  const [selectedStreet, setSelectedStreet] = useState<StreetData | null>(null);
  const [summaryStats, setSummaryStats] = useState<SummaryStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState('');
  const [showTopStreets, setShowTopStreets] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  useEffect(() => {
    // Filter streets based on search term
    const filtered = dataService.filterStreetData(streets, { searchTerm });
    setFilteredStreets(filtered);
  }, [streets, searchTerm]);

  const loadData = async () => {
    try {
      setLoading(true);
      const [streetsData, summaryData] = await Promise.all([
        dataService.getStreetData(),
        dataService.getSummaryStats()
      ]);
      
      setStreets(streetsData);
      setFilteredStreets(streetsData);
      setSummaryStats(summaryData);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load data');
    } finally {
      setLoading(false);
    }
  };

  const handleStreetSelect = (street: StreetData) => {
    setSelectedStreet(street);
  };

  const handleCloseDetails = () => {
    setSelectedStreet(null);
  };

  const toggleTopStreets = () => {
    if (showTopStreets) {
      setFilteredStreets(dataService.filterStreetData(streets, { searchTerm }));
    } else {
      const topStreets = dataService.getTop10Streets(streets);
      setFilteredStreets(topStreets);
    }
    setShowTopStreets(!showTopStreets);
  };

  if (loading) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading parking violation data...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="h-screen flex items-center justify-center bg-gray-100">
        <div className="text-center">
          <div className="text-red-500 text-6xl mb-4">⚠️</div>
          <h2 className="text-2xl font-bold text-gray-900 mb-2">Error Loading Data</h2>
          <p className="text-gray-600 mb-4">{error}</p>
          <button
            onClick={loadData}
            className="bg-primary-500 text-white px-6 py-2 rounded-lg hover:bg-primary-600 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex flex-col bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="px-4 py-3">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                Adelaide Parking Violations Map
              </h1>
              {summaryStats && (
                <p className="text-sm text-gray-600">
                  {dataService.formatNumber(summaryStats.totalRecords)} violations • 
                  {dataService.formatCurrency(summaryStats.totalFines)} total fines • 
                  {summaryStats.uniqueStreets} streets • 
                  Data: {summaryStats.dateRange.first} to {summaryStats.dateRange.last}
                </p>
              )}
            </div>
            
            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search streets..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="pl-4 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none w-full sm:w-64"
                />
              </div>
              
              <button
                onClick={toggleTopStreets}
                className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                  showTopStreets
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                }`}
              >
                {showTopStreets ? 'Show All' : 'Top 10'}
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 relative">
        <MapView
          streets={filteredStreets}
          selectedStreet={selectedStreet}
          onStreetSelect={handleStreetSelect}
        />
        
        {/* Quick Stats Panel */}
        {summaryStats && (
          <div className="absolute top-4 right-4 bg-white p-4 rounded-lg shadow-lg z-[1000] min-w-[280px]">
            <h3 className="font-bold text-lg mb-3">Quick Statistics</h3>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span>Showing Streets:</span>
                <span className="font-semibold">{filteredStreets.length}</span>
              </div>
              <div className="flex justify-between">
                <span>Total Fines:</span>
                <span className="font-semibold">{dataService.formatCurrency(summaryStats.totalFines)}</span>
              </div>
              <div className="flex justify-between">
                <span>Outstanding:</span>
                <span className="font-semibold text-red-600">
                  {dataService.formatCurrency(summaryStats.totalOutstanding)}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Collection Rate:</span>
                <span className="font-semibold text-green-600">
                  {((summaryStats.totalPaid / summaryStats.totalFines) * 100).toFixed(1)}%
                </span>
              </div>
            </div>
            <div className="mt-3 pt-3 border-t text-xs text-gray-500">
              Last updated: {new Date(summaryStats.lastUpdated).toLocaleDateString()}
            </div>
          </div>
        )}
      </main>

      {/* Street Details Modal */}
      <StreetDetails
        street={selectedStreet}
        onClose={handleCloseDetails}
      />
    </div>
  );
};

export default App;