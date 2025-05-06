import React, { useState } from "react";
import axios from "axios";

const TradeForm = () => {
  const [formData, setFormData] = useState({
    user_id: 1,
    commodity: "oil",
    price: 0,
    volume: 0,
    trade_type: "buy",
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    axios.post("http://localhost:8000/trade/", formData)
      .then((res) => alert(res.data.message))
      .catch((err) => alert("Error placing trade"));
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>Commodity:
        <select name="commodity" onChange={handleChange} value={formData.commodity}>
          <option value="oil">Oil</option>
          <option value="gas">Gas</option>
        </select>
      </label>
      <label>Price:
        <input type="number" name="price" onChange={handleChange} value={formData.price} required />
      </label>
      <label>Volume:
        <input type="number" name="volume" onChange={handleChange} value={formData.volume} required />
      </label>
      <label>Trade Type:
        <select name="trade_type" onChange={handleChange} value={formData.trade_type}>
          <option value="buy">Buy</option>
          <option value="sell">Sell</option>
        </select>
      </label>
      <button type="submit">Submit Trade</button>
    </form>
  );
};

export default TradeForm;