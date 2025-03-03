import React from 'react';
import ReactECharts from 'echarts-for-react';
import './StockChart.css';

const StockChart = ({ chartData, newsData }) => {
  // Prepare news markers data
  const newsMarkers = newsData?.map(news => ({
    xAxis: news.date,
    itemStyle: {
      color: '#FFA726',
      opacity: 0.3
    }
  })) || [];

  const option = {
    dataset: {
      source: chartData,
      dimensions: ['date', 'open', 'close', 'low', 'high', 'volume']
    },
    title: {
      text: chartData?.title || 'Stock Chart',
      left: 'center'
    },
    grid: [
      {
        top: '10%',
        height: '55%',
        left: '10%',
        right: '8%'
      },
      {
        top: '65%',
        height: '10%',
        left: '10%',
        right: '8%'
      }
    ],
    xAxis: [
      {
        type: 'category',
        gridIndex: 0,
        scale: true,
        boundaryGap: true,
        axisLine: { onZero: false },
        splitLine: { show: false },
        axisTick: { show: false },
        axisLabel: { show: false },
        zlevel: 1
      },
      {
        type: 'category',
        gridIndex: 1,
        scale: true,
        boundaryGap: true,
        axisLine: { onZero: false },
        axisTick: { show: false },
        splitLine: { show: false },
        axisLabel: {
          formatter: function(value) {
            const hasNews = newsData?.some(news => news.date === value);
            return hasNews ? value + ' •' : value;
          },
          rich: {
            news: {
              color: '#FFA726',
              fontWeight: 'bold'
            }
          }
        },
        zlevel: 1
      }
    ],
    yAxis: [
      {
        scale: true,
        gridIndex: 0,
        splitArea: {
          show: true
        }
      },
      {
        scale: true,
        gridIndex: 1,
        splitNumber: 2,
        min: 0,
        axisLabel: { show: true },
        axisLine: { show: false },
        axisTick: { show: false },
        splitLine: { show: false }
      }
    ],
    series: [
      {
        type: 'candlestick',
        encode: {
          x: 'date',
          y: ['open', 'close', 'low', 'high']
        },
        itemStyle: {
          color: '#ef232a',
          color0: '#14b143',
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        },
        markLine: {
          silent: true,
          zlevel: 0,
          data: newsMarkers.map(marker => ({
            xAxis: marker.xAxis,
            lineStyle: {
              color: '#FFA726',
              opacity: 0.3,
              type: 'solid',
              width: 2
            }
          }))
        }
      },
      {
        type: 'bar',
        xAxisIndex: 1,
        yAxisIndex: 1,
        encode: {
          x: 'date',
          y: 'volume'
        },
        barWidth: '60%',
        itemStyle: {
          color: function(params) {
            const data = params.data;
            const hasNews = newsData?.some(news => news.date === data[0]);
            
            if (hasNews) {
              const priceChange = data[2] - data[1]; // close - open
              if (priceChange > 0) {
                return {
                  color: getComputedStyle(document.documentElement).getPropertyValue('--volume-up-color').trim(),
                  opacity: parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--volume-up-opacity')),
                  shadowBlur: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--volume-up-shadow-blur')),
                  shadowColor: getComputedStyle(document.documentElement).getPropertyValue('--volume-up-shadow-color').trim()
                };
              } else {
                return {
                  color: getComputedStyle(document.documentElement).getPropertyValue('--volume-down-color').trim(),
                  opacity: parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--volume-down-opacity')),
                  shadowBlur: parseInt(getComputedStyle(document.documentElement).getPropertyValue('--volume-down-shadow-blur')),
                  shadowColor: getComputedStyle(document.documentElement).getPropertyValue('--volume-down-shadow-color').trim()
                };
              }
            } else {
              return {
                color: getComputedStyle(document.documentElement).getPropertyValue('--volume-no-news-color').trim(),
                opacity: parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--volume-no-news-opacity'))
              };
            }
          }
        },
        markLine: {
          silent: true,
          zlevel: 0,
          data: newsMarkers.map(marker => ({
            xAxis: marker.xAxis,
            lineStyle: {
              color: '#FFA726',
              opacity: 0.3,
              type: 'solid',
              width: 2
            }
          }))
        }
      }
    ],
    dataZoom: [
      {
        type: 'inside',
        xAxisIndex: [0, 1],
        start: 0,
        end: 100
      },
      {
        type: 'slider',
        xAxisIndex: [0, 1],
        bottom: 10
      }
    ],
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross'
      },
      formatter: function(params) {
        const data = params[0].data;
        const date = data[0];
        
        // Find news for this date
        const newsForDate = newsData?.find(news => news.date === date);
        
        let tooltipContent = `
          Date: ${date}<br/>
          Open: ${data[1]}<br/>
          Close: ${data[2]}<br/>
          Low: ${data[3]}<br/>
          High: ${data[4]}<br/>
          Volume: ${data[5]}
        `;
        
        // Add news title if available
        if (newsForDate) {
          tooltipContent += `<br/><br/>News: ${newsForDate.title}`;
        }
        
        return tooltipContent;
      }
    }
  };

  return (
    <div className="stock-chart-container" style={{ width: '1000px', height: '600px' }}>
      <ReactECharts 
        option={option}
        style={{ height: '100%', width: '100%' }}
        opts={{ renderer: 'canvas' }}
      />
    </div>
  );
};

export default StockChart; 