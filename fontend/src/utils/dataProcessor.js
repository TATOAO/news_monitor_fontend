// 处理事件数据，添加关联关系
export const processEventData = (events) => {
  if (!events || events.length === 0) return [];
  
  return events.map(event => ({
    ...event,
    // Add any additional processing here
    timestamp: new Date(event.date).getTime(),
    // Ensure entities is always an array
    entities: event.entities || []
  })).sort((a, b) => a.timestamp - b.timestamp);
};

// 根据关系类型对事件进行分类
export const categorizeEvents = (events) => {
  if (!events || events.length === 0) return {};
  
  const categories = {
    positive: [],
    negative: [],
    neutral: []
  };
  
  events.forEach(event => {
    if (['技术演进', '生态扩展', '政策背书', '里程碑', '成果落地'].includes(event.relation)) {
      categories.positive.push(event);
    } else if (['外部压力', '风险事件', '政治阻力'].includes(event.relation)) {
      categories.negative.push(event);
    } else {
      categories.neutral.push(event);
    }
  });
  
  return categories;
};

// 将事件与K线数据关联
export const correlateEventsWithMarket = (events, klineData) => {
  return events.map(event => {
    const eventDate = new Date(event.date);
    const marketData = klineData.find(data => {
      return new Date(data[0]).toDateString() === eventDate.toDateString();
    });
    
    return {
      ...event,
      marketData: marketData || null,
      priceChange: marketData ? ((marketData[2] - marketData[1]) / marketData[1] * 100).toFixed(2) : null
    };
  });
};

// 提取实体关系网络
export const extractEntityNetwork = (events) => {
  const entities = new Set();
  const connections = [];
  
  // 收集所有实体
  events.forEach(event => {
    event.entities.forEach(entity => entities.add(entity));
  });
  
  // 建立实体间的连接（如果它们出现在相邻事件中）
  for (let i = 0; i < events.length - 1; i++) {
    const currentEvent = events[i];
    const nextEvent = events[i + 1];
    
    currentEvent.entities.forEach(entity1 => {
      nextEvent.entities.forEach(entity2 => {
        if (entity1 !== entity2) {
          connections.push({
            source: entity1,
            target: entity2,
            strength: 1,
            eventIds: [currentEvent.id, nextEvent.id]
          });
        }
      });
    });
  }
  
  return {
    nodes: Array.from(entities).map(name => ({ id: name, name })),
    links: connections
  };
}; 