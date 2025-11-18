"use strict";

async function loadDiscussions() {
  const response = await fetch("/api/discussions/");
  const discussions = await response.json();

  const list = document.getElementById("list-partenaire");
  list.innerHTML = "";

  discussions.forEach(user => {
    const item = document.createElement("li");
    item.className = "list-group-item list-group-item-action";
    item.textContent = user.username;
    item.onclick = () => loadMessages(user.id);
    list.appendChild(item);
  });
}

async function loadMessages(userId) {
  const response = await fetch(`/api/messages/${userId}/`);
  const messages = await response.json();

  const container = document.getElementById("messages");
  container.innerHTML = "";

  messages.forEach(msg => {
    const row = document.createElement("div");
    row.classList.add("message-row");
    row.classList.add(msg.is_self ? "message-right" : "message-left");

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.classList.add(msg.is_self ? "bubble-right" : "bubble-left");

    bubble.innerHTML = `
        <b>${msg.sender}</b><br>
        ${msg.content}<br>
        <small class="text-muted">${msg.timestamp}</small>
    `;

    row.appendChild(bubble);
    container.appendChild(row);
  });
}

window.addEventListener("DOMContentLoaded", loadDiscussions);
