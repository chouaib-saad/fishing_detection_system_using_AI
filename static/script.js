const translations = {
    en: {
        heroTitle: "Advanced Threat Detection",
        heroSubtitle: "Enterprise-grade phishing analysis powered by machine learning.",
        analyzeUrl: "Analyze URL",
        analyzeBtn: "Scan URL",
        analysisReport: "Analysis Report",
        howItWorks: "How It Works",
        feature1: "Real-time heuristic & ML analysis",
        feature2: "Domain reputation checking",
        feature3: "Pattern matching engine",
        capabilities: "Capabilities",
        accuracy: "Accuracy",
        latency: "Latency",
        footerRights: "All rights reserved.",
        viewDocs: "Documentation",
        apiReference: "API Reference",

        // Dynamic Results
        analyzing: "Analyzing threat vectors...",
        error: "Analysis Error",
        safe: "SAFE",
        phishing: "THREAT DETECTED",
        suspicious: "SUSPICIOUS ACTIVITY",
        confidence: "Confidence Score",
        urlLabel: "URL",
        details: "Technical Details"
    },
    tn: {
        heroTitle: "Kachf el Rawabit el Khbitha",
        heroSubtitle: "verifi link mta3k bel dhake2 el estiba7i",
        analyzeUrl: "Nchouflek el link sahbi ?",
        analyzeBtn: "sami besmelleh !",
        analysisReport: "Taqrir el Tahlil",
        howItWorks: "Kifach Yemchi?",
        feature1: "Tahlil fawri bel AI w Heuristics",
        feature2: "Tathabot mn sm3at el domain",
        feature3: "Kachf el anmat el khbitha",
        capabilities: "El Qodorat",
        accuracy: "Deqa",
        latency: "Sor3a",
        footerRights: "Jami3 el Hoqoq Mahfodha.",
        viewDocs: "Watha2eq",
        apiReference: "Marja3 el API",

        // Dynamic Results
        analyzing: "mahbaa mahbaa..",
        error: "Fama Ghalta",
        safe: "JAWWO FESFES ! (SAFE)",
        phishing: "LIEN KHBIRTH (PHISHING)",
        suspicious: "Lien Mchkouk Fih",
        confidence: "Nesbet el Thika",
        urlLabel: "Lien",
        details: "chwaya tfalsif"
    }
};

// Icons as SVG strings for professional look
const ICONS = {
    SAFE: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" fill="rgba(52, 211, 153, 0.2)" stroke="var(--accent-green)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M9 12L11 14L15 10" stroke="var(--accent-green)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    DANGER: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" fill="rgba(248, 113, 113, 0.2)" stroke="var(--accent-red)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 8V12" stroke="var(--accent-red)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 16H12.01" stroke="var(--accent-red)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`,
    UNKNOWN: `<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12 22C12 22 20 18 20 12V5L12 2L4 5V12C4 18 12 22 12 22Z" fill="rgba(251, 191, 36, 0.2)" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 8V12" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/><path d="M12 16H12.01" stroke="#fbbf24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>`
};

// State
let currentLang = localStorage.getItem('app_lang') || 'en';

// DOM Elements
const form = document.getElementById("checkForm");
const urlInput = document.getElementById("urlInput");
const resultDiv = document.getElementById("result");
const resultContent = document.getElementById("resultContent");
const submitBtn = document.querySelector('button[type="submit"]');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Set initial active button
    document.querySelectorAll('.lang-btn').forEach(btn => {
        if (btn.dataset.lang === currentLang) {
            btn.classList.add('active');
        } else {
            btn.classList.remove('active');
        }
    });

    updateLanguage(currentLang);
    setupEventListeners();
});

function setupEventListeners() {
    // Language Switcher
    document.querySelectorAll('.lang-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const lang = e.target.dataset.lang;
            if (lang && lang !== currentLang) {
                currentLang = lang;
                localStorage.setItem('app_lang', lang);
                updateLanguage(lang);

                // Update UI active state
                document.querySelectorAll('.lang-btn').forEach(b => b.classList.remove('active'));
                e.target.classList.add('active');
            }
        });
    });

    // Form Submission
    form.addEventListener("submit", handleSubmission);
}

function updateLanguage(lang) {
    const t = translations[lang];
    if (!t) return;

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.dataset.i18n;
        if (t[key]) {
            el.textContent = t[key];
        }
    });

    // Update placeholder
    if (lang === 'tn') {
        urlInput.placeholder = "7ot lien seehbi (mithal: https://example.com)";
    } else {
        urlInput.placeholder = "Enter URL to scan (e.g., https://example.com)";
    }
}

