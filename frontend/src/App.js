import React, { useState, useEffect } from 'react';
import EventTimeline from './components/EventTimeline';
import EventDetail from './components/EventDetail';
import StockChart from './components/StockChart';
import RelationGraph from './components/RelationGraph';
import { processEventData, correlateEventsWithMarket } from './utils/dataProcessor';
import { fetchNewsEvents, fetchMarketData } from './services/api';
import './App.css';

function App() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [correlatedData, setCorrelatedData] = useState([]);
  const [marketData, setMarketData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch both news events and market data in parallel
        const [newsEventsData, marketDataData] = await Promise.all([
          fetchNewsEvents(),
          fetchMarketData()
        ]);

        // Process the raw event data
        const processedEvents = processEventData(newsEventsData);
        setEvents(processedEvents);
        setMarketData(marketDataData);
        
        // Set the first event as selected by default
        if (processedEvents.length > 0) {
          setSelectedEvent(processedEvents[0]);
        }
        
        // Correlate events with market data
        const correlatedEvents = correlateEventsWithMarket(processedEvents, marketDataData);
        setCorrelatedData(correlatedEvents);
      } catch (err) {
        setError('Failed to fetch data. Please try again later.');
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleEventSelect = (event) => {
    setSelectedEvent(event);
  };

  const handleDateSelect = (date) => {
    const event = events.find(e => e.date === date);
    if (event) {
      setSelectedEvent(event);
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>新闻事件脉络分析系统</h1>
      </header>
      <div className="app-content">
        <div className="left-panel">
          <EventTimeline 
            events={events} 
            onEventSelect={handleEventSelect} 
            selectedEvent={selectedEvent} 
          />
        </div>
        <div className="main-panel">
          <div className="top-section">
            <StockChart 
              chartData={marketData} 
              newsData={events}
            />
          </div>
          <div className="bottom-section">
            {selectedEvent && (
              <EventDetail 
                event={selectedEvent} 
                marketData={correlatedData.find(item => item.date === selectedEvent.date)}
              />
            )}
          </div>
        </div>
        <div className="right-panel">
          <RelationGraph events={events} selectedEvent={selectedEvent} />
        </div>
      </div>
    </div>
  );
}

export default App; 