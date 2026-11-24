// Main JanSetu React Application
const { useState, useEffect } = React;

function App() {
  const [activePage, setActivePage] = useState('home');
  const [lang, setLang] = useState('en');
  const [user, setUser] = useState(null);
  
  // Data states
  const [schemes, setSchemes] = useState([]);
  const [policies, setPolicies] = useState([]);
  const [categories, setCategories] = useState([]);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  // Filters
  const [selectedState, setSelectedState] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [selectedType, setSelectedType] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedPolicyType, setSelectedPolicyType] = useState('');

  // Modals
  const [activeSchemeModal, setActiveSchemeModal] = useState(null);
  const [activePolicyModal, setActivePolicyModal] = useState(null);
  const [authModalMode, setAuthModalMode] = useState(null); // 'login', 'register', or null
  const [profileModalOpen, setProfileModalOpen] = useState(false);

  // Initial Data Fetch
  useEffect(() => {
    initApp();
  }, []);

  const initApp = async () => {
    try {
      // 1. Check profile session
      const profRes = await window.JanSetuAPI.getProfile();
      if (profRes.authenticated) {
        setUser(profRes.user);
        if (profRes.user.profile?.preferred_language) {
          setLang(profRes.user.profile.preferred_language);
        }
      }

      // 2. Fetch master data in parallel
      const [statsData, catsData, schemesData, policiesData] = await Promise.all([
        window.JanSetuAPI.getStats(),
        window.JanSetuAPI.getCategories(),
        window.JanSetuAPI.getSchemes(),
        window.JanSetuAPI.getPolicies(),
      ]);

      setStats(statsData);
      setCategories(catsData);
      setSchemes(schemesData);
      setPolicies(policiesData);
    } catch (err) {
      console.error("Initialization error:", err);
    } finally {
      setLoading(false);
    }
  };

  // Filter schemes whenever selectedState, selectedCategory, selectedType, or searchQuery changes
  useEffect(() => {
    fetchFilteredSchemes();
  }, [selectedState, selectedCategory, selectedType, searchQuery]);

  const fetchFilteredSchemes = async () => {
    try {
      const params = {};
      if (selectedState) params.state = selectedState;
      if (selectedCategory) params.category = selectedCategory;
      if (selectedType) params.type = selectedType;
      if (searchQuery) params.q = searchQuery;
      const data = await window.JanSetuAPI.getSchemes(params);
      setSchemes(data);
    } catch (err) {
      console.error("Error filtering schemes:", err);
    }
  };

  const handleLogout = async () => {
    await window.JanSetuAPI.logout();
    setUser(null);
    setActivePage('home');
  };

  const handleAuthSuccess = (userData) => {
    setUser(userData);
    if (userData.profile?.preferred_language) {
      setLang(userData.profile.preferred_language);
    }
    setActivePage('dashboard');
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-slate-50 flex flex-col items-center justify-center p-4">
        <div className="w-12 h-12 border-4 border-blue-700 border-t-transparent rounded-full animate-spin mb-4"></div>
        <div className="text-sm font-bold text-slate-800">Loading JanSetu...</div>
        <div className="text-xs text-slate-500 mt-1">Know. Understand. Apply.</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 text-slate-900">
      {/* Top Navbar */}
      <window.Navbar
        activePage={activePage}
        setActivePage={setActivePage}
        lang={lang}
        setLang={setLang}
        user={user}
        openAuthModal={(mode) => setAuthModalMode(mode)}
        openProfileModal={() => setProfileModalOpen(true)}
        handleLogout={handleLogout}
        selectedState={selectedState}
        setSelectedState={setSelectedState}
      />

      {/* Main Content View Switcher */}
      <main className="flex-1">
        {activePage === 'home' && (
          <window.LandingPage
            lang={lang}
            setActivePage={setActivePage}
            stats={stats}
            categories={categories}
            schemes={schemes}
            onSelectCategory={(catName) => setSelectedCategory(catName)}
            onSearchSubmit={(q) => setSearchQuery(q)}
            openSchemeModal={(s) => setActiveSchemeModal(s)}
          />
        )}

        {activePage === 'schemes' && (
          <window.SchemeDiscovery
            lang={lang}
            schemes={schemes}
            categories={categories}
            selectedCategory={selectedCategory}
            setSelectedCategory={setSelectedCategory}
            selectedState={selectedState}
            setSelectedState={setSelectedState}
            selectedType={selectedType}
            setSelectedType={setSelectedType}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            openSchemeModal={(s) => setActiveSchemeModal(s)}
          />
        )}

        {activePage === 'policies' && (
          <window.PolicyDiscovery
            lang={lang}
            policies={policies}
            searchQuery={searchQuery}
            setSearchQuery={setSearchQuery}
            selectedPolicyType={selectedPolicyType}
            setSelectedPolicyType={setSelectedPolicyType}
            openPolicyModal={(p) => setActivePolicyModal(p)}
          />
        )}

        {activePage === 'advisor' && (
          <window.AIChatbot
            lang={lang}
            user={user}
          />
        )}

        {activePage === 'analyzer' && (
          <window.DocumentUpload
            lang={lang}
          />
        )}

        {activePage === 'dashboard' && (
          <window.Dashboard
            user={user}
            lang={lang}
            setActivePage={setActivePage}
            openSchemeModal={(s) => setActiveSchemeModal(s)}
            schemes={schemes}
          />
        )}
      </main>

      {/* Footer */}
      <window.Footer
        lang={lang}
        setActivePage={setActivePage}
      />

      {/* Modals */}
      {activeSchemeModal && (
        <window.SchemeDetailModal
          scheme={activeSchemeModal}
          onClose={() => setActiveSchemeModal(null)}
          lang={lang}
        />
      )}

      {activePolicyModal && (
        <window.PolicyDetailModal
          policy={activePolicyModal}
          onClose={() => setActivePolicyModal(null)}
          lang={lang}
        />
      )}

      {authModalMode && (
        <window.AuthModal
          isOpen={!!authModalMode}
          initialMode={authModalMode}
          onClose={() => setAuthModalMode(null)}
          onAuthSuccess={handleAuthSuccess}
          lang={lang}
        />
      )}

      {profileModalOpen && (
        <window.UserProfileModal
          isOpen={profileModalOpen}
          onClose={() => setProfileModalOpen(false)}
          user={user}
          onUpdateSuccess={(updatedUser) => setUser(updatedUser)}
        />
      )}
    </div>
  );
}

// Mount the App
const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
