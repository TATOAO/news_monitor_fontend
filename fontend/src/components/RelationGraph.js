import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { extractEntityNetwork } from '../utils/dataProcessor';
import './RelationGraph.css';

const RelationGraph = ({ events, selectedEvent }) => {
  const graphRef = useRef(null);
  
  useEffect(() => {
    if (!events || events.length === 0 || !graphRef.current) return;
    
    // Clear previous graph
    d3.select(graphRef.current).selectAll("*").remove();
    
    // Extract entity network
    const { nodes, links } = extractEntityNetwork(events);
    
    const width = graphRef.current.clientWidth;
    const height = graphRef.current.clientHeight;
    
    // Create SVG
    const svg = d3.select(graphRef.current)
      .append("svg")
      .attr("width", width)
      .attr("height", height);
    
    // Create force simulation
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id).distance(100))
      .force("charge", d3.forceManyBody().strength(-200))
      .force("center", d3.forceCenter(width / 2, height / 2))
      .force("collision", d3.forceCollide().radius(30));
    
    // Add links
    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .enter()
      .append("line")
      .attr("stroke", "#999")
      .attr("stroke-opacity", 0.6)
      .attr("stroke-width", d => Math.sqrt(d.value));
    
    // Add nodes
    const node = svg.append("g")
      .selectAll("g")
      .data(nodes)
      .enter()
      .append("g")
      .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended));
    
    // Add circles to nodes
    node.append("circle")
      .attr("r", d => d.type === 'event' ? 8 : 5)
      .attr("fill", d => {
        if (d.type === 'event') {
          return selectedEvent && d.id === selectedEvent.date ? "#e74c3c" : "#3498db";
        }
        return "#2ecc71";
      });
    
    // Add labels to nodes
    node.append("text")
      .attr("dx", 12)
      .attr("dy", ".35em")
      .text(d => d.name)
      .style("font-size", "10px");
    
    // Update positions on tick
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      
      node
        .attr("transform", d => `translate(${d.x},${d.y})`);
    });
    
    // Drag functions
    function dragstarted(event, d) {
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }
    
    function dragged(event, d) {
      d.fx = event.x;
      d.fy = event.y;
    }
    
    function dragended(event, d) {
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }
    
  }, [events, selectedEvent]);
  
  return (
    <div className="relation-graph">
      <h3>事件实体关系网络</h3>
      <div ref={graphRef} className="graph-container"></div>
    </div>
  );
};

export default RelationGraph; 