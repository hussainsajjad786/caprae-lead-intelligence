import { useEffect, useRef } from 'react';
import { X, ShieldCheck, AlertCircle } from 'lucide-react';
import { money } from './LeadTable';

export default function LeadDetail({ lead, onClose }) {
  const dialog = useRef(null);
  useEffect(() => { dialog.current.showModal(); }, []);
  return <dialog ref={dialog} className="detail" onCancel={onClose} onClick={e => { if (e.target === e.currentTarget) onClose(); }}>
    <div className="detail-head"><span className="eyebrow">LEAD PROFILE · #{lead.id.toString().padStart(3, '0')}</span><button className="icon-button" onClick={onClose} aria-label="Close lead details" autoFocus><X size={20}/></button></div>
    <h2>{lead.company_name}</h2><p>{lead.industry || 'Industry unknown'} · {lead.location || 'Market unknown'}</p>
    <div className="detail-score"><div><span className="eyebrow">FIT SCORE</span><strong>{lead.lead_score}<small>/100</small></strong></div><span className={`pill ${lead.priority.toLowerCase()}`}>{lead.priority} priority</span></div>
    <h3>Why this lead?</h3><p className="muted">A transparent rule-based score, not a prediction.</p>
    <div className="reasons">{lead.score_reasons.map(reason => <div key={reason.label}><div><span>{reason.label}</span><strong>+{reason.points}<small> / {reason.maximum}</small></strong></div><div className="track"><i style={{ width: `${reason.points / reason.maximum * 100}%` }}/></div><small>{reason.explanation}</small></div>)}</div>
    <h3>Company & contact</h3><dl className="facts">{[['Website', lead.website], ['Normalized domain', lead.normalized_domain], ['Email', lead.email], ['Phone', lead.phone], ['Employees', lead.employees?.toLocaleString()], ['Estimated revenue', money(lead.revenue)], ['Completeness', `${lead.data_completeness}%`], ['Quality', `${lead.quality_score}% · ${lead.quality_label}`], ['Duplicate status', 'Unique accepted record']].map(([label, value]) => <div key={label}><dt>{label}</dt><dd>{value ?? 'Not provided'}</dd></div>)}</dl>
    <div className="quality-note"><ShieldCheck size={18}/><div><strong>{lead.verification_status}</strong><p>Email and website syntax only. No DNS, deliverability, ownership, or external verification has been performed.</p></div></div>
    {lead.quality_flags.length > 0 && <div className="flags">{lead.quality_flags.map(flag => <p key={flag}><AlertCircle size={14}/>{flag}</p>)}</div>}
    <p className="demo-foot">Demo / Synthetic Data · Fictional companies and contacts. Do not use for outreach.</p>
  </dialog>;
}
