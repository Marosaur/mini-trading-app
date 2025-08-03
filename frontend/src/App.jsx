// src/App.jsx
import React, { useState, useEffect } from 'react';

const API_URL = 'http://127.0.0.1:8000'; 

function App() {
  const [orders, setOrders] = useState([]);
  const [form, setForm] = useState({
    instrument: '',
    way: 'buy',
    price: '',
    qty: '',
  });
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  // Fetch all orders
  const fetchOrders = async () => {
    try {
      const res = await fetch(`${API_URL}/orders`);
      console.log('Fetch response: ', res);
      if (!res.ok) throw new Error('Failed to fetch orders');
      const data = await res.json();
      setOrders(data);
    } catch (err) {
      setError(err.message);
      setOrders([]);
    }
  };

  useEffect(() => {
    fetchOrders();
  }, []);

  // Handle form input change
  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setForm({...form, [name]: value});
  };

  // Create a new order
  const createOrder = async (e) => {
    e.preventDefault();
    setError('');
    setMessage('');
    try {
      const response = await fetch(`${API_URL}/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          instrument: form.instrument,
          way: form.way,
          price: parseFloat(form.price),
          qty: parseInt(form.qty),
        }),
      });
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to create order');
      }
      setMessage('Order created successfully!');
      setForm({instrument: '', way: 'buy', price: '', qty: ''});
      fetchOrders();
    } catch (err) {
      setError(err.message);
    }
  };

  // Execute an order
  const executeOrder = async (id) => {
    setError('');
    setMessage('');
    try {
      const response = await fetch(`${API_URL}/orders/${id}/execute`);
      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to execute order');
      }
      setMessage('Order executed successfully!');
      fetchOrders();
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div style={{ padding: 20, fontFamily: 'Arial, sans-serif' }}>
      <h1>Mini Trading App</h1>

      {error && <p style={{color: 'red'}}>{error}</p>}
      {message && <p style={{color: 'green'}}>{message}</p>}

      <form onSubmit={createOrder} style={{ marginBottom: 20 }}>
        <input
          name="instrument"
          placeholder="Instrument"
          value={form.instrument}
          onChange={handleInputChange}
          required
          style={{ marginRight: 8 }}
        />
        <select name="way" value={form.way} onChange={handleInputChange} style={{ marginRight: 8 }}>
          <option value="buy">Buy</option>
          <option value="sell">Sell</option>
        </select>
        <input
          name="price"
          type="number"
          step="0.01"
          placeholder="Price"
          value={form.price}
          onChange={handleInputChange}
          required
          style={{ marginRight: 8 }}
        />
        <input
          name="qty"
          type="number"
          placeholder="Quantity"
          value={form.qty}
          onChange={handleInputChange}
          required
          style={{ marginRight: 8 }}
        />
        <button type="submit">Create Order</button>
      </form>

      <h2>All Orders</h2>
      <table border="1" cellPadding="5" cellSpacing="0" style={{ width: '100%', maxWidth: 600 }}>
        <thead>
          <tr>
            <th>#</th>
            <th>Instrument</th>
            <th>Way</th>
            <th>Price</th>
            <th>Quantity</th>
            <th>Executed</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {orders.length === 0 && (
            <tr>
              <td colSpan="7" style={{ textAlign: 'center' }}>No orders found.</td>
            </tr>
          )}
          {orders.map((order, idx) => (
            <tr key={idx}>
              <td>{idx}</td>
              <td>{order.instrument}</td>
              <td>{order.way}</td>
              <td>{order.price}</td>
              <td>{order.qty}</td>
              <td>{order.is_executed ? 'Yes' : 'No'}</td>
              <td>
                {!order.is_executed && (
                  <button onClick={() => executeOrder(idx)}>Execute</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;