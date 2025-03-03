import React from 'react';
import './EventDetail.css';

const EventDetail = ({ event, marketData }) => {
  if (!event) return <div className="event-detail">请选择一个事件</div>;

  const priceChange = marketData ? Number(marketData.priceChange) || 0 : 0;
  const priceChangeClass = priceChange > 0 ? 'positive' : priceChange < 0 ? 'negative' : '';
  
  return (
    <div className="event-detail">
      <div className="event-header">
        <h2 className="event-title">{event.title}</h2>
        <div className="event-date">{event.date}</div>
      </div>
      
      <div className="event-content">
        {event.content}
      </div>
      
      <div className="event-meta">
        <div className="relation-type">
          <strong>事件关系:</strong> {event.relation}
        </div>
        
        <div className="entity-tags">
          <strong>相关实体:</strong>
          {event.entities && event.entities.length > 0 ? (
            event.entities.map((entity, index) => (
              <span key={index} className="entity-tag">{entity}</span>
            ))
          ) : (
            <span className="entity-tag empty">无</span>
          )}
        </div>
        
        {marketData && (
          <div className="market-impact">
            <strong>市场影响:</strong>
            <div className={`price-change ${priceChangeClass}`}>
              {priceChange > 0 ? '+' : ''}{priceChange.toFixed(2)}%
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EventDetail; 