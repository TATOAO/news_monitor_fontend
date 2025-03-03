import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import './MarketChart.css';

const MarketChart = ({ klineData, events, selectedEvent, onDateSelect }) => {
  const chartRef = useRef(null);
  
  useEffect(() => {
    if (!klineData || klineData.length === 0 || !chartRef.current) return;
    
    // Clear previous chart
    d3.select(chartRef.current).selectAll("*").remove();
    
    const margin = { top: 20, right: 30, bottom: 50, left: 60 };
    const width = chartRef.current.clientWidth - margin.left - margin.right;
    const height = chartRef.current.clientHeight - margin.top - margin.bottom;
    
    // Create SVG
    const svg = d3.select(chartRef.current)
      .append("svg")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
      .append("g")
      .attr("transform", `translate(${margin.left},${margin.top})`);
    
    // Parse dates
    const parseDate = d3.timeParse("%Y-%m-%d");
    const data = klineData.map(d => ({
      date: parseDate(d[0]),
      open: +d[1],
      close: +d[2],
      high: +d[3],
      low: +d[4],
      volume: +d[5]
    }));
    
    // X scale
    const x = d3.scaleTime()
      .domain(d3.extent(data, d => d.date))
      .range([0, width]);
    
    // Y scale for price
    const y = d3.scaleLinear()
      .domain([d3.min(data, d => d.low) * 0.99, d3.max(data, d => d.high) * 1.01])
      .range([height, 0]);
    
    // Y scale for volume
    const yVolume = d3.scaleLinear()
      .domain([0, d3.max(data, d => d.volume)])
      .range([height * 0.8, 0]);
    
    // Add X axis
    svg.append("g")
      .attr("transform", `translate(0,${height})`)
      .call(d3.axisBottom(x).ticks(5))
      .selectAll("text")
      .style("text-anchor", "end")
      .attr("dx", "-.8em")
      .attr("dy", ".15em")
      .attr("transform", "rotate(-45)");
    
    // Add Y axis
    svg.append("g")
      .call(d3.axisLeft(y));
    
    // Add candlestick chart
    svg.selectAll("line.candlestick")
      .data(data)
      .enter()
      .append("line")
      .attr("class", "candlestick")
      .attr("x1", d => x(d.date))
      .attr("x2", d => x(d.date))
      .attr("y1", d => y(d.low))
      .attr("y2", d => y(d.high))
      .attr("stroke", "black")
      .attr("stroke-width", 1);
    
    svg.selectAll("rect.candlestick")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "candlestick")
      .attr("x", d => x(d.date) - 3)
      .attr("y", d => d.open > d.close ? y(d.open) : y(d.close))
      .attr("width", 6)
      .attr("height", d => Math.abs(y(d.open) - y(d.close)))
      .attr("fill", d => d.open > d.close ? "#e74c3c" : "#2ecc71");
    
    // Add volume bars
    svg.selectAll("rect.volume")
      .data(data)
      .enter()
      .append("rect")
      .attr("class", "volume")
      .attr("x", d => x(d.date) - 3)
      .attr("y", d => yVolume(d.volume))
      .attr("width", 6)
      .attr("height", d => Math.max(0, height * 0.8 - yVolume(d.volume)))
      .attr("fill", "#3498db")
      .attr("opacity", 0.5);
    
    // Add event markers
    if (events && events.length > 0) {
      const eventDates = events.map(e => e.date);
      const eventData = data.filter(d => {
        const dateStr = d3.timeFormat("%Y-%m-%d")(d.date);
        return eventDates.includes(dateStr);
      });
      
      svg.selectAll("circle.event-marker")
        .data(eventData)
        .enter()
        .append("circle")
        .attr("class", "event-marker")
        .attr("cx", d => x(d.date))
        .attr("cy", d => y(d.high) - 10)
        .attr("r", 5)
        .attr("fill", d => {
          const dateStr = d3.timeFormat("%Y-%m-%d")(d.date);
          return selectedEvent && selectedEvent.date === dateStr ? "#e74c3c" : "#f39c12";
        })
        .style("cursor", "pointer")
        .on("click", (event, d) => {
          const dateStr = d3.timeFormat("%Y-%m-%d")(d.date);
          onDateSelect(dateStr);
        });
    }
    
    // Add selected event highlight
    if (selectedEvent) {
      const selectedDate = parseDate(selectedEvent.date);
      const selectedDataPoint = data.find(d => {
        return d3.timeFormat("%Y-%m-%d")(d.date) === selectedEvent.date;
      });
      
      if (selectedDataPoint) {
        svg.append("line")
          .attr("class", "selected-event-line")
          .attr("x1", x(selectedDataPoint.date))
          .attr("x2", x(selectedDataPoint.date))
          .attr("y1", 0)
          .attr("y2", height)
          .attr("stroke", "#e74c3c")
          .attr("stroke-width", 1)
          .attr("stroke-dasharray", "5,5");
      }
    }
    
  }, [klineData, events, selectedEvent, onDateSelect]);
  
  return (
    <div className="market-chart">
      <h3>市场走势与事件关联</h3>
      <div className="chart-legend">
        <div className="candlestick-up">上涨</div>
        <div className="candlestick-down">下跌</div>
        <div className="event-marker">事件</div>
      </div>
      <div ref={chartRef} className="chart-container"></div>
    </div>
  );
};

export default MarketChart; 