import { useState } from "react";

export default function App() {
  const [symbol, setSymbol] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const fetchAnalysis = async () => {
    setLoading(true);
    const res = await fetch(`http://localhost:8000/analyze/${symbol}`);
    const data = await res.json();
    setResult(data);
    setLoading(false);
  };

  return (
    <div className="flex flex-col items-center p-10 bg-gray-900 min-h-screen text-white">
      <h1 className="text-3xl font-bold mb-6">📈 AI Stock & Options Analyzer</h1>
      
      <input
        type="text"
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
        placeholder="Enter Stock Symbol (e.g., NVDA)"
        className="p-2 mb-4 text-black w-64 border border-gray-300 rounded"
      />
      
      <button
        onClick={fetchAnalysis}
        className="px-6 py-2 bg-blue-500 rounded hover:bg-blue-700"
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>

      {result && (
        <div className="mt-8 p-4 bg-gray-800 rounded w-2/3">
          <h2 className="text-xl">📊 Analysis for {symbol.toUpperCase()}</h2>
          <p>🔹 Current Price: ${result.current_price.toFixed(2)}</p>
          <p>🔮 Predicted Price: ${result.predicted_price.toFixed(2)}</p>

          <h3 className="text-lg mt-4">💡 Option Strategies:</h3>
          {Object.entries(result.option_strategies).map(([name, [call, put]]) => (
            <p key={name}>
              ✅ {name}: Call @ {call || "N/A"} | Put @ {put || "N/A"}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}