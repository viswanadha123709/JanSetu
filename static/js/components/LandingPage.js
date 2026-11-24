// Landing Page Component
window.LandingPage = function LandingPage({ lang, setActivePage, stats, categories, onSelectCategory, onSearchSubmit, schemes, openSchemeModal }) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;
  const [searchInput, setSearchInput] = React.useState('');

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchInput.trim()) {
      onSearchSubmit(searchInput.trim());
      setActivePage('schemes');
    }
  };

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-b from-blue-900 via-blue-800 to-blue-900 text-white py-16 lg:py-24 px-4 sm:px-6 lg:px-8 rounded-b-3xl shadow-xl">
        <div className="max-w-5xl mx-auto text-center space-y-6 relative z-10">
          <div className="inline-flex items-center space-x-2 bg-blue-700/60 border border-blue-500/40 px-3 py-1 rounded-full text-xs font-semibold tracking-wide text-blue-100">
            <span>🇮🇳 Andhra Pradesh • Telangana • Central Government</span>
          </div>
          
          <h1 className="text-3xl sm:text-5xl lg:text-6xl font-black tracking-tight leading-tight">
            {t.hero_title}
          </h1>
          
          <p className="text-base sm:text-xl text-blue-100 max-w-3xl mx-auto font-normal leading-relaxed">
            {t.hero_sub}
          </p>

          {/* Quick Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto pt-4">
            <div className="relative flex items-center shadow-2xl rounded-2xl overflow-hidden bg-white p-1.5 border-2 border-blue-400">
              <span className="pl-4 text-slate-400 text-lg">🔍</span>
              <input
                type="text"
                value={searchInput}
                onChange={(e) => setSearchInput(e.target.value)}
                placeholder={t.search_placeholder}
                className="w-full px-3 py-3 text-slate-800 placeholder-slate-400 text-sm focus:outline-none"
              />
              <button
                type="submit"
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold px-6 py-3 rounded-xl text-sm transition shrink-0"
              >
                Search
              </button>
            </div>
          </form>

          {/* Action Button Pills */}
          <div className="flex flex-wrap justify-center gap-3 pt-4">
            <button
              onClick={() => setActivePage('schemes')}
              className="bg-white text-blue-900 hover:bg-blue-50 font-bold px-5 py-2.5 rounded-xl text-sm transition shadow-md"
            >
              {t.hero_btn_explore}
            </button>
            <button
              onClick={() => setActivePage('advisor')}
              className="bg-emerald-600 hover:bg-emerald-500 text-white font-bold px-5 py-2.5 rounded-xl text-sm transition shadow-md flex items-center space-x-1.5"
            >
              <span>💬</span>
              <span>{t.hero_btn_chat}</span>
            </button>
            <button
              onClick={() => setActivePage('analyzer')}
              className="bg-amber-500 hover:bg-amber-400 text-slate-900 font-bold px-5 py-2.5 rounded-xl text-sm transition shadow-md flex items-center space-x-1.5"
            >
              <span>📄</span>
              <span>{t.hero_btn_scan}</span>
            </button>
          </div>
        </div>

        {/* Decorative Grid BG */}
        <div className="absolute inset-0 opacity-10 pointer-events-none bg-[radial-gradient(#ffffff_1px,transparent_1px)] [background-size:16px_16px]"></div>
      </section>

      {/* Live Statistics Counter Bar */}
      <section className="max-w-7xl mx-auto px-4 -mt-8 relative z-20">
        <div className="bg-white rounded-2xl shadow-lg border border-slate-200 p-6 grid grid-cols-2 md:grid-cols-4 gap-6 text-center">
          <div className="border-r border-slate-100 last:border-0">
            <div className="text-3xl lg:text-4xl font-black text-blue-700">{stats ? stats.total_schemes : '17+'}</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">{t.stat_schemes}</div>
          </div>
          <div className="border-r border-slate-100 last:border-0">
            <div className="text-3xl lg:text-4xl font-black text-emerald-600">{stats ? stats.total_policies : '3+'}</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">{t.stat_policies}</div>
          </div>
          <div className="border-r border-slate-100 last:border-0">
            <div className="text-3xl lg:text-4xl font-black text-indigo-600">{stats ? stats.total_categories : '12'}</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">Categories Covered</div>
          </div>
          <div>
            <div className="text-3xl lg:text-4xl font-black text-amber-600">15+</div>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mt-1">{t.stat_conditions}</div>
          </div>
        </div>
      </section>

      {/* The Three Pillars of JanSetu */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-xs font-bold uppercase tracking-widest text-blue-700 mb-2">How JanSetu Works</h2>
          <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-900">
            Know your benefits. Understand the terms. Apply safely.
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Pillar 1 */}
          <div className="jansetu-card p-6 flex flex-col justify-between">
            <div>
              <div className="w-12 h-12 rounded-xl bg-blue-100 text-blue-700 flex items-center justify-center text-2xl font-bold mb-4">
                1
              </div>
              <h4 className="text-lg font-bold text-slate-900 mb-2">{t.pillar_1_title}</h4>
              <p className="text-sm text-slate-600 leading-relaxed">{t.pillar_1_desc}</p>
            </div>
            <button
              onClick={() => setActivePage('schemes')}
              className="mt-6 text-sm font-semibold text-blue-700 hover:text-blue-800 flex items-center space-x-1"
            >
              <span>Explore catalogue</span>
              <span>→</span>
            </button>
          </div>

          {/* Pillar 2 */}
          <div className="jansetu-card p-6 flex flex-col justify-between border-emerald-200 hover:border-emerald-300">
            <div>
              <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-700 flex items-center justify-center text-2xl font-bold mb-4">
                2
              </div>
              <h4 className="text-lg font-bold text-slate-900 mb-2">{t.pillar_2_title}</h4>
              <p className="text-sm text-slate-600 leading-relaxed">{t.pillar_2_desc}</p>
            </div>
            <button
              onClick={() => setActivePage('advisor')}
              className="mt-6 text-sm font-semibold text-emerald-700 hover:text-emerald-800 flex items-center space-x-1"
            >
              <span>Chat with AI advisor</span>
              <span>→</span>
            </button>
          </div>

          {/* Pillar 3 */}
          <div className="jansetu-card p-6 flex flex-col justify-between border-amber-200 hover:border-amber-300">
            <div>
              <div className="w-12 h-12 rounded-xl bg-amber-100 text-amber-800 flex items-center justify-center text-2xl font-bold mb-4">
                3
              </div>
              <h4 className="text-lg font-bold text-slate-900 mb-2">{t.pillar_3_title}</h4>
              <p className="text-sm text-slate-600 leading-relaxed">{t.pillar_3_desc}</p>
            </div>
            <button
              onClick={() => setActivePage('analyzer')}
              className="mt-6 text-sm font-semibold text-amber-700 hover:text-amber-800 flex items-center space-x-1"
            >
              <span>Scan PDF fine print</span>
              <span>→</span>
            </button>
          </div>
        </div>
      </section>

      {/* Category Explorer Grid */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-xs font-bold uppercase tracking-widest text-blue-700 mb-1">Catalog by Welfare Domain</h2>
            <h3 className="text-2xl font-extrabold text-slate-900">Explore Key Categories</h3>
          </div>
          <button
            onClick={() => setActivePage('schemes')}
            className="text-sm font-semibold text-blue-700 hover:underline hidden sm:block"
          >
            View all categories →
          </button>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 gap-4">
          {categories.map((cat) => (
            <div
              key={cat.id}
              onClick={() => {
                onSelectCategory(cat.category_name);
                setActivePage('schemes');
              }}
              className="jansetu-card p-4 cursor-pointer hover:border-blue-400 flex items-start space-x-3"
            >
              <div className="w-10 h-10 rounded-xl bg-blue-50 text-blue-700 flex items-center justify-center text-lg font-bold shrink-0">
                📦
              </div>
              <div>
                <h4 className="text-sm font-bold text-slate-900 hover:text-blue-700 transition">{cat.category_name}</h4>
                <p className="text-xs text-slate-500 mt-0.5 line-clamp-1">{cat.description}</p>
                <span className="inline-block mt-2 text-[10px] font-semibold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">
                  {cat.schemes_count || 0} Schemes
                </span>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Featured Schemes Highlights */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-end mb-8">
          <div>
            <h2 className="text-xs font-bold uppercase tracking-widest text-blue-700 mb-1">High-Impact Welfare Programs</h2>
            <h3 className="text-2xl font-extrabold text-slate-900">Featured Schemes in AP, Telangana & Central</h3>
          </div>
          <button
            onClick={() => setActivePage('schemes')}
            className="text-sm font-semibold text-blue-700 hover:underline"
          >
            View full catalogue ({schemes.length}) →
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {schemes.slice(0, 6).map((s) => (
            <div key={s.id} className="jansetu-card p-6 flex flex-col justify-between">
              <div>
                <div className="flex justify-between items-start gap-2 mb-3">
                  <span className={`text-[10px] font-bold px-2 py-0.5 rounded-full ${s.state_code === 'AP' ? 'bg-amber-100 text-amber-800' : s.state_code === 'TS' ? 'bg-pink-100 text-pink-800' : 'bg-blue-100 text-blue-800'}`}>
                    {s.state_name}
                  </span>
                  <span className="text-[10px] font-medium text-emerald-700 bg-emerald-50 border border-emerald-200 px-2 py-0.5 rounded-md flex items-center space-x-1">
                    <span>✓</span>
                    <span>{t.card_verified}</span>
                  </span>
                </div>
                <h4 className="text-base font-bold text-slate-900 line-clamp-2 mb-2">{s.scheme_name}</h4>
                <p className="text-xs text-slate-500 mb-3">{s.organization_name}</p>
                <p className="text-xs text-slate-700 line-clamp-3 mb-4 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                  {s.benefits}
                </p>
              </div>

              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <button
                  onClick={() => openSchemeModal(s)}
                  className="text-xs font-bold text-blue-700 hover:text-blue-800"
                >
                  {t.card_view_details} →
                </button>
                <a
                  href={s.official_source_url}
                  target="_blank"
                  rel="noreferrer"
                  className="text-xs font-medium text-slate-500 hover:text-slate-800 flex items-center space-x-1"
                >
                  <span>Portal</span>
                  <span>↗</span>
                </a>
              </div>
            </div>
          ))}
        </div>
      </section>

      {/* Fine Print Banner Callout */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="bg-gradient-to-r from-amber-500 via-amber-600 to-amber-700 rounded-3xl p-8 sm:p-12 text-slate-900 shadow-xl flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="max-w-xl space-y-3">
            <span className="bg-white/90 text-amber-900 text-xs font-black px-3 py-1 rounded-full uppercase tracking-wider">
              Flagship Fine Print Engine
            </span>
            <h3 className="text-2xl sm:text-3xl font-black text-white">
              Don't get surprised by footnotes & cancellation penalties.
            </h3>
            <p className="text-sm text-amber-100 leading-relaxed">
              Companies and insurers often tuck room rent sub-limits, 24-month waiting periods, and early foreclosure fees into small fonts and last pages. Scan your document in seconds before making decisions.
            </p>
          </div>
          <button
            onClick={() => setActivePage('analyzer')}
            className="bg-white hover:bg-slate-50 text-slate-900 font-extrabold px-8 py-4 rounded-2xl shadow-lg transition text-sm shrink-0"
          >
            Launch Fine Print Scanner →
          </button>
        </div>
      </section>
    </div>
  );
};
