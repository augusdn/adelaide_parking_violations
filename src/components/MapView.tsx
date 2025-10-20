import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import { StreetData } from '../types';
import { dataService } from '../services/dataService';
import 'leaflet/dist/leaflet.css';

interface MapViewProps {
  streets: StreetData[];
  selectedStreet?: StreetData | null;
  onStreetSelect: (street: StreetData) => void;
}

const MapView: React.FC<MapViewProps> = ({ streets, selectedStreet, onStreetSelect }) => {
  // Adelaide CBD center coordinates
  const center: [number, number] = [-34.9285, 138.6007];
  
  // Calculate circle size based on fine amount
  const getCircleSize = (amount: number, maxAmount: number): number => {
    const minRadius = 5;
    const maxRadius = 25;
    const ratio = amount / maxAmount;
    return minRadius + (ratio * (maxRadius - minRadius));
  };

  // Get color based on fine amount
  const getCircleColor = (amount: number, maxAmount: number): string => {
    const ratio = amount / maxAmount;
    if (ratio > 0.8) return '#dc2626'; // red-600
    if (ratio > 0.6) return '#ea580c'; // orange-600
    if (ratio > 0.4) return '#d97706'; // amber-600
    if (ratio > 0.2) return '#ca8a04'; // yellow-600
    return '#65a30d'; // lime-600
  };

  const maxAmount = Math.max(...streets.map(s => s.totalFines));

  return (
    <div className="h-full w-full relative">
      <MapContainer
        center={center}
        zoom={13}
        className="h-full w-full"
        zoomControl={true}
      >
        <TileLayer
          attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        
        {streets.map((street, index) => (
          <CircleMarker
            key={`${street.street}-${index}`}
            center={[street.coordinates.lat, street.coordinates.lng]}
            radius={getCircleSize(street.totalFines, maxAmount)}
            fillColor={getCircleColor(street.totalFines, maxAmount)}
            color="#ffffff"
            weight={selectedStreet?.street === street.street ? 3 : 1}
            opacity={1}
            fillOpacity={0.7}
            eventHandlers={{
              click: () => onStreetSelect(street),
            }}
          >
            <Popup>
              <div className="min-w-[250px]">
                <h3 className="font-bold text-lg mb-2">{street.street}</h3>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span>Total Fines:</span>
                    <span className="font-semibold">{dataService.formatCurrency(street.totalFines)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Total Violations:</span>
                    <span className="font-semibold">{dataService.formatNumber(street.totalCount)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Average Fine:</span>
                    <span className="font-semibold">{dataService.formatCurrency(street.averageFine)}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Outstanding:</span>
                    <span className="font-semibold text-red-600">
                      {dataService.formatCurrency(street.outstandingBalance)}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Compliance Rate:</span>
                    <span className="font-semibold text-green-600">
                      {dataService.getPaymentComplianceRate(street).toFixed(1)}%
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => onStreetSelect(street)}
                  className="mt-3 w-full bg-primary-500 text-white px-3 py-1 rounded text-sm hover:bg-primary-600 transition-colors"
                >
                  View Details
                </button>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
      
      {/* Map Legend */}
      <div className="absolute bottom-4 left-4 bg-white p-3 rounded-lg shadow-lg z-[1000]">
        <h4 className="font-semibold text-sm mb-2">Fine Amount Legend</h4>
        <div className="space-y-1 text-xs">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-red-600"></div>
            <span>Highest (80%+)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-orange-600"></div>
            <span>High (60-80%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-amber-600"></div>
            <span>Medium (40-60%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-yellow-600"></div>
            <span>Low (20-40%)</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-lime-600"></div>
            <span>Lowest (&lt;20%)</span>
          </div>
        </div>
        <div className="mt-2 pt-2 border-t text-xs text-gray-600">
          Circle size = Fine amount
        </div>
      </div>
    </div>
  );
};

export default MapView;