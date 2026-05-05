import { useCallback, useEffect, useState } from 'react'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  RadarChart, Radar, PolarGrid, PolarAngleAxis, PolarRadiusAxis,
  PieChart, Pie, Cell, Legend,
} from 'recharts'
import { getDashboard } from '../api'

const C_TEAL  = '#008080'
const C_NAVY  = '#1B2A47'
const C_GREEN = '#2ECC71'
const C_RED   = '#E74C3C'
const C_WARN  = '#F39C12'

const DIFF_COLOR = {
  EASY:   '#2ECC71',
  MEDIUM: '#F39C12',
  HARD:   '#E74C3C',
  easy:   '#2ECC71',
  medium: '#F39C12',
  hard:   '#E74C3C',
}

function CustomTooltip({ active, payload, label }) {
  if (!active || !payload?.length) return null
  return (
    <div style={{
      background: 'var(--surface)', border: '1px solid var(--border)',
      borderRadius: 8, padding: '10px 14px', fontSize: 13,
      color: 'var(--text)', boxShadow: 'var(--shadow)',
    }}>
      <div style={{ fontWeight: 700, marginBottom: 4 }}>{label}</div>
      {payload.map(p => (
        <div key={p.name} style={{ color: p.color }}>
          {p.name}: <strong>{typeof p.value === 'number' ? p.value.toFixed(1) : p.value}%</strong>
        </div>
      ))}
    </div>
  )
}

function StatCard({ icon, value, title, color, sub }) {
  return (
    <div className="stat-card fade-up">
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div className="stat-icon">{icon}</div>
        {sub && <span style={{ fontSize: 11, color: 'var(--text-muted)', fontWeight: 500 }}>{sub}</span>}
      </div>
      <div className="stat-value" style={{ color: color ?? 'var(--navy)' }}>{value}</div>
      <div className="stat-title">{title}</div>
    </div>
  )
}

function Section({ title, children }) {
  return (
    <div className="chart-card fade-up" style={{ marginBottom: 20 }}>
      <div className="chart-title">{title}</div>
      {children}
    </div>
  )
}

function ProgressBar({ value, color }) {
  const auto = value >= 70 ? C_GREEN : value >= 40 ? C_WARN : C_RED
  return (
    <div style={{ height: 6, background: 'var(--surface-2)', borderRadius: 4, overflow: 'hidden' }}>
      <div style={{
        height: '100%', width: `${Math.min(value, 100)}%`,
        background: color ?? auto, borderRadius: 4,
        transition: 'width 0.6s cubic-bezier(.4,0,.2,1)',
      }} />
    </div>
  )
}

function GaugeRing({ pct }) {
  const color = pct >= 70 ? C_GREEN : pct >= 40 ? C_WARN : C_RED
  const label = pct >= 70 ? 'Mükemmel 🎉' : pct >= 40 ? 'Gelişiyor 📈' : 'Çalışma Gerekli 💪'
  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 8 }}>
      <div style={{
        width: 130, height: 130, borderRadius: '50%',
        border: `8px solid ${color}`, boxShadow: `0 0 28px ${color}33`,
        display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
      }}>
        <div style={{ fontSize: 36, fontWeight: 800, color, lineHeight: 1 }}>%{pct}</div>
        <div style={{ fontSize: 11, color: 'var(--text-muted)' }}>Başarı</div>
      </div>
      <span style={{ fontSize: 12, color, fontWeight: 600 }}>{label}</span>
    </div>
  )
}

const COL_HEADERS = ['Konu', 'Toplam', 'Doğru', 'Yanlış', 'Grafik', 'Başarı']
const COL_GRID    = '1fr 60px 60px 60px 110px 110px'

function TableHeader() {
  return (
    <div style={{ display: 'grid', gridTemplateColumns: COL_GRID, gap: 8, padding: '0 0 8px', borderBottom: '2px solid var(--border)' }}>
      {COL_HEADERS.map(h => (
        <div key={h} style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.6px', textAlign: h !== 'Konu' ? 'center' : 'left' }}>{h}</div>
      ))}
    </div>
  )
}

