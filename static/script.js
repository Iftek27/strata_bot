document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("chat-form");
  const input = document.getElementById("user-input");
  const chatBox = document.getElementById("chat-box");

  function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
  }

  // Add message (user or bot)
  function addMessage(text, sender = "bot") {
    const wrap = document.createElement("div");
    wrap.className = "flex gap-2 " + (sender === "user" ? "justify-end" : "justify-start");

    const bubble = document.createElement("div");
    bubble.className =
      "px-3 py-2 rounded-2xl text-sm max-w-[80%] leading-relaxed " +
      (sender === "user"
        ? "bg-indigo-600 text-white rounded-br-sm"
        : "bg-indigo-50 text-gray-800 rounded-bl-sm");

    bubble.innerHTML = text.replace(/\n/g, "<br>");

    if (sender === "user") {
      wrap.appendChild(bubble);
      wrap.appendChild(
        Object.assign(document.createElement("div"), {
          className: "h-8 w-8 rounded-full bg-gray-300 flex items-center justify-center text-xs",
          innerText: "You",
        })
      );
    } else {
      wrap.appendChild(
        Object.assign(document.createElement("img"), {
          src: "/static/logo.png",   // ✅ Bot avatar is your logo
          className: "h-8 w-8 rounded",
        })
      );
      wrap.appendChild(bubble);
    }

    chatBox.appendChild(wrap);
    scrollToBottom();
  }

  // Add typing indicator
  function addTyping() {
    const wrap = document.createElement("div");
    wrap.id = "typing";
    wrap.className = "flex gap-2";
    wrap.innerHTML = `
      <img src="/static/logo.png" class="h-8 w-8 rounded">
      <div class="px-3 py-2 rounded-2xl text-sm bg-indigo-50 text-gray-600">
        <span class="animate-pulse">Thinking…</span>
      </div>
    `;
    chatBox.appendChild(wrap);
    scrollToBottom();
  }

  function removeTyping() {
    const t = document.getElementById("typing");
    if (t) t.remove();
  }

  // Handle form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const question = input.value.trim();
    if (!question) return;

    // Add user message
    addMessage(question, "user");
    input.value = "";

    // Show typing
    addTyping();

    try {
      const res = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question }),
      });
      const data = await res.json();

      removeTyping();
      addMessage(data.answer, "bot");
    } catch (err) {
      removeTyping();
      addMessage("⚠ Error connecting to server.", "bot");
    }
  });

  // Allow Enter to send, Shift+Enter = newline
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      form.dispatchEvent(new Event("submit"));
    }
  });
});
