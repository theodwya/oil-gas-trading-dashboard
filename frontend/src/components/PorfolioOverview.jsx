import React from "react";
import MarketDataChart from "./components/MarketDataChart";
import TradeForm from "./components/TradeForm";

function App() {
  return (
    <div>
      <h1>Oil & Gas Trading Dashboard</h1>
      <MarketDataChart commodity="oil" />
      <TradeForm />
    </div>
  );
}

export default App;