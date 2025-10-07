import { useState, useEffect } from 'react'
import eCloudLearniverseLogo from '/favicon.png'
import './App.css'

//  Yes, the "VITE_" prefix is required in "VITE_BACKEND_API_BASE_URL" because Vite only exposes environment variables to your client-side code which has "VITE_" prefix
// Security reason: Vite only exposes environment variables that start with VITE_ to prevent accidentally leaking sensitive server-side environment variables (like database passwords, API keys, etc.) to the client-side JavaScript bundle.
const API_BASE_URL = import.meta.env.VITE_BACKEND_API_BASE_URL || 'http://localhost:8002/api';

function App() {
  const [messages, setMessages] = useState([]);
  const [username, setUsername] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch messages only First time when Component gets Mount... because it has "[]" Empty dependency array
  useEffect(() => {
    fetchMessages();
  }, []);

  // Fetch all messages from API
  const fetchMessages = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/messages`);
      if (!response.ok) {
          throw new Error('Failed to fetch messages');
      }
      const data = await response.json();
      setMessages(data);
      setError(null);
    } 
    catch (err) {
      setError(err.message);
      console.error('Error fetching messages:', err);
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, content }),
      });

      if (!response.ok) throw new Error('Failed to create message');

      // Clear form
      setUsername('');
      setContent('');

      // Refresh messages list
      await fetchMessages();
    }
    
    catch (err) {
      setError(err.message);
      console.error('Error creating message:', err);
    }
    
    finally {
      setLoading(false);
    }
  };

  // Handle delete message
  const handleDelete = async (messageId) => {
    if (!window.confirm('Are you sure you want to delete this message?')) return;

    try {
      const response = await fetch(`${API_BASE_URL}/messages/${messageId}`, {
        method: 'DELETE',
      });

      if (!response.ok) throw new Error('Failed to delete message');

      // Refresh messages list
      await fetchMessages();
    }
    catch (err) {
      setError(err.message);
      console.error('Error deleting message:', err);
    }
  };

  return (
    <>
      <h1>
        <img src={eCloudLearniverseLogo} alt="Logo" className="logo"/>
        E-Cloud-Learniverse
      </h1>

      {error && <div className="error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          placeholder="Your name"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <textarea
          name="content"
          placeholder="Write a message..."
          rows="3"
          cols="40"
          value={content}
          onChange={(e) => setContent(e.target.value)}
          required
        ></textarea>
        <button type="submit" disabled={loading}>
          {loading ? 'Posting...' : 'Post Message'}
        </button>
      </form>

      <h2>Existing Messages:</h2>
      {messages.length === 0 ? (
        <p>No messages yet. Be the first to post!</p>
      ) : (
        <ul>
          {messages.map((msg) => (
            <li key={msg.id}>
              <strong>{msg.username}</strong>: {msg.content}
              <button
                className="delete-btn"
                onClick={() => handleDelete(msg.id)}
                title="Delete message"
              >
                🗑️
              </button>
            </li>
          ))}
        </ul>
      )}
    </>
  )
}

export default App;
