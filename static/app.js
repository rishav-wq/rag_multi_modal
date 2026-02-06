async function postJSON(url, data) {
  const resp = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return resp.json();
}

function hideWelcome() {
  const welcome = document.querySelector(".welcome-message");
  if (welcome) {
    welcome.style.display = "none";
  }
}

function appendMessage(role, text, isThinking = false, mode = null) {
  hideWelcome();
  const log = document.getElementById("chat-log");
  
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role}`;
  if (isThinking) messageDiv.classList.add("thinking");
  
  // Avatar
  const avatar = document.createElement("div");
  avatar.className = "message-avatar";
  avatar.textContent = role === "user" ? "👤" : "🤖";
  
  // Content
  const content = document.createElement("div");
  content.className = "message-content";
  
  // Add mode badge for assistant messages
  if (role === "assistant" && mode && !isThinking) {
    const badge = document.createElement("div");
    badge.style.cssText = "font-size: 11px; color: var(--text-secondary); margin-bottom: 6px; font-weight: 500;";
    
    if (mode === "online") {
      badge.innerHTML = "⚡ Online Mode (Groq)";
      badge.style.color = "#10b981"; // green
    } else if (mode === "offline") {
      badge.innerHTML = "💻 Offline Mode (phi3:mini)";
      badge.style.color = "#f59e0b"; // amber
    }
    
    content.appendChild(badge);
  }
  
  const textDiv = document.createElement("div");
  textDiv.textContent = text;
  content.appendChild(textDiv);
  
  if (role === "user") {
    messageDiv.appendChild(content);
    messageDiv.appendChild(avatar);
  } else {
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(content);
  }
  
  log.appendChild(messageDiv);
  log.scrollTop = log.scrollHeight;
  
  return messageDiv;
}

function renderContexts(contexts) {
  const sidebar = document.getElementById("context-sidebar");
  const container = document.getElementById("context-list");
  container.innerHTML = "";
  
  if (!contexts || contexts.length === 0) {
    container.innerHTML = '<div style="color: var(--text-secondary); text-align: center; padding: 20px;">No context retrieved.</div>';
    return;
  }
  
  // Show sidebar
  sidebar.classList.add("visible");
  
  contexts.forEach((c, idx) => {
    const chunkDiv = document.createElement("div");
    chunkDiv.className = "context-chunk";
    
    const meta = document.createElement("div");
    meta.className = "context-meta";
    meta.innerHTML = `
      <span>📄 ${c.source}</span>
      <span>Score: ${c.score.toFixed(3)}</span>
    `;
    
    const textDiv = document.createElement("div");
    textDiv.className = "context-chunk-text";
    textDiv.textContent = c.text;
    
    chunkDiv.appendChild(meta);
    chunkDiv.appendChild(textDiv);
    container.appendChild(chunkDiv);
  });
}

window.addEventListener("DOMContentLoaded", () => {
  const ingestBtn = document.getElementById("ingest-btn");
  const ingestStatus = document.getElementById("ingest-status");
  const form = document.getElementById("chat-form");
  const questionInput = document.getElementById("question-input");
  const sendBtn = document.getElementById("send-btn");
  const modeSelect = document.getElementById("mode-select");
  const toggleContextBtn = document.getElementById("toggle-context");
  const closeContextBtn = document.getElementById("close-context");
  const contextSidebar = document.getElementById("context-sidebar");
  const chatLog = document.getElementById("chat-log");

  // Quick prompts
  document.querySelectorAll(".quick-prompt").forEach(btn => {
    btn.addEventListener("click", () => {
      const prompt = btn.getAttribute("data-prompt");
      questionInput.value = prompt;
      questionInput.focus();
    });
  });

  // Toggle context sidebar
  toggleContextBtn.addEventListener("click", () => {
    contextSidebar.classList.toggle("visible");
  });

  closeContextBtn.addEventListener("click", () => {
    contextSidebar.classList.remove("visible");
  });

  // Ingest documents
  ingestBtn.addEventListener("click", async () => {
    ingestBtn.disabled = true;
    ingestStatus.textContent = "Building index...";
    try {
      const res = await postJSON("/api/ingest", {});
      ingestStatus.textContent = "✅ " + (res.message || "Index built successfully");
      setTimeout(() => {
        ingestStatus.textContent = "";
      }, 3000);
    } catch (e) {
      ingestStatus.textContent = "❌ Error building index";
    } finally {
      ingestBtn.disabled = false;
    }
  });

  // Handle form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = questionInput.value.trim();
    if (!question) return;

    // Add user message
    appendMessage("user", question);
    questionInput.value = "";
    sendBtn.disabled = true;

    // Add thinking message
    const thinkingMsg = appendMessage("assistant", "Thinking...", true);
    
    const mode = modeSelect.value;
    try {
      const res = await postJSON("/api/chat", { question, mode });
      
      // Remove thinking message
      if (thinkingMsg && thinkingMsg.parentNode) {
        thinkingMsg.parentNode.removeChild(thinkingMsg);
      }

      if (res.status !== "ok") {
        appendMessage("assistant", `Error: ${res.message || "Unknown error"}`);
        return;
      }
      
      // Render contexts
      renderContexts(res.contexts);
      
      // Add assistant answer with mode badge
      appendMessage("assistant", res.answer, false, res.mode);
      
    } catch (err) {
      // Remove thinking message
      if (thinkingMsg && thinkingMsg.parentNode) {
        thinkingMsg.parentNode.removeChild(thinkingMsg);
      }
      appendMessage("assistant", "Error contacting server.");
    } finally {
      sendBtn.disabled = false;
      questionInput.focus();
    }
  });

  // Auto-focus input
  questionInput.focus();
});

