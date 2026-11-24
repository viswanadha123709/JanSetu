// JanSetu REST API Client
const API_BASE = '/api';

// Helper for CSRF token from cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

window.JanSetuAPI = {
  // Auth
  async login(username, password) {
    const res = await fetch(`${API_BASE}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ username, password })
    });
    return res.json();
  },

  async register(data) {
    const res = await fetch(`${API_BASE}/auth/register/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify(data)
    });
    return res.json();
  },

  async logout() {
    const res = await fetch(`${API_BASE}/auth/logout/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') }
    });
    return res.json();
  },

  async getProfile() {
    const res = await fetch(`${API_BASE}/auth/profile/`);
    return res.json();
  },

  async updateProfile(data) {
    const res = await fetch(`${API_BASE}/auth/profile/`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify(data)
    });
    return res.json();
  },

  // Schemes & Policies
  async getSchemes(params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${API_BASE}/schemes/?${query}`);
    return res.json();
  },

  async getScheme(id) {
    const res = await fetch(`${API_BASE}/schemes/${id}/`);
    return res.json();
  },

  async getPolicies(params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${API_BASE}/policies/?${query}`);
    return res.json();
  },

  async getPolicy(id) {
    const res = await fetch(`${API_BASE}/policies/${id}/`);
    return res.json();
  },

  async getCategories() {
    const res = await fetch(`${API_BASE}/categories/`);
    return res.json();
  },

  async getStates() {
    const res = await fetch(`${API_BASE}/states/`);
    return res.json();
  },

  async getStats() {
    const res = await fetch(`${API_BASE}/stats/`);
    return res.json();
  },

  // AI Eligibility Chat
  async sendChatMessage(question, sessionId, language = 'en') {
    const res = await fetch(`${API_BASE}/eligibility/chat/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ question, session_id: sessionId, language })
    });
    return res.json();
  },

  async getChatHistory(sessionId) {
    const res = await fetch(`${API_BASE}/eligibility/history/?session_id=${sessionId}`);
    return res.json();
  },

  // Document Analysis
  async uploadDocument(file) {
    const formData = new FormData();
    formData.append('file', file);
    const res = await fetch(`${API_BASE}/documents/upload/`, {
      method: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      body: formData
    });
    return res.json();
  },

  async loadSampleDocument(sampleType) {
    const res = await fetch(`${API_BASE}/documents/sample/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ sample_type: sampleType })
    });
    return res.json();
  },

  async getDocument(id) {
    const res = await fetch(`${API_BASE}/documents/${id}/`);
    return res.json();
  },

  async getDocumentClauses(id, params = {}) {
    const query = new URLSearchParams(params).toString();
    const res = await fetch(`${API_BASE}/documents/${id}/clauses/?${query}`);
    return res.json();
  },

  async askDocumentQuestion(docId, question, language = 'en') {
    const res = await fetch(`${API_BASE}/documents/${docId}/ask/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCookie('csrftoken') },
      body: JSON.stringify({ question, language })
    });
    return res.json();
  },

  async getRecentDocuments() {
    const res = await fetch(`${API_BASE}/documents/`);
    return res.json();
  }
};
