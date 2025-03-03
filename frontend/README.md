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



请结合典型新闻案例（如国际冲突事件演进）说明架构设计，必要时可提供数据结构示意图。需考虑大规模数据处理和实时性要求。

使用REACT.js + D3.js 实现动态可交互时间轴可视化