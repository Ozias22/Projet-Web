"use strict";

//Discussion actuelle
var receiver_Id = null;
let lastMessageId = null;

async function loadDiscussions() {
  const response = await fetch("/api/discussions/");
  const discussions = await response.json();

  const list = document.getElementById("list-partenaire");
  list.innerHTML = "";

  discussions.forEach((user) => {
    const item = document.createElement("li");
    item.className =
      "list-group-item list-group-item-action d-flex align-items-start";
    item.innerHTML = `
    <img src="${
      user.photo_profil
    }" class="rounded-circle me-3 " width="52" height="52">

    <div class="flex-grow-1 ${user.is_unread ? "fw-bold" : "text-muted"}">

      <div class="fw-bold">${user.username}</div>
      
      <div class="discussion-preview">${user.last_message}</div>

      <small class="discussion-timestamp">
    ${user.last_timestamp ?? ""}
    </small>

    </div>
    `;

    item.onclick = () => {
      loadMessages(user.user_id);
    };

    list.appendChild(item);
  });
}

async function loadMessages(userId) {
  receiver_Id = userId;
  lastMessageId = null;

  const response = await fetch(`/api/messages/${userId}/`);
  const messages = await response.json();

  const container = document.getElementById("messages");
  container.innerHTML = "";

  messages.forEach((msg) => {
    const row = document.createElement("div");
    row.classList.add("message-row");
    row.classList.add(msg.is_self ? "message-right" : "message-left");

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.classList.add(msg.is_self ? "bubble-right" : "bubble-left");

    bubble.innerHTML = `
      <b>${msg.sender}</b><br>
      ${msg.content}<br>
      <small class="text-muted">${msg.timestamp}</small>`;

    row.appendChild(bubble);
    container.appendChild(row);

    lastMessageId = msg.id;
  });

  container.scrollTop = container.scrollHeight;
}

async function envoyerMessage(e) {
  e.preventDefault();
  const input = document.getElementById("message-input");
  const content = input.value;
  console.log("Receiver ID:", receiver_Id);
  if (!content || !receiver_Id) return;
  try {
    const response = await fetch(`/api/envoyer_message/${receiver_Id}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content }),
    });
    if (response.ok) {
      input.value = "";
      const data = await response.json();
      console.log("Message envoyé:", data);
      loadMessages(receiver_Id);
      return data;
    } else {
      const errorText = await response.text();
      console.error("Erreur serveur:", response.status, errorText);
    }
  } catch (error) {
    console.error("Erreur lors de l'envoi du message:", error);
  }
}

function apiTimeLoop() {
  setInterval(() => {
    fetchNewDiscussions();
  }, 5000);
}

async function fetchNewDiscussions() {
  //Rafriachissement des messages si disuccusion ouvert
  if (receiver_Id !== null) {
    await fetchNewMessageForCurrentDiscussion();
  }
  //Rafraichisement des discussions
  await loadDiscussions();
}

async function fetchNewMessageForCurrentDiscussion() {
  if (!receiver_Id) return;

  const response = await fetch(`/api/messages/${receiver_Id}/`);
  const messages = await response.json();

  if (messages.length === 0) return;

  const newest = messages[messages.length - 1];

  if (lastMessageId === newest.id) return;

  const container = document.getElementById("messages");

  messages.forEach((msg) => {
    if (lastMessageId && msg.id <= lastMessageId) return;

    const row = document.createElement("div");
    row.classList.add("message-row");
    row.classList.add(msg.is_self ? "message-right" : "message-left");

    const bubble = document.createElement("div");
    bubble.classList.add("bubble");
    bubble.classList.add(msg.is_self ? "bubble-right" : "bubble-left");

    bubble.innerHTML = `
      <b>${msg.sender}</b><br>
      ${msg.content}<br>
      <small class="text-muted">${msg.timestamp}</small>`;

    row.appendChild(bubble);
    container.appendChild(row);

    lastMessageId = msg.id;
  });

  container.scrollTop = container.scrollHeight;
}

function initialisation() {
  loadDiscussions();
  apiTimeLoop();
}

window.addEventListener("DOMContentLoaded", initialisation);
let btnEnvoyer = document.getElementById("send-btn");
btnEnvoyer.addEventListener("click", (e) => envoyerMessage(e));
