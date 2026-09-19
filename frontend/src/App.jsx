import { useEffect, useState } from 'react';
import { LayoutDashboard, Users, ChartNoAxesCombined, ShieldCheck, ArrowUpRight, Download, Sparkles, CheckCircle2, Target, ArrowRight, Database, AlertCircle } from 'lucide-react';
import { api, queryString, exportCSV } from './services/api';
import LeadTable from './components/LeadTable';
import LeadDetail from './components/LeadDetail';
import FilterBar, { EMPTY_FILTERS } from './components/FilterBar';

const NAV = [{ name: 'Overview', icon: LayoutDashboard }, { name: 'Leads', icon: Users }, { name: 'Analytics', icon: ChartNoAxesCombined }, { name: 'Data Quality', icon: ShieldCheck }];
function Distribution({ title, values, total }) {
  return <section className="panel distribution"><h3>{title}</h3>{Object.entries(values).map(([label, value]) => <div className="distribution-row" key={label}><div><span>{label}</span><strong>{value}</strong></div><div className="track"><i style={{ width: `${total ? value / total * 100 : 0}%` }}/></div></div>)}</section>;
}

export default function App() {
  const [section, setSection] = useState('Overview');
  const [stats, setStats] = useState(null);
  const [industries, setIndustries] = useState([]), [locations, setLocations] = useState([]), [duplicates, setDuplicates] = useState([]);
  const [draft, setDraft] = useState(EMPTY_FILTERS), [filters, setFilters] = useState(EMPTY_FILTERS);
  const [page, setPage] = useState({ items: [], total: 0 }), [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true), [error, setError] = useState(''), [retry, setRetry] = useState(0);
  const [lead, setLead] = useState(null), [busy, setBusy] = useState(false), [notice, setNotice] = useState('');
  useEffect(() => {
    const controller = new AbortController();
    Promise.all(['/stats', '/industries', '/locations', '/quality/duplicates'].map(path => api(path, controller.signal)))
      .then(([s, i, l, d]) => { setStats(s); setIndustries(i); setLocations(l); setDuplicates(d); })
      .catch(e => { if (e.name !== 'AbortError') setError(e.message); });
    return () => controller.abort();
  }, [retry]);
  useEffect(() => {
    const controller = new AbortController();
    setLoading(true); setError('');
    api(`/leads?${queryString({ ...filters, offset, limit: 10 })}`, controller.signal)
      .then(setPage).catch(e => { if (e.name !== 'AbortError') setError(e.message); })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [filters, offset, retry]);
  function apply(next) { setFilters({ ...next }); setDraft({ ...next }); setOffset(0); setNotice(''); }
  async function view(id) { try { setLead(await api(`/leads/${id}`)); } catch (e) { setNotice(e.message); } }
  async function download() { setBusy(true); try { await exportCSV(filters); setNotice('CSV downloaded. It includes all leads matching the applied filters.'); } catch (e) { setNotice(e.message); } finally { setBusy(false); } }
  const activeCount = Object.values(filters).filter(x => x !== '').length;
  return <div className="app-shell">
    <aside className="sidebar"><a className="brand" href="#" onClick={e => { e.preventDefault(); setSection('Overview'); }}><span className="brand-symbol">c<span>↗</span></span><div>caprae<span>LEAD INTELLIGENCE</span></div></a>
      <span className="nav-caption">WORKSPACE</span><nav aria-label="Main navigation">{NAV.map(({ name, icon: Icon }) => <button key={name} className={section === name ? 'nav-item active' : 'nav-item'} aria-current={section === name ? 'page' : undefined} onClick={() => setSection(name)}><Icon size={18}/>{name}{name === 'Leads' && stats && <span>{stats.total}</span>}</button>)}</nav>
      <div className="sidebar-note"><div className="small-icon"><Sparkles size={19}/></div><strong>Better leads.<br/>Better conversations.</strong><p>Spend less time sorting data and more time finding the right fit.</p><span>2 focused workflows <ArrowUpRight size={14}/></span></div>
      <div className="workspace-user"><span className="user-avatar">CL</span><div>Interview workspace<small>Synthetic demo environment</small></div></div>
    </aside>
    <div className="workspace"><header className="topbar"><div>Workspace <span>/</span> <strong>{section}</strong></div><span className="demo-tag"><span/> Demo / Synthetic Data</span></header>
      <main><div className="page-heading"><div><span className="eyebrow">PROSPECT WITH PURPOSE</span><h1>{section === 'Overview' || section === 'Leads' ? 'Lead Intelligence' : section}</h1><p>Prioritize high-value prospects and improve lead quality.</p></div><button className="primary" onClick={download} disabled={busy || loading || !!error || !page.total}><Download size={16}/>{busy ? 'Exporting…' : 'Export CSV'}</button></div>
      {error && <div className="error" role="alert"><AlertCircle size={18}/><span>{error}</span><button onClick={() => setRetry(retry + 1)}>Retry</button></div>}
      {notice && <div className="notice" role="status">{notice}<button aria-label="Dismiss notification" onClick={() => setNotice('')}>×</button></div>}
      <div className="stats">{[{ label: 'Total leads', value: stats?.total, icon: Users, note: 'Unique company profiles' }, { label: 'High priority', value: stats?.high_priority, icon: Target, note: 'Score of 75 or higher' }, { label: 'Format valid', value: stats?.format_valid, icon: ShieldCheck, note: 'Syntax checks · not verified' }, { label: 'Average score', value: stats?.average_score, icon: ChartNoAxesCombined, note: 'Rule-based fit · out of 100' }].map(({ label, value, icon: Icon, note }) => <section className="stat-card" key={label}><div><span>{label}</span><Icon size={18}/></div><strong>{value ?? '—'}</strong><small>{note}</small></section>)}</div>
      {section === 'Overview' && <section className="insight"><div className="insight-icon"><Sparkles size={22}/></div><div><strong>Your next conversation starts with a better lead.</strong><p>{stats ? `${stats.high_priority} high-priority companies to explore. Every score comes with a clear explanation.` : 'Loading your lead intelligence…'}</p></div><button onClick={() => { apply({ ...EMPTY_FILTERS, priority: 'High' }); setSection('Leads'); }}>Explore top leads <ArrowRight size={17}/></button></section>}
      {(section === 'Overview' || section === 'Leads') && <section className="panel leads-panel"><div className="panel-title"><div><h2>Discover leads <span>{page.total}</span></h2><p>Find, qualify, verify, and prioritize the leads that matter.</p></div><span className="list-label"><span/>{activeCount ? `${activeCount} active filters` : 'All companies'}</span></div>
        <FilterBar draft={draft} setDraft={setDraft} industries={industries} locations={locations} onApply={() => apply(draft)} onClear={() => apply(EMPTY_FILTERS)}/>
        {loading ? <div className="empty" role="status"><div className="spinner"/><h3>Finding your leads…</h3></div> : error ? <div className="empty">Unable to load leads. Retry the connection above.</div> : <LeadTable leads={page.items} onView={view}/>}
        <div className="table-footer"><span>{page.total ? `${offset + 1}–${Math.min(offset + 10, page.total)} of ${page.total}` : '0'} leads · sorted by fit score</span><div><button disabled={offset === 0 || loading} onClick={() => setOffset(Math.max(0, offset - 10))}>Previous</button><button disabled={offset + 10 >= page.total || loading} onClick={() => setOffset(offset + 10)}>Next</button></div></div></section>}
      {section === 'Analytics' && stats && <><div className="analytics-grid"><Distribution title="Priority distribution" total={stats.total} values={Object.fromEntries(['High', 'Medium', 'Low'].map(x => [x, stats.priorities[x] || 0]))}/><Distribution title="Validation coverage" total={stats.total} values={{ 'Format valid': stats.format_valid, 'Needs review': stats.needs_review, 'Externally verified': 0 }}/><Distribution title="Industry distribution" total={stats.total} values={stats.industries}/><section className="panel distribution"><h3>How to read the numbers</h3><p>Analytics describe the entire synthetic dataset, regardless of lead filters.</p><p>The average quality score is <strong>{stats.average_quality}%</strong>. Quality measures usable fields; fit score measures the illustrative prospecting profile.</p><p>No outreach or conversion results have been measured. Use this dashboard to inspect the workflow, not to claim business performance.</p></section></div></>}
      {section === 'Data Quality' && stats && <><div className="quality-banner"><ShieldCheck size={28}/><div><h2>Confidence starts with honest data.</h2><p>Format valid does not mean a company, website, or email has been externally verified.</p></div></div><div className="analytics-grid"><Distribution title="Quality overview" total={100} values={{ 'Average usable fields (%)': stats.average_quality }}/><section className="panel distribution"><h3>{stats.needs_review} profiles need attention</h3><p>Inspect missing contacts, malformed URLs, and incomplete company data before deciding on outreach.</p><button className="small-primary" onClick={() => { apply({ ...EMPTY_FILTERS, verification_status: 'Needs Review' }); setSection('Leads'); }}>Review flagged leads <ArrowRight size={15}/></button></section></div><section className="panel duplicate-panel"><h2>Duplicate review <span className="pill medium">{duplicates.length} prevented</span></h2><p>Incoming records are preserved for review. Canonical profiles remain unique; nothing is silently deleted.</p>{duplicates.map(d => <div className="duplicate-row" key={d.id}><div><strong>{d.incoming_company}</strong><small>{d.reason}</small></div><button className="view-button" onClick={() => view(d.matched_lead_id)}>View retained lead <ArrowUpRight size={14}/></button></div>)}</section></>}
      <footer className="page-footer"><span><Database size={13}/> Synthetic data only · No external verification</span><span><CheckCircle2 size={13}/> Transparent scoring. Thoughtful qualification.</span></footer>
      </main></div>{lead && <LeadDetail lead={lead} onClose={() => setLead(null)}/>}
  </div>;
}
