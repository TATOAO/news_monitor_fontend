import React, { useState, useEffect } from 'react';
import EventTimeline from './components/EventTimeline';
import EventDetail from './components/EventDetail';
import StockChart from './components/StockChart';
import RelationGraph from './components/RelationGraph';
import { newsEvents } from './data/newsEvents';
import { klineData } from './data/klineData';
import { processEventData, correlateEventsWithMarket } from './utils/dataProcessor';
import './App.css';

function App() {
  const [events, setEvents] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [correlatedData, setCorrelatedData] = useState([]);

  useEffect(() => {
    // Process the raw event data
    const processedEvents = processEventData(newsEvents);
    setEvents(processedEvents);
    
    // Set the first event as selected by default
    if (processedEvents.length > 0) {
      setSelectedEvent(processedEvents[0]);
    }
    
    // Correlate events with market data
    const correlatedEvents = correlateEventsWithMarket(processedEvents, klineData);
    setCorrelatedData(correlatedEvents);
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
              chartData={klineData} 
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