function TopicRow({ topic, type }) {
  const acc   = Number(topic.accuracy ?? 0)
  const color = type === 'strong' ? C_GREEN : type === 'weak' ? C_RED : C_WARN
  return (
    <div style={{ display: 'grid', gridTemplateColumns: COL_GRID, gap: 8, padding: '11px 0', borderBottom: '1px solid var(--border)', alignItems: 'center', fontSize: 13 }}>
      <div style={{ fontWeight: 500, color: 'var(--text)' }}>{topic.konu}</div>
      <div style={{ textAlign: 'center', color: 'var(--text-dim)' }}>{topic.n_questions}</div>
      <div style={{ textAlign: 'center', color: C_GREEN, fontWeight: 600 }}>{topic.n_correct}</div>
      <div style={{ textAlign: 'center', color: C_RED,   fontWeight: 600 }}>{topic.n_wrong}</div>
      <div style={{ paddingRight: 8 }}><ProgressBar value={acc} color={color} /></div>
      <div style={{ textAlign: 'right' }}>
        <span style={{ background: `${color}18`, color, border: `1px solid ${color}44`, borderRadius: 100, padding: '3px 10px', fontSize: 12, fontWeight: 700 }}>
          %{acc.toFixed(1)}
        </span>
      </div>
    </div>
  )
}

function GroupCard({ item, colorMap }) {
  const acc   = Number(item.accuracy ?? 0)
  const color = colorMap?.[item.label] ?? (acc >= 70 ? C_GREEN : acc >= 40 ? C_WARN : C_RED)
  return (
    <div style={{ background: 'var(--surface-2)', borderRadius: 10, padding: '16px 20px', border: `1px solid var(--border)` }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 10, alignItems: 'center' }}>
        <div style={{ fontWeight: 700, fontSize: 14, color: 'var(--navy)' }}>{item.label}</div>
        <span style={{ background: `${color}18`, color, border: `1px solid ${color}44`, borderRadius: 100, padding: '3px 10px', fontSize: 13, fontWeight: 700 }}>
          %{acc.toFixed(1)}
        </span>
      </div>
      <ProgressBar value={acc} color={color} />
      <div style={{ display: 'flex', gap: 16, marginTop: 8, fontSize: 12, color: 'var(--text-muted)' }}>
        <span>📚 {item.n_questions} soru</span>
        <span style={{ color: C_GREEN }}>✅ {item.n_correct}</span>
        <span style={{ color: C_RED }}>❌ {item.n_wrong}</span>
      </div>
    </div>
  )
}

const TABS = [
  { key: 'overview',    label: '📊 Genel Bakış' },
  { key: 'detail',      label: '🔍 Konu Detayı' },
  { key: 'breakdown',   label: '📚 Ders & Zorluk' },
  { key: 'suggestions', label: '🧠 Öneriler'    },
]

