# News Monitor Frontend

This is a React-based frontend application for monitoring news events and their correlation with market data.

## Prerequisites

Before you begin, ensure you have the following installed on your system:
- Node.js (version 14.x or higher)
- npm (version 6.x or higher) or yarn (version 1.x or higher)

You can check your current versions with:
```bash
node -v
npm -v
# or
yarn -v
```

## Getting Started

Follow these steps to set up and run the application locally:

### 1. Clone the repository

```bash
git clone <repository-url>
cd news_monitor/webapp/fontend
```

### 2. Install dependencies

Using npm:
```bash
npm install
```

Or using yarn:
```bash
yarn install
```

### 3. Start the development server

Using npm:
```bash
npm start
```

Or using yarn:
```bash
yarn start
```

This will start the development server and open the application in your default web browser at [http://localhost:3000](http://localhost:3000).

## Available Scripts

In the project directory, you can run:

### `npm start` or `yarn start`

Runs the app in development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in your browser.

The page will reload when you make changes.\
You may also see any lint errors in the console.

### `npm test` or `yarn test`

Launches the test runner in the interactive watch mode.

### `npm run build` or `yarn build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

## Project Structure

- `src/components/`: Contains all React components
- `src/data/`: Contains data files for news events and market data
- `src/utils/`: Contains utility functions for data processing
- `public/`: Contains static assets and the HTML template

## Features

- Event Timeline: Visualize news events on a timeline
- Event Detail: View detailed information about selected events
- Market Chart: View market data and its correlation with news events
- Relation Graph: Visualize relationships between different entities

## Learn More

To learn more about React, check out the [React documentation](https://reactjs.org/).

# Prompts 
我需设计一个新闻事件脉络分析系统前端，请以数据结构专家的身份提供架构建议。需求背景如下：

1. 数据特征：
- 每日接收N条金融/国际政治/热点事件类新闻
- 新闻具有事件延续性（同主题多阶段报道）
- 需实现跨时间的事件关联与脉络整合

2. 核心诉求：
- 设计可实现时空关联的数据结构
- 支持动态事件演化追踪机制
- 生成带语义关联的时间轴视图

const newsEvents = [
  { date: "2024-05-07",
    title: "A国央行宣布启动数字货币研究项目",
    content: "A国财政部长表示将在6个月内完成技术验证...",
    entities: ["A国央行", "数字货币"],
    relation: "事件起点" },

  { date: "2024-05-11",
    title: "国际清算银行警告数字货币风险",
    content: "BIS报告指出A国方案可能影响跨境支付体系...",
    entities: ["BIS"],
    relation: "外部压力" },

  { date: "2024-05-16",
    title: "A国公布数字法币技术白皮书",
    content: "采用混合区块链架构，保留央行控制权...",
    entities: ["区块链"],
    relation: "技术演进" },

  { date: "2024-05-21",
    title: "跨国银行联盟宣布兼容A国标准",
    content: "JP摩根、汇丰等20家机构签署技术协议...",
    entities: ["JP摩根", "汇丰"],
    relation: "生态扩展" },

  { date: "2024-05-24",
    title: "A国数字货币试点现技术漏洞",
    content: "压力测试中发现双花攻击漏洞...",
    entities: [],
    relation: "风险事件" },

  { date: "2024-05-26",
    title: "央行紧急升级智能合约模块",
    content: "引入零知识证明强化隐私保护...",
    entities: ["智能合约"],
    relation: "技术迭代" },

  { date: "2024-05-28",
    title: "国际货币基金组织表态支持",
    content: "IMF认为有助于提升金融监管效率...",
    entities: ["IMF"],
    relation: "政策背书" },

  { date: "2024-05-31",
    title: "反对党质疑项目透明度",
    content: "国会听证会要求公开技术审计报告...",
    entities: ["国会"],
    relation: "政治阻力" },

  { date: "2024-06-02",
    title: "央行数字法币首次跨境结算测试成功",
    content: "与C国完成1亿美元实时转账...",
    entities: ["C国"],
    relation: "里程碑" },

  { date: "2024-06-05",
    title: "A国宣布正式发行数字法币",
    content: "第一阶段覆盖大额机构交易...",
    entities: [],
    relation: "成果落地" }
]



kline_data = [
    # 格式: [date, open, close, high, low, volume(万手)]
    ["2024-05-07", 3250, 3265, 3280, 3240, 150],
    ["2024-05-08", 3265, 3270, 3285, 3250, 140],
    ["2024-05-09", 3270, 3260, 3290, 3255, 130],
    ["2024-05-10", 3260, 3255, 3275, 3245, 120],
    ["2024-05-11", 3280, 3200, 3285, 3180, 450],  # 国际机构警告
    ["2024-05-12", 3200, 3210, 3220, 3190, 160],
    ["2024-05-13", 3210, 3220, 3230, 3200, 170],
    ["2024-05-14", 3220, 3230, 3240, 3210, 180],
    ["2024-05-15", 3230, 3240, 3250, 3220, 190],
    ["2024-05-16", 3220, 3300, 3320, 3205, 380], # 白皮书发布
    ["2024-05-17", 3300, 3310, 3320, 3290, 200],
    ["2024-05-18", 3310, 3320, 3330, 3300, 210],
    ["2024-05-19", 3320, 3330, 3340, 3310, 220],
    ["2024-05-20", 3330, 3340, 3350, 3320, 230],
    ["2024-05-21", 3350, 3400, 3420, 3340, 420], # 银行联盟支持
    ["2024-05-22", 3400, 3410, 3420, 3390, 240],
    ["2024-05-23", 3410, 3420, 3430, 3400, 250],
    ["2024-05-24", 3420, 3330, 3425, 3300, 600], # 漏洞事件
    ["2024-05-25", 3330, 3320, 3340, 3310, 260],
    ["2024-05-26", 3320, 3380, 3400, 3300, 520], # 漏洞修复
    ["2024-05-27", 3380, 3400, 3410, 3370, 270],
    ["2024-05-28", 3400, 3450, 3460, 3390, 400], # IMF背书
    ["2024-05-29", 3450, 3460, 3470, 3440, 280],
    ["2024-05-30", 3460, 3420, 3465, 3400, 480], # 政治争议
    ["2024-05-31", 3420, 3430, 3440, 3410, 290],
    ["2024-06-01", 3430, 3440, 3450, 3420, 300],
    ["2024-06-02", 3430, 3500, 3520, 3420, 650], # 跨境测试成功
    ["2024-06-03", 3500, 3510, 3520, 3490, 310],
    ["2024-06-04", 3510, 3520, 3530, 3500, 320],
    ["2024-06-05", 3520, 3600, 3620, 3510, 800]  # 正式发行
]


请结合典型新闻案例（如国际冲突事件演进）说明架构设计，必要时可提供数据结构示意图。需考虑大规模数据处理和实时性要求。

使用REACT.js + D3.js 实现动态可交互时间轴可视化