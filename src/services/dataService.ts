import { StreetData, TemporalData, OffenceTypeData, SummaryStats } from '../types';

class DataService {
  private cache = new Map<string, any>();

  private async fetchJson<T>(path: string): Promise<T> {
    if (this.cache.has(path)) {
      return this.cache.get(path);
    }

    try {
      // Use relative path that works in both dev and production
      const url = `./data/${path}`;
      console.log(`Fetching data from: ${url}`);
      
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }
      
      const data = await response.json();
      this.cache.set(path, data);
      console.log(`Successfully loaded ${path}`);
      return data;
    } catch (error) {
      console.error(`Error loading ${path}:`, error);
      console.error(`Current URL: ${window.location.href}`);
      throw new Error(`Failed to load ${path}. Please check the console for details.`);
    }
  }

  async getStreetData(): Promise<StreetData[]> {
    return this.fetchJson<StreetData[]>('streets.json');
  }

  async getTemporalData(): Promise<TemporalData> {
    return this.fetchJson<TemporalData>('temporal.json');
  }

  async getOffenceData(): Promise<OffenceTypeData[]> {
    return this.fetchJson<OffenceTypeData[]>('offences.json');
  }

  async getSummaryStats(): Promise<SummaryStats> {
    return this.fetchJson<SummaryStats>('summary.json');
  }

  // Utility functions for data filtering and processing
  filterStreetData(streets: StreetData[], filters: {
    minAmount?: number;
    maxAmount?: number;
    searchTerm?: string;
  }): StreetData[] {
    return streets.filter(street => {
      if (filters.minAmount && street.totalFines < filters.minAmount) return false;
      if (filters.maxAmount && street.totalFines > filters.maxAmount) return false;
      if (filters.searchTerm && !street.street.toLowerCase().includes(filters.searchTerm.toLowerCase())) return false;
      return true;
    });
  }

  formatCurrency(amount: number): string {
    return new Intl.NumberFormat('en-AU', {
      style: 'currency',
      currency: 'AUD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(amount);
  }

  formatNumber(num: number): string {
    return new Intl.NumberFormat('en-AU').format(num);
  }

  getTop10Streets(streets: StreetData[]): StreetData[] {
    return streets
      .sort((a, b) => b.totalFines - a.totalFines)
      .slice(0, 10);
  }

  getPaymentComplianceRate(street: StreetData): number {
    const totalAmount = street.totalFines;
    const paidAmount = street.totalPaid;
    return totalAmount > 0 ? (paidAmount / totalAmount) * 100 : 0;
  }
}

export const dataService = new DataService();