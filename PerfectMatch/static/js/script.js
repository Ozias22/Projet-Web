function toggleNotifications() {
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
                            <small>${msg.timestamp}</small>
                        </div>
                    `;
                });
            }

            popup.style.display = "block";
        })
        .catch(err => console.error("Erreur notifications:", err));
}
