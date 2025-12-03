"use strict";

var receiver_Id = null;
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
  console.log("Messages reçus:", messages);

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

    receiver_Id = userId;
  });
}

async function envoyerMessage() {
  const input = document.getElementById("message-input");
  const content = input.value;
  console.log("Receiver ID:", receiver_Id);
  if (!content || !receiver_Id) return;
  try{
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
  }
  catch(error){
    console.error("Erreur lors de l'envoi du message:", error);
  }
}


window.addEventListener("DOMContentLoaded", loadDiscussions);
let btnEnvoyer = document.getElementById("send-btn");
btnEnvoyer.addEventListener("click", () => envoyerMessage());

