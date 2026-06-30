import { useState, useEffect } from 'react'
import './App.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [incidents, setIncidents] = useState([])
  const [selectedIncident, setSelectedIncident] = useState(null)
  const [question, setQuestion] = useState('')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    fetch(`${API_BASE}/incidents/`)
      .then(res => res.json())
      .then(data => setIncidents(data))
      .catch(() => setError('Could not reach the incident log.'))
  }, [])

  const handleSelectIncident = (incident) => {
    setSelectedIncident(incident)
    setResponse(null)
    setQuestion(`Why was this decision made?`)
  }

  const handleSubmit = async () => {
    if (!selectedIncident || !question.trim()) return
    setLoading(true)
    setError(null)
    setResponse(null)
    try {
      const res = await fetch(`${API_BASE}/explain/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          incident: selectedIncident.incident,
          question: question
        })
      })
      const data = await res.json()
      setResponse(data)
    } catch (e) {
      setError('The ruling desk is unreachable right now.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <header className="masthead">
        <div className="masthead-inner">
          <span className="eyebrow">VAR Transparency Companion</span>
          <h1>ClearCall</h1>
          <p className="tagline">Every contested decision, explained against the Laws of the Game.</p>
        </div>
      </header>

      <main className="layout">
        <aside className="case-file">
          <h2 className="panel-label">Case File</h2>
          <ul className="incident-list">
            {incidents.length === 0 && !error && (
              <li className="incident-empty">Loading incidents…</li>
            )}
            {incidents.map((inc) => (
              <li
                key={inc.id}
                className={`incident-item ${selectedIncident?.id === inc.id ? 'is-active' : ''}`}
                onClick={() => handleSelectIncident(inc)}
              >
                <span className="incident-type">{inc.type}</span>
                <span className="incident-match">{inc.match}</span>
                <span className="incident-desc">{inc.incident}</span>
              </li>
            ))}
          </ul>
        </aside>

        <section className="ruling-desk">
          {!selectedIncident && (
            <div className="empty-state">
              <div className="whistle-mark" aria-hidden="true">§</div>
              <p>Select an incident from the case file to begin a ruling.</p>
            </div>
          )}

          {selectedIncident && (
            <div className="ruling-content">
              <div className="incident-banner">
                <span className="incident-type">{selectedIncident.type}</span>
                <h2>{selectedIncident.match}</h2>
                <p>{selectedIncident.incident}</p>
              </div>

              <div className="question-row">
                <input
                  type="text"
                  value={question}
                  onChange={(e) => setQuestion(e.target.value)}
                  placeholder="Ask about this decision…"
                  onKeyDown={(e) => e.key === 'Enter' && handleSubmit()}
                />
                <button onClick={handleSubmit} disabled={loading}>
                  {loading ? 'Reviewing…' : 'Request ruling'}
                </button>
              </div>

              {error && <p className="error-text">{error}</p>}

              {response && (
                <div className="verdict">
                  <h3 className="verdict-label">Ruling</h3>
                  <p className="verdict-text">{response.explanation}</p>

                  {response.rules_used && response.rules_used.length > 0 && (
                    <div className="citations">
                      <h4>Cited from the Laws of the Game</h4>
                      <div className="citation-stubs">
                        {response.rules_used.map((rule, i) => (
                          <div className="citation-stub" key={i}>
                            <span className="stub-index">Excerpt {i + 1}</span>
                            <p>{rule.slice(0, 220)}{rule.length > 220 ? '…' : ''}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </section>
      </main>

      <footer className="footer">
        <span>Grounded in the official FIFA Laws of the Game · Built for the IBM June Innovation Challenge</span>
      </footer>
    </div>
  )
}

export default App