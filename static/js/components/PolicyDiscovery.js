// Policy Discovery & Detail Modal Component
window.PolicyDiscovery = function PolicyDiscovery({ lang, policies, openPolicyModal, searchQuery, setSearchQuery, selectedPolicyType, setSelectedPolicyType }) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;

  const filtered = policies.filter(p => {
    if (selectedPolicyType && p.policy_type !== selectedPolicyType) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return p.policy_name.toLowerCase().includes(q) || p.description.toLowerCase().includes(q) || p.key_exclusions.toLowerCase().includes(q);
    }
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Header */}
      <div className="border-b border-slate-200 pb-6 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-black text-slate-900 tracking-tight">
            {t.nav_policies}
          </h1>
          <p className="text-sm text-slate-500 mt-1">
            Browse insurance policies, student education loans, and financial products with transparent fine-print disclosures.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-xs flex flex-wrap gap-4 items-center justify-between">
        <div className="relative flex-1 min-w-[240px]">
          <span className="absolute left-3.5 top-3 text-slate-400">🔍</span>
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search policies, exclusions, or loans..."
            className="w-full pl-10 pr-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-blue-600"
          />
        </div>

        {/* Policy Type Filter */}
        <div className="flex items-center space-x-2">
          {['', 'insurance', 'loan', 'investment'].map((type) => (
            <button
              key={type}
              onClick={() => setSelectedPolicyType(type)}
              className={`px-3 py-1.5 rounded-xl text-xs font-semibold capitalize transition ${selectedPolicyType === type ? 'bg-blue-700 text-white shadow-xs' : 'bg-slate-100 text-slate-700 hover:bg-slate-200'}`}
            >
              {type === '' ? 'All Products' : type}
            </button>
          ))}
        </div>
      </div>

      {/* Policy Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filtered.map((pol) => (
          <div key={pol.id} className="jansetu-card p-6 flex flex-col justify-between">
            <div>
              <div className="flex justify-between items-start gap-2 mb-3">
                <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 uppercase tracking-wider">
                  {pol.policy_type}
                </span>
                <span className="text-[10px] font-bold text-amber-700 bg-amber-50 border border-amber-200 px-2 py-0.5 rounded">
                  Fine Print Disclosed
                </span>
              </div>

              <h3 className="text-base font-bold text-slate-900 leading-snug line-clamp-2 mb-1.5 hover:text-blue-700 cursor-pointer" onClick={() => openPolicyModal(pol)}>
                {pol.policy_name}
              </h3>
              <p className="text-xs text-slate-500 mb-3">{pol.organization_name}</p>

              {/* Benefits */}
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 mb-3 text-xs text-slate-700">
                <span className="font-bold text-blue-800 block mb-1">Key Coverage:</span>
                <p className="line-clamp-2">{pol.benefits}</p>
              </div>

              {/* Exclusions Warning Box */}
              <div className="fine-print-box p-3 rounded-xl mb-4 text-xs text-amber-950">
                <span className="font-bold text-amber-800 block mb-1">⚠️ Prominent Fine Print Exclusions:</span>
                <p className="line-clamp-2">{pol.key_exclusions}</p>
              </div>
            </div>

            <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
              <button
                onClick={() => openPolicyModal(pol)}
                className="bg-blue-50 hover:bg-blue-100 text-blue-700 text-xs font-bold px-3 py-2 rounded-lg transition"
              >
                Inspect All Terms →
              </button>
              <a
                href={pol.official_source_url}
                target="_blank"
                rel="noreferrer"
                className="text-xs font-medium text-slate-500 hover:text-slate-800"
              >
                Official Site ↗
              </a>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

// Policy Detail Modal
window.PolicyDetailModal = function PolicyDetailModal({ policy, onClose }) {
  if (!policy) return null;

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-2xl w-full max-h-[90vh] overflow-y-auto shadow-2xl border border-slate-200">
        <div className="sticky top-0 bg-white border-b border-slate-200 px-6 py-4 flex justify-between items-center z-10">
          <div className="flex items-center space-x-2">
            <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-blue-100 text-blue-800 uppercase">
              {policy.policy_type}
            </span>
            <span className="text-[10px] font-semibold text-slate-500 bg-slate-100 px-2 py-0.5 rounded">
              {policy.category_name}
            </span>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-700 bg-slate-100 w-8 h-8 rounded-full flex items-center justify-center font-bold">
            ✕
          </button>
        </div>

        <div className="p-6 space-y-6">
          <div>
            <h2 className="text-xl sm:text-2xl font-black text-slate-900 mb-1">{policy.policy_name}</h2>
            <p className="text-xs font-semibold text-slate-500">{policy.organization_name}</p>
          </div>

          <div className="bg-blue-50/80 border border-blue-200 p-4 rounded-2xl">
            <h4 className="text-xs font-bold text-blue-900 uppercase tracking-wider mb-2">Coverage & Benefits</h4>
            <p className="text-xs sm:text-sm text-slate-800 leading-relaxed whitespace-pre-line">{policy.benefits}</p>
          </div>

          <div className="fine-print-box p-4 rounded-2xl">
            <h4 className="text-xs font-bold text-amber-900 uppercase tracking-wider mb-2">⚠️ Key Exclusions & Waiting Periods</h4>
            <p className="text-xs sm:text-sm text-amber-950 leading-relaxed whitespace-pre-line">{policy.key_exclusions}</p>
          </div>

          <div className="bg-slate-50 border border-slate-200 p-4 rounded-2xl">
            <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">Key Terms & Lock-in Requirements</h4>
            <p className="text-xs sm:text-sm text-slate-800 leading-relaxed whitespace-pre-line">{policy.terms_conditions_summary}</p>
          </div>
        </div>

        <div className="sticky bottom-0 bg-slate-50 border-t border-slate-200 px-6 py-4 flex justify-between items-center">
          <button onClick={onClose} className="text-xs font-semibold text-slate-600">Close</button>
          <a
            href={policy.official_source_url}
            target="_blank"
            rel="noreferrer"
            className="bg-blue-700 hover:bg-blue-800 text-white font-bold text-xs px-5 py-2.5 rounded-xl shadow-md transition"
          >
            Visit Provider Portal ↗
          </a>
        </div>
      </div>
    </div>
  );
};
