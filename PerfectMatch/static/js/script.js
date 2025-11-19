function toggleNotifications() {
    // Faire disparaître le badge
    const badge = document.querySelector(".notif-badge");
    if (badge) badge.style.display = "none";

    let popup = document.getElementById("notif-popup");

    if (popup.style.display === "block") {
        popup.style.display = "none";
        return;
    }

    fetch("/notifications/")
        .then(response => response.json())
        .then(data => {
            popup.innerHTML = "";

            if (data.messages.length === 0) {
                popup.innerHTML = "<p>Aucune nouvelle notification.</p>";
            } else {
                data.messages.forEach(msg => {
                    popup.innerHTML += `
                        <div style="background:#d4edda; border-bottom:1px solid #eee; padding:5px; border-radius:4px; margin-bottom:3px;">
                            <strong>${msg.sender}</strong><br>
                            ${msg.content}<br>
                            <small>${msg.timestamp}</small><br>
                            <a href="/messages/${msg.id}/" class="btn btn-sm btn-primary mt-1">Voir</a>
                        </div>
                    `;
                });
            }

            popup.style.display = "block";
        })
        .catch(err => console.error("Erreur notifications:", err));
}
function toggleNotifications() {
    // Faire disparaître le badge
    const badge = document.querySelector(".notif-badge");
    if (badge) badge.style.display = "none";

    let popup = document.getElementById("notif-popup");

    if (popup.style.display === "block") {
        popup.style.display = "none";
        return;
    }

    fetch("/notifications/")
        .then(response => response.json())
        .then(data => {
            popup.innerHTML = "";

            if (data.messages.length === 0) {
                popup.innerHTML = "<p>Aucune nouvelle notification.</p>";
            } else {
                data.messages.forEach(msg => {
                    popup.innerHTML += `
                        <div style="background:#d4edda; border-bottom:1px solid #eee; padding:5px; border-radius:4px; margin-bottom:3px;">
                            <strong>${msg.sender}</strong><br>
                            ${msg.content}<br>
                            <small>${msg.timestamp}</small><br>
                            <a href="/messages/${msg.id}/" class="btn btn-sm btn-success mt-1">Voir</a>
                        </div>
                    `;
                });
            }

            popup.style.display = "block";
        })
        .catch(err => console.error("Erreur notifications:", err));
}
