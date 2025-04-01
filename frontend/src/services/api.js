import { newsEvents } from '../data/newsEvents';
import { klineData } from '../data/klineData';

// Transform kline data to match the expected format
const transformKlineData = (data) => {
  return data.map(item => ({
    date: item[0],
    open: item[1],
    close: item[2],
    low: item[3],
    high: item[4],
    volume: item[5] * 10000 // Convert 万手 to actual volume
  }));
};

// API functions using demo data
export const fetchNewsEvents = async () => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  return newsEvents;
};

export const fetchMarketData = async () => {
  // Simulate API delay
  await new Promise(resolve => setTimeout(resolve, 500));
  return transformKlineData(klineData);
}; 