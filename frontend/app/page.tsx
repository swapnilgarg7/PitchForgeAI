"use client";

import { useState } from "react";

export default function Home() {
  const [formData, setFormData] = useState({
    idea: "",
    customer: "",
    region: "",
    constraints: "",
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Failed to generate pitch deck");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = "pitch_deck.pptx";
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Something went wrong");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-white flex flex-col items-center justify-center p-8">
      <div className="w-full max-w-xl space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <h1 className="text-4xl font-semibold tracking-tight">
            PitchForge<span className="text-emerald-400">AI</span>
          </h1>
          <p className="text-zinc-400 text-lg">
            Turn your idea into an investor-ready deck
          </p>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="space-y-4">
            <input
              type="text"
              placeholder="What's your startup idea?"
              value={formData.idea}
              onChange={(e) =>
                setFormData({ ...formData, idea: e.target.value })
              }
              required
              className="w-full px-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl focus:outline-none focus:border-emerald-500 transition-colors placeholder:text-zinc-500"
            />
            <input
              type="text"
              placeholder="Target customer"
              value={formData.customer}
              onChange={(e) =>
                setFormData({ ...formData, customer: e.target.value })
              }
              className="w-full px-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl focus:outline-none focus:border-emerald-500 transition-colors placeholder:text-zinc-500"
            />
            <div className="grid grid-cols-2 gap-4">
              <input
                type="text"
                placeholder="Region"
                value={formData.region}
                onChange={(e) =>
                  setFormData({ ...formData, region: e.target.value })
                }
                className="w-full px-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl focus:outline-none focus:border-emerald-500 transition-colors placeholder:text-zinc-500"
              />
              <input
                type="text"
                placeholder="Constraints"
                value={formData.constraints}
                onChange={(e) =>
                  setFormData({ ...formData, constraints: e.target.value })
                }
                className="w-full px-4 py-3 bg-zinc-900 border border-zinc-800 rounded-xl focus:outline-none focus:border-emerald-500 transition-colors placeholder:text-zinc-500"
              />
            </div>
          </div>

          {error && (
            <p className="text-red-400 text-sm text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading || !formData.idea}
            className="w-full py-3 bg-emerald-500 hover:bg-emerald-600 disabled:bg-zinc-700 disabled:cursor-not-allowed rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
          >
            {loading ? (
              <>
                <svg
                  className="animate-spin h-5 w-5"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                >
                  <circle
                    className="opacity-25"
                    cx="12"
                    cy="12"
                    r="10"
                    stroke="currentColor"
                    strokeWidth="4"
                  ></circle>
                  <path
                    className="opacity-75"
                    fill="currentColor"
                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                  ></path>
                </svg>
                Generating...
              </>
            ) : (
              "Generate Pitch Deck"
            )}
          </button>
        </form>

        {/* Footer */}
        <p className="text-center text-zinc-600 text-sm">
          Powered by Google Gemini & Slides API
        </p>
      </div>
    </div>
  );
}
