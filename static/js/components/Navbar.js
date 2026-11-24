// Navbar Component
window.Navbar = function Navbar({ activePage, setActivePage, lang, setLang, user, openAuthModal, openProfileModal, handleLogout, selectedState, setSelectedState }) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-50 shadow-xs">
      {/* Top Notice Bar */}
      <div className="bg-blue-900 text-white text-xs py-1.5 px-4">
        <div className="max-w-7xl mx-auto flex flex-wrap justify-between items-center gap-2">
          <div className="flex items-center space-x-2">
            <span className="bg-blue-800 text-blue-200 px-2 py-0.5 rounded text-[10px] font-semibold uppercase tracking-wider">Official Portal</span>
            <span>Government Schemes & Transparent Document Intelligence</span>
          </div>
          <div className="flex items-center space-x-4">
            {/* State Quick Selector */}
            <div className="flex items-center space-x-1">
              <span className="text-blue-300">Region:</span>
              <select
                value={selectedState}
                onChange={(e) => setSelectedState(e.target.value)}
                className="bg-blue-800 text-white text-xs rounded px-2 py-0.5 border border-blue-700 focus:outline-none cursor-pointer"
              >
                <option value="">{t.filter_all_states}</option>
                <option value="AP">Andhra Pradesh (ఆంధ్రప్రదేశ్)</option>
                <option value="TS">Telangana (తెలంగాణ)</option>
                <option value="IN">Central Schemes</option>
              </select>
            </div>
            {/* Language Toggle */}
            <div className="flex items-center bg-blue-800 rounded px-1 py-0.5 border border-blue-700">
              <button
                onClick={() => setLang('en')}
                className={`px-2 py-0.5 rounded text-xs font-medium transition ${lang === 'en' ? 'bg-blue-600 text-white' : 'text-blue-200 hover:text-white'}`}
              >
                English
              </button>
              <button
                onClick={() => setLang('te')}
                className={`px-2 py-0.5 rounded text-xs font-medium transition ${lang === 'te' ? 'bg-blue-600 text-white' : 'text-blue-200 hover:text-white'}`}
              >
                తెలుగు
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Main Navigation Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16 items-center">
          {/* Logo & Tagline */}
          <div className="flex items-center space-x-3 cursor-pointer" onClick={() => setActivePage('home')}>
            <div className="w-10 h-10 rounded-xl bg-blue-700 text-white flex items-center justify-center font-bold text-xl shadow-md">
              JS
            </div>
            <div>
              <div className="flex items-center space-x-2">
                <span className="text-2xl font-black text-blue-900 tracking-tight">{t.brand_name}</span>
                <span className="bg-amber-100 text-amber-800 text-[10px] font-bold px-2 py-0.5 rounded-full border border-amber-300">AI Powered</span>
              </div>
              <p className="text-[11px] font-medium text-slate-500 leading-none">{t.tagline}</p>
            </div>
          </div>

          {/* Desktop Navigation Links */}
          <nav className="hidden md:flex items-center space-x-1 lg:space-x-2">
            <button
              onClick={() => setActivePage('home')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${activePage === 'home' ? 'text-blue-700 bg-blue-50 font-semibold' : 'text-slate-600 hover:text-blue-700 hover:bg-slate-50'}`}
            >
              {t.nav_home}
            </button>
            <button
              onClick={() => setActivePage('schemes')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${activePage === 'schemes' ? 'text-blue-700 bg-blue-50 font-semibold' : 'text-slate-600 hover:text-blue-700 hover:bg-slate-50'}`}
            >
              {t.nav_schemes}
            </button>
            <button
              onClick={() => setActivePage('policies')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition ${activePage === 'policies' ? 'text-blue-700 bg-blue-50 font-semibold' : 'text-slate-600 hover:text-blue-700 hover:bg-slate-50'}`}
            >
              {t.nav_policies}
            </button>
            <button
              onClick={() => setActivePage('advisor')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${activePage === 'advisor' ? 'text-blue-700 bg-blue-50 font-semibold' : 'text-slate-600 hover:text-blue-700 hover:bg-slate-50'}`}
            >
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>{t.nav_advisor}</span>
            </button>
            <button
              onClick={() => setActivePage('analyzer')}
              className={`px-3 py-2 rounded-lg text-sm font-medium transition flex items-center space-x-1.5 ${activePage === 'analyzer' ? 'text-blue-700 bg-blue-50 font-semibold' : 'text-amber-800 bg-amber-50 hover:bg-amber-100'}`}
            >
              <span>🔍</span>
              <span>{t.nav_doc_analyzer}</span>
            </button>
            {user && (
              <button
                onClick={() => setActivePage('dashboard')}
                className={`px-3 py-2 rounded-lg text-sm font-medium transition ${activePage === 'dashboard' ? 'text-blue-700 bg-blue-50 font-semibold' : 'text-slate-600 hover:text-blue-700 hover:bg-slate-50'}`}
              >
                {t.nav_dashboard}
              </button>
            )}
          </nav>

          {/* Right Action Buttons */}
          <div className="flex items-center space-x-2">
            {user ? (
              <div className="flex items-center space-x-2">
                <button
                  onClick={openProfileModal}
                  className="flex items-center space-x-2 bg-slate-100 hover:bg-slate-200 px-3 py-1.5 rounded-lg text-xs font-semibold text-slate-800 transition"
                >
                  <div className="w-6 h-6 rounded-full bg-blue-600 text-white flex items-center justify-center text-[10px] font-bold">
                    {user.username.charAt(0).toUpperCase()}
                  </div>
                  <span>{user.username}</span>
                </button>
                <button
                  onClick={handleLogout}
                  className="text-xs text-slate-500 hover:text-red-600 px-2 py-1"
                >
                  {t.nav_logout}
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-2">
                <button
                  onClick={() => openAuthModal('login')}
                  className="text-xs font-semibold text-blue-700 hover:text-blue-800 px-3 py-1.5 rounded-lg border border-blue-300 hover:bg-blue-50 transition"
                >
                  {t.nav_login}
                </button>
                <button
                  onClick={() => openAuthModal('register')}
                  className="text-xs font-semibold text-white bg-blue-700 hover:bg-blue-800 px-3 py-1.5 rounded-lg shadow-sm transition"
                >
                  {t.nav_register}
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

// Footer Component
window.Footer = function Footer({ lang, setActivePage }) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;

  return (
    <footer className="bg-slate-900 text-slate-300 pt-12 pb-8 border-t border-slate-800 mt-20">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Brand Info */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-3 mb-3">
              <div className="w-8 h-8 rounded-lg bg-blue-600 text-white flex items-center justify-center font-bold text-base">
                JS
              </div>
              <span className="text-xl font-bold text-white tracking-tight">{t.brand_name}</span>
            </div>
            <p className="text-sm text-slate-400 mb-4 max-w-md">
              JanSetu bridges Indian citizens with welfare schemes, scholarships, education loans, and transparent policy analysis. Know your benefits, understand the fine print, and apply with confidence.
            </p>
            <p className="text-xs text-slate-500 font-semibold uppercase tracking-wider">
              Tagline: {t.tagline}
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-white text-xs font-bold uppercase tracking-wider mb-3">Key Modules</h4>
            <ul className="space-y-2 text-sm">
              <li><button onClick={() => setActivePage('schemes')} className="hover:text-blue-400 transition">Scheme Discovery (AP, TS, Central)</button></li>
              <li><button onClick={() => setActivePage('policies')} className="hover:text-blue-400 transition">Policies & Loan Agreements</button></li>
              <li><button onClick={() => setActivePage('advisor')} className="hover:text-blue-400 transition">AI Eligibility Assistant</button></li>
              <li><button onClick={() => setActivePage('analyzer')} className="hover:text-blue-400 transition">AI Fine Print Detector</button></li>
            </ul>
          </div>

          {/* Admin & Trust */}
          <div>
            <h4 className="text-white text-xs font-bold uppercase tracking-wider mb-3">Transparency & Admin</h4>
            <ul className="space-y-2 text-sm">
              <li><a href="/admin/" target="_blank" rel="noreferrer" className="text-amber-400 hover:text-amber-300 font-medium">Django Admin Portal →</a></li>
              <li><span className="text-xs text-slate-400">Database: Relational SQLite3 with Django ORM</span></li>
              <li><span className="text-xs text-slate-400">PDF Engine: PyMuPDF Layout Analysis</span></li>
              <li><span className="text-xs text-slate-400">Multilingual: English & Telugu (తెలుగు)</span></li>
            </ul>
          </div>
        </div>

        <div className="pt-6 border-t border-slate-800 flex flex-col md:flex-row justify-between items-center text-xs text-slate-500 gap-2">
          <p>© 2026 JanSetu. Know. Understand. Apply. All rights reserved.</p>
          <p className="italic">AI assessments are advisory. Final approval decisions belong to the competent government authority.</p>
        </div>
      </div>
    </footer>
  );
};
