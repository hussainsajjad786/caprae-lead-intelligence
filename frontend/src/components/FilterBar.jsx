import { Search, SlidersHorizontal, RotateCcw } from 'lucide-react';
export const EMPTY_FILTERS = { search: '', industry: '', location: '', min_score: '', priority: '', verification_status: '' };
export default function FilterBar({ draft, setDraft, industries, locations, onApply, onClear }) {
  const field = key => ({ value: draft[key], onChange: e => setDraft({ ...draft, [key]: e.target.value }) });
  return <form className="filters" onSubmit={e => { e.preventDefault(); onApply(); }}>
    <div className="filter-grid"><label className="search-label">Company<div className="search-input"><Search size={17}/><input placeholder="Search companies…" maxLength={160} {...field('search')}/></div></label>
    <label>Industry<select {...field('industry')}><option value="">All industries</option>{industries.map(x => <option key={x}>{x}</option>)}</select></label>
    <label>Location<select {...field('location')}><option value="">All markets</option>{locations.map(x => <option key={x}>{x}</option>)}</select></label>
    <label>Minimum score<input type="number" min="0" max="100" placeholder="0" {...field('min_score')}/></label>
    <label>Priority<select {...field('priority')}><option value="">Any priority</option>{['High', 'Medium', 'Low'].map(x => <option key={x}>{x}</option>)}</select></label>
    <label>Validation<select {...field('verification_status')}><option value="">Any status</option><option>Format Valid</option><option>Needs Review</option></select></label></div>
    <div className="filter-footer"><span><SlidersHorizontal size={14}/> Refine your ideal customer profile</span><div><button type="button" className="text-button" onClick={onClear}><RotateCcw size={14}/>Clear filters</button><button type="submit" className="small-primary">Apply filters</button></div></div>
  </form>;
}
