const yearEl = document.getElementById('year');
if (yearEl) yearEl.textContent = new Date().getFullYear();

const header = document.getElementById('siteHeader');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 40);
  });
}

const coverImg = document.getElementById('coverImg');
const bookCover = document.getElementById('bookCover');
if (coverImg && bookCover) {
  coverImg.addEventListener('error', () => bookCover.classList.add('no-image'));
}

const revealEls = document.querySelectorAll('[data-reveal]');
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.15 });
revealEls.forEach(el => observer.observe(el));

const form = document.querySelector('.contact-form');
if (form) {
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const btn = form.querySelector('button');
    const original = btn.textContent;
    btn.textContent = 'Thank You!';
    form.querySelector('input').value = '';
    setTimeout(() => { btn.textContent = original; }, 2500);
  });
}

/* ============================
   Glow Era AI Assistant Widget
   ============================ */
(function () {
  // IMPORTANT: replace this with your actual Cloudflare Worker URL once deployed
  const WORKER_URL = "https://glow-era-chat.babynteo.workers.dev/";

  const conversation = [];

  function escapeHTML(str) {
    const div = document.createElement("div");
    div.textContent = str;
    return div.innerHTML;
  }

  // Very small markdown-link renderer: [text](url) -> <a href="url">text</a>
  function renderLinks(text) {
    const escaped = escapeHTML(text);
    return escaped.replace(
      /\[([^\]]+)\]\(([^)]+)\)/g,
      '<a href="$2" target="_blank" rel="noopener">$1</a>'
    );
  }

  function buildWidget() {
    const bubble = document.createElement("button");
    bubble.id = "glow-chat-bubble";
    bubble.setAttribute("aria-label", "Ask Glow Era");
    bubble.innerHTML = "&#10022;";

    const win = document.createElement("div");
    win.id = "glow-chat-window";
    win.innerHTML = `
      <div id="glow-chat-header">
        <span>Ask Glow Era</span>
        <button id="glow-chat-close" aria-label="Close chat">&times;</button>
      </div>
      <div id="glow-chat-messages">
        <div class="glow-msg glow-msg-assistant">Hi! I'm here to help with wellness questions, self-care, boundaries, rest, travel wellness, and more. What's on your mind?</div>
      </div>
      <div id="glow-chat-input-row">
        <input id="glow-chat-input" type="text" placeholder="Ask a wellness question..." autocomplete="off">
        <button id="glow-chat-send" aria-label="Send">&#10148;</button>
      </div>
    `;

    document.body.appendChild(bubble);
    document.body.appendChild(win);

    const messagesEl = win.querySelector("#glow-chat-messages");
    const inputEl = win.querySelector("#glow-chat-input");
    const sendBtn = win.querySelector("#glow-chat-send");
    const closeBtn = win.querySelector("#glow-chat-close");

    bubble.addEventListener("click", () => {
      win.classList.toggle("open");
      if (win.classList.contains("open")) inputEl.focus();
    });
    closeBtn.addEventListener("click", () => win.classList.remove("open"));

    function addMessage(role, text) {
      const div = document.createElement("div");
      div.className = "glow-msg " + (role === "user" ? "glow-msg-user" : "glow-msg-assistant");
      div.innerHTML = role === "user" ? escapeHTML(text) : renderLinks(text);
      messagesEl.appendChild(div);
      messagesEl.scrollTop = messagesEl.scrollHeight;
    }

    async function sendMessage() {
      const text = inputEl.value.trim();
      if (!text) return;

      addMessage("user", text);
      conversation.push({ role: "user", content: text });
      inputEl.value = "";
      sendBtn.disabled = true;

      const loadingEl = document.createElement("div");
      loadingEl.className = "glow-msg-loading";
      loadingEl.textContent = "Thinking...";
      messagesEl.appendChild(loadingEl);
      messagesEl.scrollTop = messagesEl.scrollHeight;

      try {
        const res = await fetch(WORKER_URL, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ messages: conversation }),
        });
        const data = await res.json();
        loadingEl.remove();

        // TEMPORARY DIAGNOSTIC: remove this line once the issue is fixed
        console.log("Glow Era Chat - raw response:", data);

        if (data.content && data.content[0] && data.content[0].text) {
          const reply = data.content[0].text;
          addMessage("assistant", reply);
          conversation.push({ role: "assistant", content: reply });
        } else {
          addMessage("assistant", "Sorry, I couldn't get a response just now. Please try again in a moment.");
        }
      } catch (err) {
        loadingEl.remove();
        addMessage("assistant", "Sorry, something went wrong. Please try again in a moment.");
      } finally {
        sendBtn.disabled = false;
      }
    }

    sendBtn.addEventListener("click", sendMessage);
    inputEl.addEventListener("keydown", (e) => {
      if (e.key === "Enter") sendMessage();
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", buildWidget);
  } else {
    buildWidget();
  }
})();
