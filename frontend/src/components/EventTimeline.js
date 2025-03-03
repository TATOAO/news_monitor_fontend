import React from 'react';
import './EventTimeline.css';

const EventTimeline = ({ events, onEventSelect, selectedEvent }) => {
  if (!events || events.length === 0) {
    return <div className="event-timeline-empty">加载中...</div>;
  }

  return (
    <div className="event-timeline">
      <h2>事件时间线</h2>
      <div className="timeline-container">
        <div className="timeline-line"></div>
        {events.map((event, index) => (
          <div 
            key={index}
            className={`timeline-item ${selectedEvent && selectedEvent.date === event.date ? 'selected' : ''}`}
            onClick={() => onEventSelect(event)}
          >
            <div className="timeline-dot"></div>
            <div className="timeline-date">{event.date}</div>
            <div className="timeline-content">
              <div className="timeline-title">{event.title}</div>
              <div className="timeline-relation">{event.relation}</div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventTimeline; 