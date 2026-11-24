// User Dashboard Component (Module 1)
window.Dashboard = function Dashboard({ user, lang, setActivePage, openSchemeModal, schemes }) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;
  const profile = user?.profile || {};

  // Find schemes matching user profile
  const matchedSchemes = schemes.filter(s => {
    if (profile.state && s.applicable_state && !profile.state.includes(s.applicable_state.state_name)) {
      return false;
    }
    if (profile.occupation === 'farmer' && s.category_name.toLowerCase().includes('agriculture')) return true;
    if (profile.occupation === 'student' && (s.category_name.toLowerCase().includes('scholarship') || s.category_name.toLowerCase().includes('education'))) return true;
    if (profile.occupation === 'senior_citizen' && (s.category_name.toLowerCase().includes('senior') || s.category_name.toLowerCase().includes('pension'))) return true;
    if ((profile.occupation === 'entrepreneur' || profile.occupation === 'small_business_owner') && (s.category_name.toLowerCase().includes('entrepreneurship') || s.category_name.toLowerCase().includes('business'))) return true;
    return false;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8">
      {/* Welcome Greeting Banner */}
      <div className="bg-gradient-to-r from-blue-900 to-indigo-900 text-white rounded-3xl p-6 sm:p-8 shadow-lg flex flex-col md:flex-row justify-between items-start md:items-center gap-6">
        <div className="space-y-2">
          <span className="text-[10px] font-bold bg-blue-700 text-blue-200 px-3 py-1 rounded-full uppercase tracking-wider">
            Citizen Profile Dashboard
          </span>
          <h1 className="text-2xl sm:text-3xl font-black">
            Welcome, {user?.first_name || user?.username}!
          </h1>
          <p className="text-xs sm:text-sm text-blue-200 max-w-xl">
            Active in <strong className="text-white">{profile.state || 'Andhra Pradesh'}</strong> as a <strong className="text-white">{profile.occupation?.replace('_', ' ') || 'Citizen'}</strong>. Below are personalized welfare opportunities curated for you.
          </p>
        </div>

        <div className="flex gap-2 shrink-0">
          <button
            onClick={() => setActivePage('advisor')}
            className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-4 py-2.5 rounded-xl text-xs transition shadow-md flex items-center space-x-1.5"
          >
            <span>💬</span>
            <span>Check Full Eligibility</span>
          </button>
          <button
            onClick={() => setActivePage('analyzer')}
            className="bg-amber-500 hover:bg-amber-400 text-slate-900 font-bold px-4 py-2.5 rounded-xl text-xs transition shadow-md flex items-center space-x-1.5"
          >
            <span>📄</span>
            <span>Scan Fine Print</span>
          </button>
        </div>
      </div>

      {/* Profile Overview Card */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
        <div>
          <span className="text-slate-400 font-semibold block uppercase text-[10px]">Primary State</span>
          <span className="font-bold text-slate-900 text-sm mt-0.5 block">{profile.state || 'Not specified'}</span>
        </div>
        <div>
          <span className="text-slate-400 font-semibold block uppercase text-[10px]">Occupation</span>
          <span className="font-bold text-slate-900 text-sm mt-0.5 block capitalize">{profile.occupation?.replace('_', ' ') || 'General Public'}</span>
        </div>
        <div>
          <span className="text-slate-400 font-semibold block uppercase text-[10px]">Income Category</span>
          <span className="font-bold text-slate-900 text-sm mt-0.5 block">{profile.income_range || 'Flexible'}</span>
        </div>
        <div>
          <span className="text-slate-400 font-semibold block uppercase text-[10px]">Preferred Language</span>
          <span className="font-bold text-slate-900 text-sm mt-0.5 block">{profile.preferred_language === 'te' ? 'Telugu (తెలుగు)' : 'English'}</span>
        </div>
      </div>

      {/* Recommended Schemes */}
      <div className="space-y-4">
        <div className="flex justify-between items-center">
          <h2 className="text-lg font-bold text-slate-900">
            Recommended Opportunities for Your Profile ({matchedSchemes.length})
          </h2>
          <button onClick={() => setActivePage('schemes')} className="text-xs text-blue-700 font-semibold hover:underline">
            Browse all schemes →
          </button>
        </div>

        {matchedSchemes.length === 0 ? (
          <div className="bg-white p-8 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">
            No specific scheme match for current filter. Explore the full catalogue.
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {matchedSchemes.slice(0, 6).map((s) => (
              <div key={s.id} className="jansetu-card p-6 flex flex-col justify-between">
                <div>
                  <div className="flex justify-between items-start gap-2 mb-2">
                    <span className="text-[10px] font-bold bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                      {s.state_name}
                    </span>
                    <span className="text-[10px] font-semibold bg-slate-100 text-slate-700 px-2 py-0.5 rounded">
                      {s.category_name}
                    </span>
                  </div>
                  <h3 className="text-sm font-bold text-slate-900 line-clamp-2 mb-1.5">{s.scheme_name}</h3>
                  <p className="text-xs text-slate-500 mb-3">{s.organization_name}</p>
                  <p className="text-xs text-slate-700 line-clamp-3 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                    {s.benefits}
                  </p>
                </div>
                <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                  <button
                    onClick={() => openSchemeModal(s)}
                    className="text-xs font-bold text-blue-700 hover:text-blue-800"
                  >
                    View Details →
                  </button>
                  <a
                    href={s.official_source_url}
                    target="_blank"
                    rel="noreferrer"
                    className="text-xs text-slate-500 hover:text-slate-800"
                  >
                    Portal ↗
                  </a>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
