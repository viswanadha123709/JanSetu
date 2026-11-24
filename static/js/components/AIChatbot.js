// AI Eligibility Chatbot Component
window.AIChatbot = function AIChatbot({ lang, user }) {
  const t = window.JANSETU_TRANSLATIONS[lang] || window.JANSETU_TRANSLATIONS.en;
  const [messages, setMessages] = React.useState([
    {
      id: 'init-1',
      sender: 'bot',
      text: lang === 'te' 
        ? "నమస్కారం! నేను జనసేతు AI సంక్షేమ మరియు అర్హత సహాయకుడిని. మీ వృత్తి, రాష్ట్రం మరియు వార్షిక ఆదాయం తెలియజేస్తే మీకు వర్తించే ప్రభుత్వ పథకాలను పరిశీలించి చెబుతాను."
        : "Hello! I am JanSetu AI, your schemes and eligibility assistant. Tell me your occupation, state (e.g. Andhra Pradesh, Telangana), and annual income to see which welfare schemes match your profile.",
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
  ]);
  const [inputText, setInputText] = React.useState('');
  const [isLoading, setIsLoading] = React.useState(false);
  const [sessionId] = React.useState(() => 'sess-' + Math.random().toString(36).substring(2, 10));
  const messagesEndRef = React.useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  React.useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const quickPrompts = lang === 'te' ? [
    "నేను ఆంధ్రప్రదేశ్ రైతును, ఆదాయం ₹1,50,000",
    "తెలంగాణ ఇంజనీరింగ్ విద్యార్థులకు స్కాలర్‌షిప్‌లు",
    "మహిళా వ్యాపారవేత్తలకు ముద్రా లోన్",
    "ఆంధ్రప్రదేశ్ వృద్ధుల పెన్షన్ అర్హత"
  ] : [
    "I am a farmer from Andhra Pradesh with ₹1,50,000 income",
    "Scholarships for Telangana engineering students",
    "Mudra loan for women entrepreneurs",
    "Old age pension benefits in AP"
  ];

  const handleSend = async (queryToSend) => {
    const query = (queryToSend || inputText).trim();
    if (!query) return;

    const userMsg = {
      id: 'usr-' + Date.now(),
      sender: 'user',
      text: query,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages(prev => [...prev, userMsg]);
    setInputText('');
    setIsLoading(true);

    try {
      const res = await window.JanSetuAPI.sendChatMessage(query, sessionId, lang);
      const botMsg = {
        id: 'bot-' + Date.now(),
        sender: 'bot',
        text: res.answer,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      setMessages(prev => [...prev, {
        id: 'err-' + Date.now(),
        sender: 'bot',
        text: "Sorry, I encountered a temporary connection issue. Please verify that your local JanSetu server is running.",
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  // Text to speech helper for accessibility
  const speakText = (text) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      // Strip markdown asterisks and links for smooth voice
      const clean = text.replace(/[*#_\[\]\(\)]/g, '').replace(/https?:\/\/\S+/g, 'link');
      const utterance = new SpeechSynthesisUtterance(clean);
      utterance.lang = lang === 'te' ? 'te-IN' : 'en-IN';
      utterance.rate = 0.95;
      window.speechSynthesis.speak(utterance);
    } else {
      alert("Text-to-speech is not supported by your current browser.");
    }
  };

  return (
    <div className="max-w-4xl mx-auto px-4 py-8 space-y-6">
      {/* Header */}
      <div className="bg-white p-6 rounded-3xl border border-slate-200 shadow-xs flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="text-xl sm:text-2xl font-black text-slate-900 tracking-tight">
              {t.chat_header_title}
            </h1>
            <span className="bg-emerald-100 text-emerald-800 text-[10px] font-bold px-2 py-0.5 rounded-full border border-emerald-300">
              Online
            </span>
          </div>
          <p className="text-xs text-slate-500 mt-1">{t.chat_header_sub}</p>
        </div>
        <div className="text-[11px] bg-slate-50 border border-slate-200 text-slate-600 px-3 py-1.5 rounded-xl font-medium">
          Session ID: <span className="font-mono text-slate-800">{sessionId}</span>
        </div>
      </div>

      {/* Chat Messages Container */}
      <div className="bg-white rounded-3xl border border-slate-200 shadow-sm flex flex-col h-[650px] overflow-hidden">
        {/* Messages List */}
        <div className="flex-1 p-6 overflow-y-auto space-y-5 bg-slate-50/50">
          {messages.map((m) => (
            <div
              key={m.id}
              className={`flex flex-col ${m.sender === 'user' ? 'items-end' : 'items-start'}`}
            >
              <div className="flex items-end space-x-2 max-w-[88%]">
                {m.sender === 'bot' && (
                  <div className="w-8 h-8 rounded-full bg-blue-700 text-white flex items-center justify-center text-xs font-bold shrink-0 mb-1">
                    JS
                  </div>
                )}
                <div
                  className={`p-4 sm:p-5 rounded-2xl text-xs sm:text-sm leading-relaxed shadow-xs ${
                    m.sender === 'user'
                      ? 'bg-blue-600 text-white rounded-br-none'
                      : 'bg-white text-slate-800 border border-slate-200 rounded-bl-none'
                  }`}
                >
                  <div className="whitespace-pre-line">{m.text}</div>

                  {m.sender === 'bot' && (
                    <div className="mt-3 pt-3 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
                      <span>{m.time}</span>
                      <button
                        onClick={() => speakText(m.text)}
                        className="text-blue-600 hover:text-blue-800 font-semibold flex items-center space-x-1 hover:underline"
                        title="Read aloud"
                      >
                        <span>🔊</span>
                        <span>{t.btn_listen}</span>
                      </button>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex items-center space-x-2 text-slate-400 text-xs">
              <div className="w-8 h-8 rounded-full bg-blue-100 text-blue-700 flex items-center justify-center text-xs font-bold animate-pulse">
                JS
              </div>
              <div className="bg-white border border-slate-200 px-4 py-2.5 rounded-2xl flex items-center space-x-2 shadow-xs">
                <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce"></span>
                <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce [animation-delay:0.2s]"></span>
                <span className="w-2 h-2 rounded-full bg-blue-600 animate-bounce [animation-delay:0.4s]"></span>
                <span className="text-slate-500 font-medium">Checking eligibility rules...</span>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Quick Prompts Bar */}
        <div className="bg-slate-100 border-t border-slate-200 px-4 py-2.5 flex items-center space-x-2 overflow-x-auto text-xs">
          <span className="text-slate-500 font-bold shrink-0">Quick Ask:</span>
          {quickPrompts.map((p, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(p)}
              className="bg-white hover:bg-blue-50 border border-slate-200 hover:border-blue-300 text-slate-700 px-3 py-1 rounded-full shrink-0 transition"
            >
              {p}
            </button>
          ))}
        </div>

        {/* Input Bar */}
        <div className="p-4 bg-white border-t border-slate-200">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center space-x-3"
          >
            <input
              type="text"
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder={t.chat_input_placeholder}
              className="flex-1 px-4 py-3 rounded-2xl border border-slate-200 text-sm focus:outline-none focus:border-blue-600 focus:ring-1 focus:ring-blue-600"
            />
            <button
              type="submit"
              disabled={isLoading || !inputText.trim()}
              className="bg-blue-700 hover:bg-blue-800 disabled:opacity-50 text-white font-bold px-6 py-3 rounded-2xl text-sm transition shadow-md shrink-0 flex items-center space-x-1"
            >
              <span>Ask</span>
              <span>→</span>
            </button>
          </form>
          <p className="text-[10px] text-slate-400 text-center mt-2 italic">
            {t.chat_disclaimer}
          </p>
        </div>
      </div>
    </div>
  );
};