async function handleSubmission(e) {
    e.preventDefault();

    const ui = translations[currentLang];
    const url = urlInput.value;

    // UI Loading State
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<span class="spinner-sm"></span> ${ui.analyzing}`;
    resultDiv.classList.add("hidden");

    // Add artificial delay for "mahbaa mahbaa.." effect (3-4 seconds)
    if (currentLang === 'tn') {
        await new Promise(resolve => setTimeout(resolve, 3500));
    } else {
        // Shorter delay for EN just for smooth UI
        await new Promise(resolve => setTimeout(resolve, 1000));
    }

    try {
        const response = await fetch("/check", {
            method: "POST",
            headers: { "Content-Type": "application/x-www-form-urlencoded" },
            body: `url=${encodeURIComponent(url)}`
        });

        const data = await response.json();
        renderResult(data);
    } catch (error) {
        showError(error);
    } finally {
        submitBtn.disabled = false;
        submitBtn.textContent = ui.analyzeBtn; // Reset button text properly
    }
}

function renderResult(data) {
    const ui = translations[currentLang];
    resultDiv.classList.remove("hidden");

    if (data.error) {
        resultContent.innerHTML = `<div class="alert alert-error">${ui.error}: ${data.error}</div>`;
        return;
    }

    const isPhishing = data.result.includes("PHISHING") || data.result.includes("SUSPICIOUS");
    const isSafe = data.result.includes("SAFE");

    let statusLabel = isSafe ? ui.safe : (isPhishing ? ui.phishing : ui.suspicious);
    let statusClass = isSafe ? "status-safe" : (isPhishing ? "status-danger" : "status-unknown");
    let bgClass = isSafe ? "bg-safe" : (isPhishing ? "bg-danger" : "bg-unknown");
    let iconSvg = isSafe ? ICONS.SAFE : (isPhishing ? ICONS.DANGER : ICONS.UNKNOWN);
    let confidenceColor = isSafe ? "#34d399" : "#f87171";

    // Override Tunisian text for specific cases if needed
    if (currentLang === 'tn') {
        if (isSafe) statusLabel = "JAWWO FESFES ! (SAFE)";
        else if (isPhishing) statusLabel = "Nchouflek el link sahbi ? (PHISHING)";
    }

    const confidencePercent = (data.confidence * 100).toFixed(1);
    const timestamp = new Date().toLocaleTimeString();

    document.getElementById("timestamp").textContent = timestamp;

    resultContent.innerHTML = `
        <div class="result-card ${bgClass}" style="padding: 24px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.02);">
            <div class="result-status" style="display: flex; align-items: center; gap: 16px; margin-bottom: 24px;">
                <div class="status-icon-wrapper" style="display: flex; align-items: center; justify-content: center;">
                    ${iconSvg}
                </div>
                <div class="status-content">
                    <span class="status-text ${statusClass}" style="font-size: 1.5rem; font-weight: 700; letter-spacing: -0.02em;">${statusLabel}</span>
                </div>
            </div>
            
            <div class="meta-row" style="display: grid; grid-template-columns: 1fr auto; gap: 16px; margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid rgba(255,255,255,0.1);">
                <div class="meta-item">
                    <div class="meta-label" style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;">${ui.urlLabel}</div>
                    <div class="meta-value url-text" style="word-break: break-all; font-family: 'JetBrains Mono', monospace; color: #38bdf8;">${data.url}</div>
                </div>
                <div class="meta-item" style="text-align: right;">
                    <div class="meta-label" style="color: #94a3b8; font-size: 0.875rem; margin-bottom: 4px; text-transform: uppercase; letter-spacing: 0.05em;">${ui.confidence}</div>
                    <div class="meta-value" style="font-size: 1.5rem; font-weight: 700; color: ${confidenceColor};">${confidencePercent}%</div>
                </div>
            </div>
            
            <details class="tech-details">
                <summary style="cursor: pointer; color: #38bdf8; font-weight: 500; font-size: 0.9rem; transition: color 0.2s;">${ui.details}</summary>
                <div style="margin-top: 12px; background: rgba(15, 23, 42, 0.6); padding: 16px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.05);">
                    <pre style="overflow-x: auto; font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; color: #94a3b8; line-height: 1.5;">${JSON.stringify(data.features, null, 2)}</pre>
                </div>
            </details>
        </div>
    `;
}

function showError(error) {
    const ui = translations[currentLang];
    resultDiv.classList.remove("hidden");
    resultContent.innerHTML = `<div class="error-msg" style="color: #f87171; padding: 16px; background: rgba(248, 113, 113, 0.1); border-radius: 8px;">❌ ${ui.error}: ${error.message}</div>`;
}