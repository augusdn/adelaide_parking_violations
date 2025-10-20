// Type definitions for our data structures

export interface Coordinates {
  lat: number;
  lng: number;
}

export interface StreetData {
  street: string;
  coordinates: Coordinates;
  totalFines: number;
  totalCount: number;
  averageFine: number;
  outstandingBalance: number;
  totalPaid: number;
  offenceTypes: Record<string, number>;
  statusBreakdown: Record<string, number>;
  dateRange: {
    first: string;
    last: string;
  };
}

export interface TemporalData {
  monthly: MonthlyData[];
  hourly: HourlyData[];
  daily: DailyData[];
}

export interface MonthlyData {
  Year: number;
  Month: number;
  ExpiationAmount_sum: number;
  ExpiationAmount_count: number;
  OffenceBalance_sum: number;
  date: string;
}

export interface HourlyData {
  Hour: number;
  ExpiationAmount_sum: number;
  ExpiationAmount_count: number;
  ExpiationAmount_mean: number;
}

export interface DailyData {
  DayOfWeek: number;
  dayName: string;
  ExpiationAmount_sum: number;
  ExpiationAmount_count: number;
  ExpiationAmount_mean: number;
}

export interface OffenceTypeData {
  OffenceType: string;
  ExpiationAmount_sum: number;
  ExpiationAmount_count: number;
  ExpiationAmount_mean: number;
}

export interface SummaryStats {
  totalRecords: number;
  totalFines: number;
  totalOutstanding: number;
  totalPaid: number;
  averageFine: number;
  dateRange: {
    first: string;
    last: string;
  };
  uniqueStreets: number;
  lastUpdated: string;
}

export interface Filters {
  minAmount?: number;
  maxAmount?: number;
  dateRange?: {
    start: string;
    end: string;
  };
  offenceTypes?: string[];
  paymentStatus?: string[];
}