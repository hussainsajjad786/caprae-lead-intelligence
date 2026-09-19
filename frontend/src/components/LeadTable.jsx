import { ArrowUpRight, CheckCircle2, AlertCircle, SearchX } from 'lucide-react';
export const money = value => value === null ? '—' : new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD', notation: 'compact', maximumFractionDigits: 1 }).format(value);
export default function LeadTable({ leads, onView }) {
  if (!leads.length) return <div className="empty"><SearchX size={36}/><h3>No leads match these filters</h3><p>Try a lower minimum score or clear your filters.</p></div>;
  return <div className="table-scroll"><table><thead><tr>{['Company', 'Industry', 'Location', 'Employees', 'Revenue', 'Score ↓', 'Priority', 'Validation', 'Quality', ''].map((name, i) => <th key={i}>{name || <span className="sr-only">Actions</span>}</th>)}</tr></thead><tbody>{leads.map(lead => <tr key={lead.id}>
    <td><div className="company"><span className={`avatar tone-${lead.id % 4}`}>{lead.company_name.split(' ').slice(0, 2).map(s => s[0]).join('')}</span><div><strong>{lead.company_name.replace(' (Demo)', '')}</strong><small>{lead.normalized_domain || 'Website needs review'}</small></div></div></td>
    <td>{lead.industry || '—'}</td><td>{lead.location || '—'}</td><td>{lead.employees?.toLocaleString() ?? '—'}</td><td>{money(lead.revenue)}</td>
    <td><span className={`score ${lead.priority.toLowerCase()}`}>{lead.lead_score}</span></td><td><span className={`pill ${lead.priority.toLowerCase()}`}><i/>{lead.priority}</span></td>
    <td><span className={`validation ${lead.verification_status === 'Format Valid' ? 'valid' : 'review'}`}>{lead.verification_status === 'Format Valid' ? <CheckCircle2 size={14}/> : <AlertCircle size={14}/>} {lead.verification_status}</span></td>
    <td><div className="quality-cell"><span>{lead.quality_score}%</span><div className="track"><i style={{ width: `${lead.quality_score}%` }}/></div></div></td><td><button className="view-button" aria-label={`View ${lead.company_name}`} onClick={() => onView(lead.id)}>View <ArrowUpRight size={14}/></button></td>
  </tr>)}</tbody></table></div>;
}
