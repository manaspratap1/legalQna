import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);
  const chatEndRef = useRef(null);

  const faqs = [
    "What is the Motor Vehicle Act?",
    "fine on wrong side",
    "parking in no parking",
    "helmet rule for pillion",
  ];

  const handleAsk = async (inputQuestion) => {
    const q = inputQuestion || question;
    if (!q.trim()) return;
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/ask", {
        question: q,
      });

      const newChat = { question: q, answer: res.data.answer };
      setHistory((prev) => [...prev, newChat]);
      setQuestion("");
    } catch (err) {
      const errorMsg = "⚠️ Error fetching answer. Please try again.";
      setHistory((prev) => [...prev, { question: q, answer: errorMsg, err }]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") handleAsk();
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [history]);

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <div className="sidebar">
        <h2>📚 FAQs</h2>
        <ul>
          {faqs.map((faq, idx) => (
            <li key={idx} onClick={() => handleAsk(faq)}>
              {faq}
            </li>
          ))}
        </ul>

        <h3>🕘 Recent Questions</h3>
        <ul className="history">
          {history.slice(-2).reverse().map((item, idx) => (
            <li key={idx}>
              <strong>Q:</strong> {item.question}
              <br />
              <strong>A:</strong> {item.answer}
            </li>
          ))}
        </ul>
      </div>

      {/* Chat Main Area */}
      <div className="chat-main">
        <h1 className="title">🧠 Legal QnA</h1>

        <div className="chat-box">
          <div className="user-question">
            <label>❓ Your Question</label>
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKeyPress}
              placeholder="e.g., fine on wrong side"
            />
            <button onClick={() => handleAsk()} disabled={loading}>
              {loading ? "Thinking..." : "Ask"}
            </button>
          </div>

          <div className="chat-history">
            {history.map((item, idx) => (
              <div className="chat-bubble" key={idx}>
                <div><strong>❓ You:</strong> {item.question}</div>
                <div><strong>💬 LegalBot:</strong> {item.answer}</div>
              </div>
            ))}
            <div ref={chatEndRef} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