export default function DashboardPage({ profile }) {
  const [report,  setReport]  = useState(null)
  const [loading, setLoading] = useState(false)
  const [error,   setError]   = useState('')
  const [tab,     setTab]     = useState('overview')

  const load = useCallback(async () => {
    const activeUserId = profile?.userId?.trim()
    if (!activeUserId) {
      setReport(null)
      setError('Önce Profil sayfasından profil ID ile giriş yapın.')
      return
    }
    setError('')
    setLoading(true)
    try {
      const data = await getDashboard(activeUserId)
      setReport(data)
      setTab('overview')
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }, [profile?.userId])

  useEffect(() => {
    const activeUserId = profile?.userId?.trim()
    let cancelled = false

    Promise.resolve().then(async () => {
      if (!activeUserId) {
        if (!cancelled) {
          setReport(null)
          setError('Önce Profil sayfasından profil ID ile giriş yapın.')
        }
        return
      }

      setError('')
      setLoading(true)
      try {
        const data = await getDashboard(activeUserId)
        if (!cancelled) {
          setReport(data)
          setTab('overview')
        }
      } catch (e) {
        if (!cancelled) setError(e.message)
      } finally {
        if (!cancelled) setLoading(false)
      }
    })

    return () => { cancelled = true }
  }, [profile?.userId])

  const summary        = report?.summary                   || {}
  const weakTopics     = report?.weak_topics               || []
  const strongTopics   = report?.strong_topics             || []
  const insufficient   = report?.insufficient_data_topics  || []
  const suggestions    = report?.suggestions               || []
  const topicStats     = report?.topic_stats               || []
  const subjectStats   = report?.subject_stats             || []
  const diffStats      = report?.difficulty_stats          || []

  const pct = Number(summary.accuracy ?? 0)

  const pieData = [
    { name: 'Doğru',  value: summary.correct ?? 0, color: C_GREEN },
    { name: 'Yanlış', value: summary.wrong   ?? 0, color: C_RED   },
  ]

  const radarData = topicStats.slice(0, 8).map(t => ({
    subject: t.konu?.length > 12 ? t.konu.slice(0, 12) + '…' : t.konu,
    'Başarı': Number(t.accuracy ?? 0),
  }))

  const allTopicsBar = [...topicStats]
    .sort((a, b) => Number(b.accuracy) - Number(a.accuracy))
    .map(t => ({
      name:   t.konu?.length > 14 ? t.konu.slice(0, 14) + '…' : t.konu,
      Başarı: Number(t.accuracy ?? 0),
      fill:   Number(t.accuracy) >= 60 ? C_TEAL : C_RED,
    }))

  const subjectBarData = subjectStats.map(s => ({
    name:   s.label?.length > 16 ? s.label.slice(0, 16) + '…' : s.label,
    Başarı: Number(s.accuracy ?? 0),
  }))

  const weakBarData = weakTopics.map(t => ({
    name:        t.konu?.length > 16 ? t.konu.slice(0, 16) + '…' : t.konu,
    'Başarı (%)': Number(t.accuracy ?? 0),
  }))

  return (
    <div className="page">
      <div className="page-header">
        <h1>Performans Dashboard</h1>
        <p>Kullanıcı bazlı quiz analizi, ders & zorluk dağılımı ve akıllı çalışma önerileri.</p>
      </div>

      <div className="user-query-box dashboard-actions">
        <button id="dash-load-btn" className="btn btn-primary" onClick={load} disabled={loading}>
          {loading ? <><div className="spinner" style={{ width: 18, height: 18 }} /> Yükleniyor…</> : '📊 Analiz Et'}
        </button>
      </div>

      {error && <div className="alert alert-error" style={{ marginBottom: 20 }}>⚠️ {error}</div>}

      {!report && !loading && (
        <div className="card" style={{ textAlign: 'center', padding: '64px 32px', color: 'var(--text-muted)' }}>
          <div style={{ fontSize: 56, marginBottom: 16 }}>📊</div>
          <h2 style={{ fontSize: 18, fontWeight: 700, color: 'var(--navy)', marginBottom: 8 }}>Analiz Başlatın</h2>
          <p style={{ fontSize: 14 }}>Profil ID ile giriş yaptıktan sonra detaylı performans raporunuza ulaşın.</p>
        </div>
      )}

      {report && (
        <>
          {/* KPI Cards */}
          <div className="stats-grid" style={{ gridTemplateColumns: 'repeat(auto-fill, minmax(160px, 1fr))' }}>
            <StatCard icon="📚" value={summary.total_questions ?? 0} title="Toplam Soru" />
            <StatCard icon="✅" value={summary.correct ?? 0}         title="Doğru Cevap"  color={C_GREEN} />
            <StatCard icon="❌" value={summary.wrong ?? 0}           title="Yanlış Cevap" color={C_RED} />
            <StatCard icon="🎯" value={`%${pct}`}                    title="Başarı Oranı" color={pct >= 70 ? C_GREEN : pct >= 40 ? C_WARN : C_RED} />
            <StatCard icon="📉" value={weakTopics.length}            title="Zayıf Konu"   color={C_RED}   sub="< %60" />
            <StatCard icon="💪" value={strongTopics.length}          title="Güçlü Konu"   color={C_GREEN} sub="> %60" />
          </div>

          {/* Tab Bar */}
          <div style={{ display: 'flex', gap: 4, marginBottom: 24, borderBottom: '2px solid var(--border)', paddingBottom: 0, flexWrap: 'wrap' }}>
            {TABS.map(t => (
              <button key={t.key} onClick={() => setTab(t.key)} style={{
                padding: '9px 18px', border: 'none', background: 'none', fontSize: 13.5,
                fontWeight: 600, cursor: 'pointer', fontFamily: 'inherit',
                color:        tab === t.key ? C_TEAL : 'var(--text-dim)',
                borderBottom: `2px solid ${tab === t.key ? C_TEAL : 'transparent'}`,
                marginBottom: -2, transition: 'all 0.2s',
              }}>{t.label}</button>
            ))}
          </div>

          {/* ── TAB: GENEL BAKIŞ ── */}
          {tab === 'overview' && (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 20, marginBottom: 20 }}>
                <div className="chart-card fade-up" style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', padding: 32 }}>
                  <GaugeRing pct={pct} />
                </div>
                <div className="chart-card fade-up">
                  <div className="chart-title">Doğru / Yanlış Dağılımı</div>
                  <ResponsiveContainer width="100%" height={200}>
                    <PieChart>
                      <Pie data={pieData} cx="50%" cy="50%" innerRadius={55} outerRadius={85} paddingAngle={3} dataKey="value">
                        {pieData.map((e, i) => <Cell key={i} fill={e.color} />)}
                      </Pie>
                      <Tooltip formatter={v => [`${v} soru`, '']} />
                      <Legend wrapperStyle={{ fontSize: 13 }} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {radarData.length >= 3 && (
                <Section title="🕸️ Konu Bazlı Performans Haritası">
                  <ResponsiveContainer width="100%" height={300}>
                    <RadarChart data={radarData}>
                      <PolarGrid stroke="rgba(27,42,71,0.10)" />
                      <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--text-dim)', fontSize: 11 }} />
                      <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fill: 'var(--text-muted)', fontSize: 10 }} />
                      <Radar name="Başarı" dataKey="Başarı" stroke={C_TEAL} fill={C_TEAL} fillOpacity={0.18} strokeWidth={2} />
                      <Tooltip content={<CustomTooltip />} />
                    </RadarChart>
                  </ResponsiveContainer>
                </Section>
              )}

              {allTopicsBar.length > 0 && (
                <Section title="📊 Tüm Konular – Başarı Karşılaştırması">
                  <ResponsiveContainer width="100%" height={Math.max(260, allTopicsBar.length * 32)}>
                    <BarChart data={allTopicsBar} layout="vertical" margin={{ top: 4, right: 60, left: 0, bottom: 4 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(27,42,71,0.07)" horizontal={false} />
                      <XAxis type="number" domain={[0, 100]} tick={{ fill: 'var(--text-muted)', fontSize: 11 }} unit="%" />
                      <YAxis type="category" dataKey="name" width={120} tick={{ fill: 'var(--text-dim)', fontSize: 11 }} />
                      <Tooltip content={<CustomTooltip />} />
                      <Bar dataKey="Başarı" radius={[0, 6, 6, 0]} maxBarSize={22}>
                        {allTopicsBar.map((e, i) => <Cell key={i} fill={e.fill} />)}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                  <div style={{ display: 'flex', gap: 16, marginTop: 12, fontSize: 12 }}>
                    <span style={{ color: C_TEAL }}>● Güçlü (%60+)</span>
                    <span style={{ color: C_RED  }}>● Zayıf (-%60)</span>
                  </div>
                </Section>
              )}
            </>
          )}

          {/* ── TAB: KONU DETAYI ── */}
          {tab === 'detail' && (
            <>
              {weakTopics.length > 0 && (
                <Section title={`⚠️ Zayıf Konular (${weakTopics.length})`}>
                  <TableHeader />
                  {weakTopics.map((t, i) => <TopicRow key={i} topic={t} type="weak" />)}
                </Section>
              )}

              {strongTopics.length > 0 && (
                <Section title={`💪 Güçlü Konular (${strongTopics.length})`}>
                  <TableHeader />
                  {strongTopics.map((t, i) => <TopicRow key={i} topic={t} type="strong" />)}
                </Section>
              )}

              {insufficient.length > 0 && (
                <Section title={`📌 Yetersiz Veri (${insufficient.length} konu)`}>
                  <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {insufficient.map((t, i) => (
                      <div key={i} className="alert alert-warn">
                        <span>📌</span>
                        <div>
                          <strong>{t.konu}</strong>
                          <div style={{ marginTop: 2, opacity: 0.85 }}>
                            {t.message} ({t.n_questions} / {t.min_n} soru)
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </Section>
              )}

              {weakTopics.length === 0 && strongTopics.length === 0 && insufficient.length === 0 && (
                <div className="card" style={{ textAlign: 'center', padding: 40, color: 'var(--text-muted)' }}>
                  <div style={{ fontSize: 40 }}>📭</div>
                  <p style={{ marginTop: 12 }}>Konu verisi bulunamadı.</p>
                </div>
              )}
            </>
          )}

          {/* ── TAB: DERS & ZORLUK ── */}
          {tab === 'breakdown' && (
            <>
              {/* Ders Bazlı */}
              {subjectStats.length > 0 ? (
                <Section title="📚 Ders Bazlı Performans">
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(240px, 1fr))', gap: 12, marginBottom: 20 }}>
                    {subjectStats.map((s, i) => <GroupCard key={i} item={s} />)}
                  </div>
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={subjectBarData} margin={{ top: 4, right: 16, left: 0, bottom: 48 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(27,42,71,0.08)" />
                      <XAxis dataKey="name" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} angle={-30} textAnchor="end" interval={0} />
                      <YAxis domain={[0, 100]} tick={{ fill: 'var(--text-muted)', fontSize: 11 }} unit="%" />
                      <Tooltip content={<CustomTooltip />} />
                      <Bar dataKey="Başarı" fill={C_NAVY} radius={[6, 6, 0, 0]} maxBarSize={44} />
                    </BarChart>
                  </ResponsiveContainer>
                </Section>
              ) : (
                <div className="card" style={{ textAlign: 'center', padding: 32, color: 'var(--text-muted)', marginBottom: 20 }}>
                  <p>Ders bazlı veri henüz mevcut değil.</p>
                </div>
              )}

              {/* Zorluk Bazlı */}
              {diffStats.length > 0 ? (
                <Section title="🎯 Zorluk Seviyesi Bazlı Performans">
                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(200px, 1fr))', gap: 12 }}>
                    {diffStats.map((d, i) => <GroupCard key={i} item={d} colorMap={DIFF_COLOR} />)}
                  </div>
                </Section>
              ) : (
                <div className="card" style={{ textAlign: 'center', padding: 32, color: 'var(--text-muted)' }}>
                  <p>Zorluk seviyesi verisi henüz mevcut değil.</p>
                </div>
              )}
            </>
          )}

          {/* ── TAB: ÖNERİLER ── */}
          {tab === 'suggestions' && (
            <>
              <Section title="🧠 Kişiselleştirilmiş Çalışma Önerileri">
                <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                  {suggestions.map((s, i) => (
                    <div key={i} style={{
                      display: 'flex', gap: 14, padding: '14px 18px',
                      background: 'var(--surface-2)', borderRadius: 10,
                      borderLeft: `4px solid ${C_TEAL}`,
                    }}>
                      <span style={{ fontSize: 20, flexShrink: 0 }}>💡</span>
                      <div>
                        <div style={{ fontWeight: 600, fontSize: 14, color: 'var(--navy)', marginBottom: 2 }}>Öneri #{i + 1}</div>
                        <div style={{ fontSize: 13.5, color: 'var(--text-dim)', lineHeight: 1.55 }}>{s}</div>
                      </div>
                    </div>
                  ))}
                </div>
              </Section>

              {weakBarData.length > 0 && (
                <Section title="📉 Öncelikli Çalışılacak Konular">
                  <ResponsiveContainer width="100%" height={260}>
                    <BarChart data={weakBarData} margin={{ top: 8, right: 16, left: 0, bottom: 48 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(27,42,71,0.08)" />
                      <XAxis dataKey="name" tick={{ fill: 'var(--text-muted)', fontSize: 11 }} angle={-35} textAnchor="end" interval={0} />
                      <YAxis domain={[0, 100]} tick={{ fill: 'var(--text-muted)', fontSize: 11 }} unit="%" />
                      <Tooltip content={<CustomTooltip />} />
                      <Bar dataKey="Başarı (%)" fill={C_RED} radius={[6, 6, 0, 0]} maxBarSize={44} />
                    </BarChart>
                  </ResponsiveContainer>
                </Section>
              )}
            </>
          )}
        </>
      )}
    </div>
  )
}
