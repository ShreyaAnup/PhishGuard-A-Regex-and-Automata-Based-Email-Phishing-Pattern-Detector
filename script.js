let currentMode = "message";
const input = document.getElementById("inputText");
const modeLabels = {
  message: { label: "Paste an email or message", placeholder: "Example: URGENT! Verify your account now and enter your password…" },
  url: { label: "Paste a URL", placeholder: "https://example.com/account/verify" },
  email: { label: "Enter an email address", placeholder: "name@example.com" }
};
document.querySelectorAll(".mode").forEach(btn => btn.addEventListener("click", () => {
  document.querySelectorAll(".mode").forEach(b => b.classList.remove("active"));
  btn.classList.add("active");
  currentMode = btn.dataset.mode;
  document.getElementById("inputLabel").textContent = modeLabels[currentMode].label;
  input.placeholder = modeLabels[currentMode].placeholder;
  document.getElementById("errorMsg").textContent = "";
}));
input.addEventListener("input", () => document.getElementById("charCount").textContent = `${input.value.length} / 10000`);
document.getElementById("sampleBtn").addEventListener("click", () => {
  const samples = {
    message: "URGENT! Your account is suspended. Click here to verify your password immediately: https://bit.ly/demo-login",
    url: "https://bit.ly/demo-login",
    email: "support@example.com"
  };
  input.value = samples[currentMode];
  document.getElementById("charCount").textContent = `${input.value.length} / 10000`;
});
document.getElementById("analyzeBtn").addEventListener("click", analyze);
async function analyze() {
  const text = input.value.trim();
  const error = document.getElementById("errorMsg");
  error.textContent = "";
  if (!text) { error.textContent = "Please enter some text to analyze."; return; }
  const btn = document.getElementById("analyzeBtn");
  btn.disabled = true; btn.textContent = "Analyzing…";
  try {
    const response = await fetch("/api/analyze", {
      method: "POST", headers: {"Content-Type":"application/json"},
      body: JSON.stringify({text, mode: currentMode})
    });
    if (!response.ok) throw new Error("The server could not analyze this input.");
    renderResults(await response.json());
  } catch (e) {
    error.textContent = "Could not reach the backend. Start the FastAPI server and try again.";
  } finally {
    btn.disabled = false; btn.innerHTML = 'Analyze patterns <span>↗</span>';
  }
}
function renderResults(data) {
  document.getElementById("emptyState").hidden = true;
  document.getElementById("results").hidden = false;
  document.getElementById("score").textContent = data.risk_score;
  document.getElementById("riskLevel").textContent = data.risk_level;
  const fill = document.getElementById("meterFill");
  fill.style.width = `${data.risk_score}%`;
  fill.style.background = data.risk_score >= 50 ? "#d9799c" : data.risk_score >= 25 ? "#c4a33b" : "#4c8c68";
  const chip = document.getElementById("riskLevel");
  chip.style.background = data.risk_score >= 50 ? "#fff0f5" : data.risk_score >= 25 ? "#fff9df" : "#eff9ef";
  chip.style.color = data.risk_score >= 50 ? "#99546e" : data.risk_score >= 25 ? "#8c751d" : "#4c8c68";
  const emailStatus = document.getElementById("emailStatus");
  if (data.email_format_valid !== null) {
    emailStatus.hidden = false;
    emailStatus.textContent = data.email_format_valid ? "✓ Format looks plausible. This does not authenticate the sender." : "ⓘ Email format did not match the project's validation rule.";
  } else emailStatus.hidden = true;
  const findings = document.getElementById("findings");
  findings.replaceChildren();
  data.findings.forEach(item => {
    const div = document.createElement("div"); div.className = `finding ${item.severity}`;
    const dot = document.createElement("span"); dot.className = "finding-dot";
    const content = document.createElement("div");
    const title = document.createElement("h4"); title.textContent = item.title;
    const detail = document.createElement("p"); detail.textContent = item.detail;
    content.append(title, detail); div.append(dot, content); findings.append(div);
  });
  document.getElementById("disclaimer").textContent = data.disclaimer;
}
document.getElementById("traceBtn").addEventListener("click", runTrace);
async function runTrace() {
  const text = document.getElementById("traceInput").value;
  const status = document.getElementById("traceStatus");
  const steps = document.getElementById("traceSteps");
  try {
    const response = await fetch("/api/automata/trace", {
      method:"POST", headers:{"Content-Type":"application/json"},
      body:JSON.stringify({text, mode:"message"})
    });
    const data = await response.json();
    steps.replaceChildren();
    data.trace.forEach((item, idx) => {
      const chip = document.createElement("span"); chip.className = "trace-step";
      chip.innerHTML = `${item.index === 0 ? "START" : escapeHtml(item.character)} → <b>${item.state}</b>`;
      steps.append(chip);
    });
    document.getElementById("stateQ0").classList.toggle("active-state", data.final_state === "q0");
    document.getElementById("stateQ1").classList.toggle("active-state", data.final_state === "q1");
    status.textContent = data.accepted ? "Accepted: digit found" : "Rejected: no digit";
  } catch(e) { status.textContent = "Backend unavailable"; }
}
function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[c]));
}
document.getElementById("regex101Link").addEventListener("click", () => {});
runTrace();
