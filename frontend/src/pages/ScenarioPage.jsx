import { useCallback, useEffect, useState } from 'react';

const API_BASE = 'http://localhost:8000/api';

export default function ScenarioPage() {
  const [scenarios, setScenarios] = useState([]);
  const [activeScenario, setActiveScenario] = useState(null);
  const [selectedOption, setSelectedOption] = useState(null);
  const [showResult, setShowResult] = useState(false);
  const [loading, setLoading] = useState(true);

  const fetchScenarios = useCallback(async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/scenarios/`);
      const data = await res.json();
      setScenarios(data);
    } catch (err) {
      console.error("Senaryolar yüklenemedi:", err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    Promise.resolve().then(fetchScenarios);
  }, [fetchScenarios]);

  const startScenario = async (id = null) => {
    setLoading(true);
    try {
      const url = id ? `${API_BASE}/scenarios/${id}` : `${API_BASE}/scenarios/random`;
      const res = await fetch(url);
      const data = await res.json();
      setActiveScenario(data);
      setSelectedOption(null);
      setShowResult(false);
    } catch (err) {
      console.error("Senaryo başlatılamadı:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleOptionSelect = (opt) => {
    if (showResult) return;
    setSelectedOption(opt);
  };

  if (loading && !activeScenario) {
    return (
      <div className="page chat-empty">
        <div className="spinner"></div>
        <p>Senaryolar yükleniyor...</p>
      </div>
    );
  }

  if (activeScenario) {
    const isCorrect = selectedOption === activeScenario.correct_option;

    return (
      <div className="page fade-up">
        <div className="scenario-active-container">
          <header className="scenario-header-nav">
            <button className="scenario-back-btn" onClick={() => setActiveScenario(null)} title="Geri Dön">
              <span style={{fontSize: '20px'}}>‹</span>
            </button>
            <div>
              <h1 style={{fontSize: '22px', margin: 0}}>{activeScenario.title}</h1>
              <div className="badge badge-teal">{activeScenario.course}</div>
            </div>
          </header>

          <div className="scenario-main-grid">
            {/* Olay Kısmı */}
            <div className="card scenario-text-card">
              <h4>Hukuki Olay</h4>
              <div className="legal-text">
                {activeScenario.scenario_text}
              </div>
              <div style={{marginTop: '16px', display: 'flex', gap: '8px'}}>
                <span className="badge badge-gold">{activeScenario.topic}</span>
                <span className="badge badge-teal">{activeScenario.difficulty}</span>
              </div>
            </div>

            {/* Soru ve Şıklar Kısmı */}
            <div className="card scenario-q-card">
              <h3>{activeScenario.question_text}</h3>
              
              <div className="scenario-options">
                {['A', 'B', 'C', 'D'].map((opt) => {
                  const optText = activeScenario[`option_${opt.toLowerCase()}`];
                  let className = "scenario-opt";
                  if (selectedOption === opt) className += " selected";
                  if (showResult) {
                    className += " disabled";
                    if (opt === activeScenario.correct_option) className += " correct";
                    else if (selectedOption === opt) className += " wrong";
                  }

                  return (
                    <div
                      key={opt}
                      className={className}
                      onClick={() => handleOptionSelect(opt)}
                    >
                      <div className="opt-circle">{opt}</div>
                      <div className="opt-text">{optText}</div>
                    </div>
                  );
                })}
              </div>

              {!showResult ? (
                <div style={{marginTop: '24px'}}>
                  <button
                    className="btn btn-primary"
                    style={{width: '100%', justifyContent: 'center'}}
                    disabled={!selectedOption}
                    onClick={() => setShowResult(true)}
                  >
                    Cevabı Kontrol Et
                  </button>
                </div>
              ) : (
                <div className={`scenario-explanation ${isCorrect ? 'correct' : 'wrong'}`}>
                  <h5>
                    {isCorrect ? '✅ Tebrikler, Doğru!' : '❌ Maalesef, Yanlış.'}
                  </h5>
                  <p><strong>Açıklama:</strong> {activeScenario.explanation}</p>
                  {activeScenario.legal_basis && (
                    <p style={{marginTop: '10px', fontSize: '13px', color: 'var(--navy)'}}>
                      <strong>Dayanak:</strong> {activeScenario.legal_basis}
                    </p>
                  )}
                  
                  <div className="scenario-footer-actions">
                    <button className="btn btn-ghost" onClick={() => startScenario()}>
                      Sıradaki Senaryo →
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="page fade-up">
      <header className="page-header" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end'}}>
        <div>
          <h1>Hukuki Senaryolar</h1>
          <p>Gerçek hayat vakaları üzerinden hukuk bilginizi test edin.</p>
        </div>
        <button className="btn btn-primary" onClick={() => startScenario()}>
          <span>🧠</span> Rastgele Başlat
        </button>
      </header>

      <div className="scenario-grid">
        {scenarios.map(s => (
          <div key={s.id} className="card scenario-item-card hover-effect" onClick={() => startScenario(s.id)}>
            <div className="card-top">
              <span className="badge badge-teal" style={{fontSize: '10px'}}>{s.course}</span>
              <span className="badge badge-gold" style={{fontSize: '10px'}}>{s.difficulty}</span>
            </div>
            <h3>{s.title}</h3>
            <div className="topic-meta">
              <span>{s.topic}</span>
              <span style={{color: 'var(--teal)', fontWeight: '700'}}>Çöz →</span>
            </div>
          </div>
        ))}
      </div>
      
      {scenarios.length === 0 && !loading && (
        <div className="chat-empty">
          <span className="empty-icon">⚖️</span>
          <h2>Henüz senaryo yok</h2>
          <p>Sistemde kayıtlı aktif senaryo bulunamadı.</p>
        </div>
      )}
    </div>
  );
}
