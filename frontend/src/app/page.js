'use client';

import { useState } from 'react';
import { Loader2 } from 'lucide-react';

export default function Home() {
  const [pdfFiles, setPdfFiles] = useState([]);
  const [question, setQuestion] = useState('');
  const [progress, setProgress] = useState([]);
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setPdfFiles([...e.target.files]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setResult('');
    setProgress([]);
    setLoading(true);

    const formData = new FormData();
    pdfFiles.forEach((file) => formData.append('files', file));
    formData.append('question', question);

    const xhr = new XMLHttpRequest();
    xhr.open('POST', 'http://localhost:8000/analyze/', true);
    xhr.setRequestHeader('Accept', 'text/event-stream');

    xhr.onload = () => {
      setLoading(false);
    };

    xhr.onprogress = (event) => {
      const chunk = event.currentTarget.response;
      const updates = chunk
        .split('data: ')
        .filter(Boolean)
        .map((line) => line.trim())
        .filter(Boolean);

      setProgress((prev) => {
        const newProgress = [];
        for (const update of updates) {
          if (update.startsWith('✅ Final Prediction:')) {
            setResult(update.replace('✅ Final Prediction:', '').trim());
            if (!prev.includes('✅ Final Prediction done!')) {
              newProgress.push('✅ Final Prediction done!');
            }
          } else if (!prev.includes(update)) {
            newProgress.push(update);
          }
        }
        return [...prev, ...newProgress];
      });
    };

    xhr.onerror = () => {
      setLoading(false);
      setResult('❌ Error receiving progress updates.');
    };

    xhr.send(formData);
  };

  return (
    <main className="flex flex-col items-center justify-center min-h-screen p-6 bg-gray-100">
      <h1 className="text-3xl font-bold mb-6 text-center">AI Research Assistant</h1>

      <div className="flex flex-col lg:flex-row gap-6 w-full max-w-7xl">
        {/* Left Side */}
        <div className="lg:w-1/2 w-full space-y-6">
          <form
            onSubmit={handleSubmit}
            className="bg-white p-6 rounded-xl shadow-md space-y-4"
          >
            <div>
              <label className="block mb-2 font-semibold">Upload PDFs</label>
              <input
                type="file"
                accept="application/pdf"
                multiple
                onChange={handleFileChange}
                className="w-full border border-gray-300 rounded px-3 py-2"
              />
            </div>

            <div>
              <label className="block mb-2 font-semibold">Research Question</label>
              <textarea
                rows="4"
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                className="w-full border border-gray-300 rounded px-3 py-2"
                placeholder="What result can I expect if I use EfficientNet-B0..."
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 transition flex justify-center items-center gap-2"
            >
              {loading && <Loader2 className="animate-spin h-5 w-5" />} Analyze
            </button>
          </form>

          {progress.length > 0 && (
            <div className="bg-white p-4 rounded-xl shadow-sm border">
              <h2 className="text-xl font-semibold mb-2">🔄 Agent Progress</h2>
              <ul className="space-y-2 list-disc pl-5 text-sm text-gray-700">
                {progress.map((line, index) => (
                  <li key={index}>{line}</li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Right Side */}
        <div className="lg:w-1/2 w-full">
          {result && (
            <div className="bg-white p-4 rounded-xl shadow-md border border-blue-200 h-full max-h-[600px] overflow-y-auto">
              <h2 className="text-xl font-semibold mb-2">🧠 Final Prediction</h2>
              <pre className="whitespace-pre-wrap text-gray-800 text-sm">{result}</pre>
            </div>
          )}
        </div>
      </div>
    </main>
  );
}
