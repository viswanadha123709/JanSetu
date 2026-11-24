// Document Upload & Analysis Report Component (Module 4 & Module 5)
window.DocumentUpload = function DocumentUpload({ lang }) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;
  const [currentDoc, setCurrentDoc] = React.useState(null);
  const [clauses, setClauses] = React.useState([]);
  const [isUploading, setIsUploading] = React.useState(false);
  const [activeTab, setActiveTab] = React.useState('all'); // 'all', 'high', 'small', 'late', 'qa'
  const [recentDocs, setRecentDocs] = React.useState([]);
  const [qaInput, setQaInput] = React.useState('');
  const [qaLoading, setQaLoading] = React.useState(false);
  const [qaHistory, setQaHistory] = React.useState([]);
  const [explLang, setExplLang] = React.useState(lang); // 'en' or 'te'

  React.useEffect(() => {
    loadRecentDocs();
  }, []);

  React.useEffect(() => {
    setExplLang(lang);
  }, [lang]);

  const loadRecentDocs = async () => {
    try {
      const docs = await window.JanSetuAPI.getRecentDocuments();
      setRecentDocs(docs);
    } catch (e) {
      console.error(e);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      alert("Please upload a valid PDF document.");
      return;
    }

    setIsUploading(true);
    try {
      const res = await window.JanSetuAPI.uploadDocument(file);
      await loadDocumentDetails(res.id);
      loadRecentDocs();
    } catch (err) {
      alert("Failed to analyze PDF document. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleSampleLoad = async (sampleType) => {
    setIsUploading(true);
    try {
      const res = await window.JanSetuAPI.loadSampleDocument(sampleType);
      await loadDocumentDetails(res.id);
      loadRecentDocs();
    } catch (err) {
      alert("Failed to load sample document.");
    } finally {
      setIsUploading(false);
    }
  };

  const loadDocumentDetails = async (docId) => {
    const docData = await window.JanSetuAPI.getDocument(docId);
    setCurrentDoc(docData);
    const clausesData = await window.JanSetuAPI.getDocumentClauses(docId);
    setClauses(clausesData);
    setQaHistory([]);
  };

  const handleDocumentQA = async (e) => {
    e.preventDefault();
    if (!qaInput.trim() || !currentDoc) return;

    const userQ = qaInput.trim();
    setQaInput('');
    setQaLoading(true);

    try {
      const res = await window.JanSetuAPI.askDocumentQuestion(currentDoc.id, userQ, explLang);
      setQaHistory(prev => [
        ...prev,
        { question: userQ, answer: res.answer, citations: res.citations }
      ]);
    } catch (err) {
      alert("Failed to get answer for query.");
    } finally {
      setQaLoading(false);
    }
  };

  // Filter clauses based on active tab
  const filteredClauses = clauses.filter(cl => {
    if (activeTab === 'high') return cl.importance_level === 'High';
    if (activeTab === 'small') return cl.is_small_font;
    if (activeTab === 'late') return cl.document_position === 'final_pages' || cl.document_position === 'footnote';
    return true;
  });

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-10">
      {/* Header */}
      <div className="border-b border-slate-200 pb-6">
        <div className="inline-flex items-center space-x-2 bg-amber-100 text-amber-900 px-3 py-1 rounded-full text-xs font-bold mb-2">
          <span>🛡️ Flagship Feature</span>
          <span>•</span>
          <span>Module 5: Fine Print & Hidden Conditions Engine</span>
        </div>
        <h1 className="text-2xl sm:text-4xl font-black text-slate-900 tracking-tight">
          {t.upload_title}
        </h1>
        <p className="text-sm text-slate-600 mt-2 max-w-3xl">
          {t.upload_sub}
        </p>
      </div>

      {/* Upload Zone & Pre-Loaded Sample Triggers */}
      <div className="bg-white rounded-3xl p-6 sm:p-8 border border-slate-200 shadow-sm space-y-6">
        <div className="border-2 border-dashed border-blue-300 hover:border-blue-500 rounded-2xl p-8 text-center bg-blue-50/40 hover:bg-blue-50/70 transition cursor-pointer relative">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileUpload}
            disabled={isUploading}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
          />
          <div className="space-y-3">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-blue-100 text-blue-700 flex items-center justify-center text-3xl font-bold">
              📄
            </div>
            <h3 className="text-base font-bold text-slate-900">{t.upload_drag}</h3>
            <p className="text-xs text-slate-500">{t.upload_formats}</p>
          </div>
        </div>

        {/* 1-Click Instant Test Buttons */}
        <div className="pt-2 border-t border-slate-100">
          <div className="text-xs font-bold text-slate-600 uppercase tracking-wider mb-3">
            {t.upload_sample_prompt}
          </div>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => handleSampleLoad('health')}
              disabled={isUploading}
              className="bg-amber-50 hover:bg-amber-100 border border-amber-300 text-amber-900 px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center space-x-2 shadow-2xs"
            >
              <span>🏥</span>
              <span>{t.btn_sample_health}</span>
            </button>
            <button
              onClick={() => handleSampleLoad('loan')}
              disabled={isUploading}
              className="bg-blue-50 hover:bg-blue-100 border border-blue-300 text-blue-900 px-4 py-2.5 rounded-xl text-xs font-bold transition flex items-center space-x-2 shadow-2xs"
            >
              <span>💳</span>
              <span>{t.btn_sample_loan}</span>
            </button>
          </div>
        </div>

        {/* Loading Progress Bar */}
        {isUploading && (
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-2xl flex items-center space-x-3 animate-pulse">
            <div className="w-5 h-5 border-2 border-blue-600 border-t-transparent rounded-full animate-spin shrink-0"></div>
            <div className="text-xs text-blue-900 font-semibold">
              PyMuPDF is inspecting all pages, measuring font point sizes, and detecting fine print clauses...
            </div>
          </div>
        )}
      </div>

      {/* Analysis Results Display */}
      {currentDoc && currentDoc.analysis && (
        <div className="space-y-8 animate-fadeIn">
          {/* Document Header & Statistics */}
          <div className="bg-slate-900 text-white rounded-3xl p-6 sm:p-8 shadow-xl space-y-6">
            <div className="flex flex-wrap justify-between items-start gap-4">
              <div>
                <span className="text-[10px] font-bold bg-blue-600 text-white px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                  Analysis Verified
                </span>
                <h2 className="text-xl sm:text-2xl font-black text-white mt-1.5">{currentDoc.file_name}</h2>
                <p className="text-xs text-slate-400 mt-0.5">
                  Full PDF layout extracted with PyMuPDF • Exact Page References & Coordinates Preserved
                </p>
              </div>

              {/* Language Switcher for Report Explanations */}
              <div className="flex items-center space-x-2 bg-slate-800 p-1 rounded-xl text-xs">
                <span className="text-slate-400 px-2">Explanations:</span>
                <button
                  onClick={() => setExplLang('en')}
                  className={`px-3 py-1 rounded-lg font-bold transition ${explLang === 'en' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:text-white'}`}
                >
                  English
                </button>
                <button
                  onClick={() => setExplLang('te')}
                  className={`px-3 py-1 rounded-lg font-bold transition ${explLang === 'te' ? 'bg-blue-600 text-white' : 'text-slate-300 hover:text-white'}`}
                >
                  తెలుగు
                </button>
              </div>
            </div>

            {/* Statistics Cards Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 pt-4 border-t border-slate-800">
              <div className="bg-slate-800/80 p-3 rounded-2xl text-center">
                <div className="text-2xl font-black text-blue-400">{currentDoc.analysis.total_pages_analysed}</div>
                <div className="text-[10px] text-slate-400 font-bold uppercase mt-0.5">Pages Analysed</div>
              </div>
              <div className="bg-slate-800/80 p-3 rounded-2xl text-center">
                <div className="text-2xl font-black text-amber-400">{currentDoc.analysis.total_conditions_detected}</div>
                <div className="text-[10px] text-slate-400 font-bold uppercase mt-0.5">Clauses Detected</div>
              </div>
              <div className="bg-slate-800/80 p-3 rounded-2xl text-center">
                <div className="text-2xl font-black text-red-400">{currentDoc.analysis.high_risk_count}</div>
                <div className="text-[10px] text-slate-400 font-bold uppercase mt-0.5">High Priority</div>
              </div>
              <div className="bg-slate-800/80 p-3 rounded-2xl text-center">
                <div className="text-2xl font-black text-orange-400">{currentDoc.analysis.small_font_count}</div>
                <div className="text-[10px] text-slate-400 font-bold uppercase mt-0.5">Fine Print / Small</div>
              </div>
              <div className="bg-slate-800/80 p-3 rounded-2xl text-center col-span-2 sm:col-span-1">
                <div className="text-2xl font-black text-purple-400">{currentDoc.analysis.later_pages_count}</div>
                <div className="text-[10px] text-slate-400 font-bold uppercase mt-0.5">Final Pages</div>
              </div>
            </div>

            {/* Plain Language Summary Box */}
            <div className="bg-slate-800/90 border border-slate-700 p-4 sm:p-5 rounded-2xl space-y-2">
              <h3 className="text-xs font-bold text-blue-300 uppercase tracking-wider flex items-center space-x-1.5">
                <span>📋</span>
                <span>{t.report_overall_summary}</span>
              </h3>
              <p className="text-xs sm:text-sm text-slate-200 leading-relaxed">
                {explLang === 'te' && currentDoc.analysis.overall_summary_te
                  ? currentDoc.analysis.overall_summary_te
                  : currentDoc.analysis.overall_summary}
              </p>
            </div>
          </div>

          {/* Filter Tabs Bar */}
          <div className="flex flex-wrap border-b border-slate-200 gap-2">
            <button
              onClick={() => setActiveTab('all')}
              className={`px-4 py-2.5 text-xs font-bold rounded-t-xl transition ${activeTab === 'all' ? 'bg-white border-t-2 border-blue-600 text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              {t.tab_all} ({clauses.length})
            </button>
            <button
              onClick={() => setActiveTab('high')}
              className={`px-4 py-2.5 text-xs font-bold rounded-t-xl transition ${activeTab === 'high' ? 'bg-white border-t-2 border-red-600 text-red-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              ⚠️ {t.tab_high} ({currentDoc.analysis.high_risk_count})
            </button>
            <button
              onClick={() => setActiveTab('small')}
              className={`px-4 py-2.5 text-xs font-bold rounded-t-xl transition ${activeTab === 'small' ? 'bg-white border-t-2 border-amber-600 text-amber-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              🔍 {t.tab_small_font} ({currentDoc.analysis.small_font_count})
            </button>
            <button
              onClick={() => setActiveTab('late')}
              className={`px-4 py-2.5 text-xs font-bold rounded-t-xl transition ${activeTab === 'late' ? 'bg-white border-t-2 border-purple-600 text-purple-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              📑 {t.tab_late_pages} ({currentDoc.analysis.later_pages_count})
            </button>
            <button
              onClick={() => setActiveTab('qa')}
              className={`px-4 py-2.5 text-xs font-bold rounded-t-xl transition ${activeTab === 'qa' ? 'bg-white border-t-2 border-emerald-600 text-emerald-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'}`}
            >
              💬 {t.tab_ask}
            </button>
          </div>

          {/* Tab 1-4: Extracted Clauses Cards */}
          {activeTab !== 'qa' && (
            <div className="space-y-4">
              {filteredClauses.length === 0 ? (
                <div className="bg-white p-8 rounded-2xl border border-slate-200 text-center text-xs text-slate-500">
                  No clauses matching this filter.
                </div>
              ) : (
                filteredClauses.map((cl) => (
                  <div
                    key={cl.id}
                    className={`jansetu-card p-6 border-l-4 space-y-4 ${
                      cl.importance_level === 'High'
                        ? 'border-l-red-500'
                        : cl.importance_level === 'Medium'
                        ? 'border-l-amber-500'
                        : 'border-l-blue-500'
                    }`}
                  >
                    {/* Top Meta Badges */}
                    <div className="flex flex-wrap justify-between items-center gap-2">
                      <div className="flex items-center space-x-2">
                        <span className={`text-[10px] font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider ${
                          cl.importance_level === 'High' ? 'bg-red-100 text-red-800' : cl.importance_level === 'Medium' ? 'bg-amber-100 text-amber-800' : 'bg-blue-100 text-blue-800'
                        }`}>
                          {cl.importance_level} Review Priority
                        </span>
                        <span className="text-[10px] font-bold bg-slate-900 text-white px-2 py-0.5 rounded-md">
                          {t.clause_page} {cl.page_number}
                        </span>
                        <span className="text-[10px] font-semibold text-slate-600 bg-slate-100 px-2 py-0.5 rounded-md">
                          Position: {cl.document_position}
                        </span>
                        {cl.is_small_font && (
                          <span className="text-[10px] font-bold bg-amber-100 text-amber-900 border border-amber-300 px-2 py-0.5 rounded-md">
                            🔍 Small Font ({cl.font_size}pt vs {cl.body_font_size}pt body)
                          </span>
                        )}
                      </div>
                      <span className="text-[11px] text-slate-400 font-medium">
                        Confidence: {Math.round(cl.confidence_score * 100)}%
                      </span>
                    </div>

                    {/* Clause Category Title */}
                    <div>
                      <h4 className="text-base font-extrabold text-slate-900">
                        {cl.clause_category}
                      </h4>
                      {cl.section_heading && (
                        <p className="text-xs text-slate-500 font-medium">{cl.section_heading}</p>
                      )}
                    </div>

                    {/* Exact Verbatim Text in Document */}
                    <div className="fine-print-box p-3.5 rounded-xl text-xs text-slate-800 leading-relaxed">
                      <span className="font-bold text-amber-900 block text-[10px] uppercase tracking-wider mb-1">
                        Exact Verbatim Text in Document (Page {cl.page_number}):
                      </span>
                      "{cl.original_text}"
                    </div>

                    {/* Simplified Explanation & Why it matters */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                      <div className="bg-slate-50 p-3.5 rounded-xl border border-slate-200">
                        <span className="font-bold text-slate-800 block mb-1">
                          {t.clause_simple_expl}
                        </span>
                        <p className="text-slate-700 leading-relaxed">
                          {explLang === 'te' && cl.te_explanation ? cl.te_explanation : cl.ai_explanation}
                        </p>
                      </div>

                      <div className="bg-red-50/60 p-3.5 rounded-xl border border-red-200/60">
                        <span className="font-bold text-red-900 block mb-1">
                          {t.clause_why_matters}
                        </span>
                        <p className="text-red-950 leading-relaxed">
                          {cl.why_it_matters}
                        </p>
                      </div>
                    </div>

                    {/* Suggested Action */}
                    <div className="bg-blue-50/80 p-3 rounded-xl border border-blue-200 text-xs flex items-start space-x-2">
                      <span className="text-blue-700 text-sm">💡</span>
                      <div>
                        <span className="font-bold text-blue-950 block">{t.clause_suggested_action}</span>
                        <span className="text-blue-900">{cl.suggested_action}</span>
                      </div>
                    </div>
                  </div>
                ))
              )}
            </div>
          )}

          {/* Tab 5: Grounded Document Q&A Assistant */}
          {activeTab === 'qa' && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-6">
              <div>
                <h3 className="text-lg font-black text-slate-900">Grounded Document Q&A</h3>
                <p className="text-xs text-slate-500 mt-1">
                  Ask any question specifically about '{currentDoc.file_name}'. Answers are extracted directly from the PDF text with exact page numbers.
                </p>
              </div>

              {/* Sample Document Questions */}
              <div className="flex flex-wrap gap-2 text-xs">
                <span className="text-slate-500 font-bold">Suggested:</span>
                {[
                  "What happens if I cancel the agreement?",
                  "Are there waiting periods for pre-existing diseases?",
                  "What are the late payment penalties?",
                  "Are there room rent limits?"
                ].map((sq, idx) => (
                  <button
                    key={idx}
                    onClick={() => {
                      setQaInput(sq);
                    }}
                    className="bg-slate-100 hover:bg-blue-50 text-slate-700 px-3 py-1 rounded-full border border-slate-200 text-xs"
                  >
                    {sq}
                  </button>
                ))}
              </div>

              {/* Q&A Form */}
              <form onSubmit={handleDocumentQA} className="flex gap-2">
                <input
                  type="text"
                  value={qaInput}
                  onChange={(e) => setQaInput(e.target.value)}
                  placeholder="Ask a question about this document..."
                  className="flex-1 px-4 py-2.5 rounded-xl border border-slate-200 text-sm focus:outline-none focus:border-blue-600"
                />
                <button
                  type="submit"
                  disabled={qaLoading || !qaInput.trim()}
                  className="bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white font-bold px-6 py-2.5 rounded-xl text-sm transition"
                >
                  {qaLoading ? 'Searching...' : 'Ask Document'}
                </button>
              </form>

              {/* Q&A History */}
              <div className="space-y-4">
                {qaHistory.map((item, idx) => (
                  <div key={idx} className="bg-slate-50 p-4 rounded-2xl border border-slate-200 space-y-2">
                    <div className="font-bold text-xs text-blue-900">Q: {item.question}</div>
                    <div className="text-xs sm:text-sm text-slate-800 whitespace-pre-line leading-relaxed">
                      {item.answer}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Jargon Glossary Box */}
          {currentDoc.analysis.difficult_terms && currentDoc.analysis.difficult_terms.length > 0 && (
            <div className="bg-white p-6 sm:p-8 rounded-3xl border border-slate-200 shadow-sm space-y-4">
              <h3 className="text-base font-extrabold text-slate-900 flex items-center space-x-2">
                <span>📖</span>
                <span>Simplified Financial & Insurance Jargon Glossary</span>
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {currentDoc.analysis.difficult_terms.map((termItem, idx) => (
                  <div key={idx} className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-xs space-y-1">
                    <span className="font-bold text-blue-900 block">{termItem.term}</span>
                    <p className="text-slate-600">
                      {explLang === 'te' && termItem.te ? termItem.te : termItem.simple}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
