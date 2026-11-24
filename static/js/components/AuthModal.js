// Auth Modal & User Profile Modal Components
window.AuthModal = function AuthModal({ isOpen, onClose, initialMode = 'login', onAuthSuccess, lang }) {
  if (!isOpen) return null;
  const [mode, setMode] = React.useState(initialMode); // 'login' or 'register'
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [email, setEmail] = React.useState('');
  const [state, setState] = React.useState('Andhra Pradesh');
  const [occupation, setOccupation] = React.useState('farmer');
  const [incomeRange, setIncomeRange] = React.useState('1l_to_2.5l');
  const [preferredLang, setPreferredLang] = React.useState(lang);
  const [errorMsg, setErrorMsg] = React.useState('');
  const [loading, setLoading] = React.useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setLoading(true);

    try {
      if (mode === 'login') {
        const res = await window.JanSetuAPI.login(username, password);
        if (res.error) {
          setErrorMsg(res.error);
        } else {
          onAuthSuccess(res);
          onClose();
        }
      } else {
        const res = await window.JanSetuAPI.register({
          username,
          password,
          email,
          state,
          occupation,
          income_range: incomeRange,
          preferred_language: preferredLang,
        });
        if (res.id) {
          onAuthSuccess(res);
          onClose();
        } else {
          setErrorMsg(JSON.stringify(res));
        }
      }
    } catch (err) {
      setErrorMsg("An error occurred. Please check credentials.");
    } finally {
      setLoading(false);
    }
  };

  const handleQuickDemo = async (role) => {
    setLoading(true);
    setErrorMsg('');
    try {
      if (role === 'admin') {
        const res = await window.JanSetuAPI.login('admin', 'admin123');
        if (!res.error) {
          onAuthSuccess(res);
          onClose();
        }
      } else {
        // Create demo citizen or login if exists
        const demoUser = 'citizen_demo';
        const demoPass = 'Citizen@123';
        const resLogin = await window.JanSetuAPI.login(demoUser, demoPass);
        if (!resLogin.error) {
          onAuthSuccess(resLogin);
          onClose();
        } else {
          const resReg = await window.JanSetuAPI.register({
            username: demoUser,
            password: demoPass,
            state: 'Andhra Pradesh',
            occupation: 'farmer',
            income_range: '1l_to_2.5l',
            preferred_language: 'en'
          });
          onAuthSuccess(resReg);
          onClose();
        }
      }
    } catch (err) {
      setErrorMsg("Failed to log in as demo user.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-slate-200">
        <div className="flex justify-between items-center mb-6">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-blue-700 text-white flex items-center justify-center font-bold text-sm">
              JS
            </div>
            <h3 className="text-xl font-black text-slate-900">
              {mode === 'login' ? 'Sign In to JanSetu' : 'Create Citizen Account'}
            </h3>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        {errorMsg && (
          <div className="bg-red-50 border border-red-200 text-red-700 text-xs p-3 rounded-xl mb-4">
            {errorMsg}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4 text-xs">
          <div>
            <label className="block font-bold text-slate-700 mb-1">Username</label>
            <input
              type="text"
              required
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-blue-600"
            />
          </div>

          {mode === 'register' && (
            <div>
              <label className="block font-bold text-slate-700 mb-1">Email Address</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="citizen@example.com"
                className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-blue-600"
              />
            </div>
          )}

          <div>
            <label className="block font-bold text-slate-700 mb-1">Password</label>
            <input
              type="password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-blue-600"
            />
          </div>

          {mode === 'register' && (
            <div className="grid grid-cols-2 gap-3 pt-2">
              <div>
                <label className="block font-bold text-slate-700 mb-1">State</label>
                <select
                  value={state}
                  onChange={(e) => setState(e.target.value)}
                  className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white"
                >
                  <option value="Andhra Pradesh">Andhra Pradesh</option>
                  <option value="Telangana">Telangana</option>
                  <option value="Other">Other State</option>
                </select>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Occupation</label>
                <select
                  value={occupation}
                  onChange={(e) => setOccupation(e.target.value)}
                  className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white"
                >
                  <option value="farmer">Farmer</option>
                  <option value="student">Student</option>
                  <option value="senior_citizen">Senior Citizen</option>
                  <option value="entrepreneur">Entrepreneur</option>
                  <option value="small_business_owner">Small Business</option>
                  <option value="working_professional">Professional</option>
                  <option value="general_public">General Public</option>
                </select>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Annual Income</label>
                <select
                  value={incomeRange}
                  onChange={(e) => setIncomeRange(e.target.value)}
                  className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white"
                >
                  <option value="below_1l">Below ₹1,00,000</option>
                  <option value="1l_to_2.5l">₹1L - ₹2.5 Lakhs</option>
                  <option value="2.5l_to_5l">₹2.5L - ₹5 Lakhs</option>
                  <option value="5l_to_10l">₹5L - ₹10 Lakhs</option>
                  <option value="above_10l">Above ₹10 Lakhs</option>
                </select>
              </div>

              <div>
                <label className="block font-bold text-slate-700 mb-1">Language</label>
                <select
                  value={preferredLang}
                  onChange={(e) => setPreferredLang(e.target.value)}
                  className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white"
                >
                  <option value="en">English</option>
                  <option value="te">Telugu (తెలుగు)</option>
                </select>
              </div>
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-700 hover:bg-blue-800 text-white font-bold py-3 rounded-xl transition shadow-md mt-4 text-sm"
          >
            {loading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Create Account'}
          </button>
        </form>

        {/* Quick Demo Login Buttons */}
        <div className="mt-6 pt-4 border-t border-slate-100 text-center space-y-2">
          <span className="text-[11px] text-slate-400 font-medium block">Or try with one-click demo credentials:</span>
          <div className="flex gap-2">
            <button
              onClick={() => handleQuickDemo('citizen')}
              className="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold py-2 rounded-xl text-xs transition"
            >
              Demo Citizen
            </button>
            <button
              onClick={() => handleQuickDemo('admin')}
              className="flex-1 bg-amber-50 hover:bg-amber-100 text-amber-900 border border-amber-200 font-bold py-2 rounded-xl text-xs transition"
            >
              Admin (admin/admin123)
            </button>
          </div>
        </div>

        <div className="mt-4 text-center text-xs text-slate-500">
          {mode === 'login' ? (
            <span>
              Don't have an account yet?{' '}
              <button onClick={() => setMode('register')} className="text-blue-700 font-bold hover:underline">
                Register here
              </button>
            </span>
          ) : (
            <span>
              Already registered?{' '}
              <button onClick={() => setMode('login')} className="text-blue-700 font-bold hover:underline">
                Sign in here
              </button>
            </span>
          )}
        </div>
      </div>
    </div>
  );
};

// User Profile Details Modal
window.UserProfileModal = function UserProfileModal({ isOpen, onClose, user, onUpdateSuccess }) {
  if (!isOpen || !user) return null;
  const profile = user.profile || {};
  const [state, setState] = React.useState(profile.state || 'Andhra Pradesh');
  const [district, setDistrict] = React.useState(profile.district || '');
  const [occupation, setOccupation] = React.useState(profile.occupation || 'farmer');
  const [incomeRange, setIncomeRange] = React.useState(profile.income_range || '1l_to_2.5l');
  const [prefLang, setPrefLang] = React.useState(profile.preferred_language || 'en');
  const [age, setAge] = React.useState(profile.age || '');
  const [saving, setSaving] = React.useState(false);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const res = await window.JanSetuAPI.updateProfile({
        state,
        district,
        occupation,
        income_range: incomeRange,
        preferred_language: prefLang,
        age: age ? parseInt(age) : null
      });
      onUpdateSuccess(res);
      onClose();
    } catch (err) {
      alert("Failed to update profile.");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
      <div className="bg-white rounded-3xl max-w-md w-full p-6 sm:p-8 shadow-2xl border border-slate-200">
        <div className="flex justify-between items-center mb-6">
          <h3 className="text-xl font-black text-slate-900">Manage Citizen Profile</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 font-bold">✕</button>
        </div>

        <form onSubmit={handleSave} className="space-y-4 text-xs">
          <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 flex items-center space-x-3 mb-2">
            <div className="w-10 h-10 rounded-full bg-blue-700 text-white flex items-center justify-center font-bold text-base">
              {user.username.charAt(0).toUpperCase()}
            </div>
            <div>
              <span className="font-bold text-slate-900 text-sm block">{user.username}</span>
              <span className="text-[11px] text-slate-500">{user.email || 'No email registered'}</span>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">State</label>
              <select value={state} onChange={(e) => setState(e.target.value)} className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white">
                <option value="Andhra Pradesh">Andhra Pradesh</option>
                <option value="Telangana">Telangana</option>
                <option value="Other">Other</option>
              </select>
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">District</label>
              <input type="text" value={district} onChange={(e) => setDistrict(e.target.value)} placeholder="e.g. Guntur, Warangal" className="w-full border border-slate-200 rounded-xl px-2.5 py-2 text-xs" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Occupation</label>
              <select value={occupation} onChange={(e) => setOccupation(e.target.value)} className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white">
                <option value="farmer">Farmer</option>
                <option value="student">Student</option>
                <option value="senior_citizen">Senior Citizen</option>
                <option value="entrepreneur">Entrepreneur</option>
                <option value="small_business_owner">Small Business</option>
                <option value="working_professional">Professional</option>
                <option value="general_public">General Public</option>
              </select>
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Age</label>
              <input type="number" value={age} onChange={(e) => setAge(e.target.value)} placeholder="Age in years" className="w-full border border-slate-200 rounded-xl px-2.5 py-2 text-xs" />
            </div>
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block font-bold text-slate-700 mb-1">Annual Income</label>
              <select value={incomeRange} onChange={(e) => setIncomeRange(e.target.value)} className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white">
                <option value="below_1l">Below ₹1,00,000</option>
                <option value="1l_to_2.5l">₹1L - ₹2.5 Lakhs</option>
                <option value="2.5l_to_5l">₹2.5L - ₹5 Lakhs</option>
                <option value="5l_to_10l">₹5L - ₹10 Lakhs</option>
                <option value="above_10l">Above ₹10 Lakhs</option>
              </select>
            </div>
            <div>
              <label className="block font-bold text-slate-700 mb-1">Language</label>
              <select value={prefLang} onChange={(e) => setPrefLang(e.target.value)} className="w-full border border-slate-200 rounded-xl px-2.5 py-2 bg-white">
                <option value="en">English</option>
                <option value="te">Telugu (తెలుగు)</option>
              </select>
            </div>
          </div>

          <div className="pt-4 flex justify-end space-x-2">
            <button type="button" onClick={onClose} className="px-4 py-2 font-semibold text-slate-600 hover:text-slate-800">
              Cancel
            </button>
            <button type="submit" disabled={saving} className="bg-blue-700 hover:bg-blue-800 text-white font-bold px-5 py-2 rounded-xl shadow-md transition">
              {saving ? 'Saving...' : 'Save Profile'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
