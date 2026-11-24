// Scheme Discovery Component
window.SchemeDiscovery = function SchemeDiscovery({
  lang,
  schemes,
  categories,
  selectedCategory,
  setSelectedCategory,
  selectedState,
  setSelectedState,
  selectedType,
  setSelectedType,
  searchQuery,
  setSearchQuery,
  openSchemeModal
}) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="border-b border-slate-200 pb-6">
        <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
          {t.nav_schemes}
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Explore verified Central Government and State schemes for Andhra Pradesh and Telangana. Filter by domain or region.
        </p>
      </div>

      {/* Filter and Search Controls */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs space-y-4">
        {/* Search Bar */}
        <div className="relative">
          <span className="absolute left-3.5 top-3 text-slate-400">🔍</span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search schemes by name, keyword, benefits, or organization..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3.5 top-2.5 text-xs text-slate-400 hover:text-slate-600 bg-slate-100 rounded-full w-5 h-5 flex items-center justify-center"
            >
              ✕
            </button>
          )}
        </div>

        {/* Dropdown Filters Grid */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* State Filter */}
          <div>
            <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">Applicable State / Level</label>
            <select
              value={selectedState}
              onChange={(e) => setSelectedState(e.target.value)}
              className="w-full border border-slate-200 rounded-xl px-3 py-2 text-xs bg-white focus:outline-none focus:border-blue-600"
            >
              <option value="">{t.filter_all_states}</option>
              <option value="AP">Andhra Pradesh</option>
              <option value="TS">Telangana</option>
              <option value="IN">Central Government</option>
            </select>
          </div>

          {/* Category Filter */}
          <div>
            <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">Category / Domain</label>
            <select
              value={selectedCategory}
              onChange={(e) => setSelectedCategory(e.target.value)}
              className="w-full border border-slate-200 rounded-xl px-3 py-2 text-xs bg-white focus:outline-none focus:border-blue-600"
            >
              <option value="">{t.filter_category}</option>
              {categories.map((c) => (
                <option key={c.id} value={c.category_name}>{c.category_name}</option>
              ))}
            </select>
          </div>

          {/* Scheme Type Filter */}
          <div>
            <label className="block text-[11px] font-bold text-slate-600 uppercase tracking-wider mb-1">Offering Type</label>
            <select
              value={selectedType}
              onChange={(e) => setSelectedType(e.target.value)}
              className="w-full border border-slate-200 rounded-xl px-3 py-2 text-xs bg-white focus:outline-none focus:border-blue-600"
            >
              <option value="">{t.filter_type}</option>
              <option value="Central">Central Scheme</option>
              <option value="State">State Government Scheme</option>
              <option value="Public">Public-Sector Scheme</option>
            </select>
          </div>
        </div>

        {/* Active Filters Display */}
        {(selectedState || selectedCategory || selectedType || searchQuery) && (
          <div className="pt-2 flex flex-wrap items-center gap-2 text-xs">
            <span className="text-slate-500 font-medium">Active Filters:</span>
            {selectedState && (
              <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full font-semibold flex items-center space-x-1">
                <span>State: {selectedState}</span>
                <button onClick={() => setSelectedState('')}>×</button>
              </span>
            )}
            {selectedCategory && (
              <span className="bg-indigo-100 text-indigo-800 px-2 py-0.5 rounded-full font-semibold flex items-center space-x-1">
                <span>Category: {selectedCategory}</span>
                <button onClick={() => setSelectedCategory('')}>×</button>
              </span>
            )}
            {selectedType && (
              <span className="bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-semibold flex items-center space-x-1">
                <span>Type: {selectedType}</span>
                <button onClick={() => setSelectedType('')}>×</button>
              </span>
            )}
            <button
              onClick={() => {
                setSelectedState('');
                setSelectedCategory('');
                setSelectedType('');
                setSearchQuery('');
              }}
              className="text-red-600 hover:underline font-medium text-xs ml-2"
            >
              Reset all
            </button>
          </div>
        )}
      </div>

      {/* Schemes Grid Count */}
      <div className="flex justify-between items-center text-xs text-slate-500 font-medium">
        <span>Showing {schemes.length} verified schemes</span>
        <span>All data synced with official government portals</span>
      </div>

      {/* Schemes Cards Grid */}
      {schemes.length === 0 ? (
        <div className="bg-white p-12 text-center rounded-2xl border border-slate-200 space-y-3">
          <div className="text-4xl">🔍</div>
          <h3 className="text-lg font-bold text-slate-800">No matching schemes found</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto">
            Try adjusting your search keywords or removing state/category filters.
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {schemes.map((s) => (
            <div key={s.id} className="jansetu-card p-6 flex flex-col justify-between">
              <div>
                {/* Badges */}
                <div className="flex justify-between items-start gap-2 mb-3">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${s.state_code === 'AP' ? 'bg-amber-100 text-amber-800' : s.state_code === 'TS' ? 'bg-pink-100 text-pink-800' : 'bg-blue-100 text-blue-800'}`}>
                    {s.state_name}
                  </span>
                  <span className="text-[10px] font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md">
                    {s.category_name}
                  </span>
                </div>

                {/* Scheme Title & Org */}
                <h3 className="text-base font-bold text-slate-900 leading-snug line-clamp-2 mb-1.5 hover:text-blue-700 cursor-pointer" onClick={() => openSchemeModal(s)}>
                  {s.scheme_name}
                </h3>
                <p className="text-xs text-slate-500 mb-3">{s.organization_name}</p>

                {/* Benefits Excerpt */}
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 mb-4 text-xs text-slate-700 space-y-1">
                  <span className="font-bold text-blue-800 block">Benefits:</span>
                  <p className="line-clamp-3 leading-relaxed">{s.benefits}</p>
                </div>

                {/* Key Eligibility Snippet */}
                <div className="text-xs text-slate-600 mb-4">
                  <span className="font-semibold text-slate-800">Eligibility: </span>
                  <span className="line-clamp-2">{s.eligibility_info}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <button
                  onClick={() => openSchemeModal(s)}
                  className="bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold px-3 py-2 rounded-lg transition"
                >
                  {t.card_view_details}
                </button>
                <a
                  href={s.official_source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs font-semibold text-slate-600 hover:text-blue-800 flex items-center space-x-1"
                >
                  <span>Official Portal</span>
                  <span>↗</span>
                </a>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

// Scheme Detail Modal Component
window.SchemeDetailModal = function SchemeDetailModal({ scheme, onClose, lang }) {
  if (!scheme) return null;
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;
  const [checkedDocs, setCheckedDocs] = React.useState({});

  const toggleDoc = (idx) => {
    setCheckedDocs(prev => ({ ...prev, [idx]: !prev[idx] }));
  };

  const docsList = scheme.required_documents.split(',').map(d => d.trim()).filter(Boolean);

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-slate-200">
        {/* Modal Header */}
        <div className="sticky top-0 bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center z-10">
          <div className="flex items-center space-x-2">
            <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${scheme.state_code === 'AP' ? 'bg-amber-100 text-amber-800' : scheme.state_code === 'TS' ? 'bg-pink-100 text-pink-800' : 'bg-blue-100 text-blue-800'}`}>
              {scheme.state_name}
            </span>
            <span className="text-[10px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded-md">
              {scheme.category_name}
            </span>
            <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
              Verified: {scheme.last_verified_date}
            </span>
          </div>
          <button
            onClick={onClose}
            className="text-slate-400 hover:text-slate-700 bg-slate-100 hover:bg-slate-200 w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm transition"
          >
            ✕
          </button>
        </div>

        {/* Modal Content */}
        <div className="p-6 space-y-6">
          <div>
            <h2 className="text-xl sm:text-2xl font-black text-slate-900 leading-tight mb-1">
              {scheme.scheme_name}
            </h2>
            <p className="text-xs font-semibold text-slate-500">{scheme.organization_name}</p>
          </div>

          {/* Benefits Section */}
          <div className="bg-blue-50/80 border border-blue-200/60 p-4 rounded-2xl">
            <h4 className="text-xs font-bold text-blue-900 uppercase tracking-wider mb-2">🎁 Key Financial & Social Benefits</h4>
            <p className="text-xs sm:text-sm text-slate-800 leading-relaxed whitespace-pre-line">
              {scheme.benefits}
            </p>
          </div>

          {/* Eligibility Criteria */}
          <div>
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">📋 Eligibility Requirements</h4>
            <div className="bg-slate-50 border border-slate-200 p-4 rounded-2xl text-xs sm:text-sm text-slate-800 leading-relaxed whitespace-pre-line">
              {scheme.eligibility_info}
            </div>
          </div>

          {/* Interactive Required Documents Checklist */}
          <div>
            <div className="flex justify-between items-center mb-2">
              <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider">📁 Required Documents Checklist</h4>
              <span className="text-[11px] text-slate-400">Tick items you have ready</span>
            </div>
            <div className="space-y-2">
              {docsList.map((doc, idx) => (
                <div
                  key={idx}
                  onClick={() => toggleDoc(idx)}
                  className={`p-3 rounded-xl border text-xs cursor-pointer flex items-center space-x-3 transition ${checkedDocs[idx] ? 'bg-emerald-50 border-emerald-300 text-emerald-900' : 'bg-white border-slate-200 text-slate-700 hover:bg-slate-50'}`}
                >
                  <input
                    type="checkbox"
                    checked={!!checkedDocs[idx]}
                    onChange={() => {}}
                    className="w-4 h-4 text-emerald-600 rounded cursor-pointer"
                  />
                  <span className={checkedDocs[idx] ? 'line-through text-slate-500' : 'font-medium'}>{doc}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Application Procedure */}
          <div>
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">📝 Application Procedure</h4>
            <div className="bg-slate-50 border border-slate-200 p-4 rounded-2xl text-xs sm:text-sm text-slate-800 leading-relaxed whitespace-pre-line">
              {scheme.application_procedure}
            </div>
          </div>

          {/* Important Timelines */}
          {scheme.important_dates && (
            <div className="text-xs text-slate-600 bg-amber-50 border border-amber-200 p-3 rounded-xl">
              <span className="font-bold text-amber-900">Important Dates / Cycle: </span>
              <span>{scheme.important_dates}</span>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="sticky bottom-0 bg-slate-50 border-t border-slate-200 px-6 py-4 flex flex-wrap justify-between items-center gap-3">
          <span className="text-xs text-slate-500">Official URL verified by JanSetu</span>
          <div className="flex space-x-3">
            <button
              onClick={onClose}
              className="px-4 py-2 text-xs font-semibold text-slate-600 hover:text-slate-800"
            >
              Close
            </button>
            <a
              href={scheme.official_source_url}
              target="_blank"
              rel="noreferrer"
              className="bg-blue-700 hover:bg-blue-800 text-white font-bold text-xs px-5 py-2.5 rounded-xl shadow-md transition flex items-center space-x-1.5"
            >
              <span>{t.card_official_link}</span>
              <span>↗</span>
            </a>
          </div>
        </div>
      </div>
    </div>
  );
};
