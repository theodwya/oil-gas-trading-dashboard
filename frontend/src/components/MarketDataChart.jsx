import React, { useEffect, useState } from "react";
import { LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid } from "recharts";
import axios from "axios";

const MarketDataChart = ({ commodity }) => {
  const [data, setData] = useState([]);

  useEffect(() => {
    axios.get(`http://localhost:8000/marketdata/?commodity=${commodity}`)
      .then((res) => setData(res.data))
      .catch(console.error);
  }, [commodity]);

  return (
    <LineChart width={700} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="date" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="price" stroke="#8884d8" />
    </LineChart>
  );
};

export default MarketDataChart;