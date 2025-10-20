import React, { useState, useEffect } from 'react';
import { Calendar } from 'lucide-react';

interface DateRangePickerProps {
  startDate: string;
  endDate: string;
  minDate: string;
  maxDate: string;
  onDateRangeChange: (startDate: string, endDate: string) => void;
}

const DateRangePicker: React.FC<DateRangePickerProps> = ({
  startDate,
  endDate,
  minDate,
  maxDate,
  onDateRangeChange,
}) => {
  const [localStartDate, setLocalStartDate] = useState(startDate);
  const [localEndDate, setLocalEndDate] = useState(endDate);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    setLocalStartDate(startDate);
    setLocalEndDate(endDate);
  }, [startDate, endDate]);

  const handleApply = () => {
    // Validate that start date is before end date
    if (new Date(localStartDate) > new Date(localEndDate)) {
      alert('Start date must be before end date');
      return;
    }
    onDateRangeChange(localStartDate, localEndDate);
    setIsOpen(false);
  };

  const handleReset = () => {
    setLocalStartDate(minDate);
    setLocalEndDate(maxDate);
    onDateRangeChange(minDate, maxDate);
    setIsOpen(false);
  };

  const formatDateForDisplay = (date: string): string => {
    return new Date(date).toLocaleDateString('en-AU', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
    });
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
        aria-label="Select date range"
      >
        <Calendar size={18} />
        <span className="text-sm font-medium">
          {formatDateForDisplay(startDate)} - {formatDateForDisplay(endDate)}
        </span>
      </button>

      {isOpen && (
        <>
          {/* Backdrop */}
          <div
            className="fixed inset-0 z-40"
            onClick={() => setIsOpen(false)}
          />

          {/* Dropdown */}
          <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 z-50">
            <div className="p-4">
              <h3 className="font-semibold text-lg mb-4">Select Date Range</h3>
              
              <div className="space-y-4">
                <div>
                  <label htmlFor="start-date" className="block text-sm font-medium text-gray-700 mb-1">
                    Start Date
                  </label>
                  <input
                    id="start-date"
                    type="date"
                    value={localStartDate}
                    min={minDate}
                    max={maxDate}
                    onChange={(e) => setLocalStartDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                  />
                </div>

                <div>
                  <label htmlFor="end-date" className="block text-sm font-medium text-gray-700 mb-1">
                    End Date
                  </label>
                  <input
                    id="end-date"
                    type="date"
                    value={localEndDate}
                    min={minDate}
                    max={maxDate}
                    onChange={(e) => setLocalEndDate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none"
                  />
                </div>
              </div>

              <div className="mt-4 pt-4 border-t flex gap-2">
                <button
                  onClick={handleReset}
                  className="flex-1 px-4 py-2 text-sm font-medium text-gray-700 bg-gray-100 rounded-md hover:bg-gray-200 transition-colors"
                >
                  Reset
                </button>
                <button
                  onClick={handleApply}
                  className="flex-1 px-4 py-2 text-sm font-medium text-white bg-primary-500 rounded-md hover:bg-primary-600 transition-colors"
                >
                  Apply
                </button>
              </div>

              <div className="mt-3 text-xs text-gray-500">
                Available data: {formatDateForDisplay(minDate)} to {formatDateForDisplay(maxDate)}
              </div>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default DateRangePicker;
