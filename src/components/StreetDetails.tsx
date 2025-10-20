import React from 'react';
import { StreetData } from '../types';
import { dataService } from '../services/dataService';

interface StreetDetailsProps {
  street: StreetData | null;
  onClose: () => void;
}

const StreetDetails: React.FC<StreetDetailsProps> = ({ street, onClose }) => {
  if (!street) return null;

  const complianceRate = dataService.getPaymentComplianceRate(street);
  const topOffences = Object.entries(street.offenceTypes)
    .sort(([,a], [,b]) => b - a)
    .slice(0, 5);

  const statusEntries = Object.entries(street.statusBreakdown)
    .sort(([,a], [,b]) => b - a);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-[2000]">
      <div className="bg-white rounded-lg p-6 max-w-2xl w-full mx-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-start mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">{street.street}</h2>
            <p className="text-gray-600">
              {street.dateRange.first} to {street.dateRange.last}
            </p>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 text-2xl font-bold"
          >
            ×
          </button>
        </div>

        {/* Key Statistics */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-blue-50 p-4 rounded-lg">
            <div className="text-blue-600 text-sm font-medium">Total Fines</div>
            <div className="text-2xl font-bold text-blue-900">
              {dataService.formatCurrency(street.totalFines)}
            </div>
          </div>
          <div className="bg-purple-50 p-4 rounded-lg">
            <div className="text-purple-600 text-sm font-medium">Violations</div>
            <div className="text-2xl font-bold text-purple-900">
              {dataService.formatNumber(street.totalCount)}
            </div>
          </div>
          <div className="bg-green-50 p-4 rounded-lg">
            <div className="text-green-600 text-sm font-medium">Paid</div>
            <div className="text-2xl font-bold text-green-900">
              {dataService.formatCurrency(street.totalPaid)}
            </div>
          </div>
          <div className="bg-red-50 p-4 rounded-lg">
            <div className="text-red-600 text-sm font-medium">Outstanding</div>
            <div className="text-2xl font-bold text-red-900">
              {dataService.formatCurrency(street.outstandingBalance)}
            </div>
          </div>
        </div>

        {/* Additional Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="text-gray-600 text-sm font-medium">Average Fine Amount</div>
            <div className="text-xl font-bold text-gray-900">
              {dataService.formatCurrency(street.averageFine)}
            </div>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <div className="text-gray-600 text-sm font-medium">Payment Compliance Rate</div>
            <div className="text-xl font-bold text-gray-900">
              {complianceRate.toFixed(1)}%
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
              <div 
                className="bg-green-600 h-2 rounded-full"
                style={{ width: `${Math.min(complianceRate, 100)}%` }}
              ></div>
            </div>
          </div>
        </div>

        {/* Top Offence Types */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Top Violation Types</h3>
          <div className="space-y-2">
            {topOffences.map(([type, count]) => (
              <div key={type} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm font-medium text-gray-700 flex-1 mr-4">{type}</span>
                <span className="text-sm font-bold text-gray-900">
                  {dataService.formatNumber(count)} violations
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Status Breakdown */}
        <div className="mb-6">
          <h3 className="text-lg font-semibold mb-3">Payment Status Breakdown</h3>
          <div className="space-y-2">
            {statusEntries.map(([status, count]) => (
              <div key={status} className="flex justify-between items-center p-3 bg-gray-50 rounded">
                <span className="text-sm font-medium text-gray-700">{status}</span>
                <span className="text-sm font-bold text-gray-900">
                  {dataService.formatNumber(count)} cases
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* Close Button */}
        <div className="flex justify-end">
          <button
            onClick={onClose}
            className="bg-primary-500 text-white px-6 py-2 rounded-lg hover:bg-primary-600 transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
};

export default StreetDetails;