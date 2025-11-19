"use strict";

const  divProfils = document.getElementById("bloc_profils");

function creerCardProfil(){
        const container = document.createElement("div");
        container.classList.add("col-md-8");

        const card = document.createElement("div");
        card.classList.add("card", "w-100", "mb-4");

        // Image
        const img = document.createElement("img");
        img.src = "../../static/images/Untitled.jpg";
        img.classList.add("card-img-top");
        img.alt = "image profil utilisateur";
        card.appendChild(img);

        // Card body
        const cardBody1 = document.createElement("div");
        cardBody1.classList.add("card-body");

        const title = document.createElement("h5");
        title.classList.add("card-title", "fw-semibold");
        title.textContent = "Ozias, 22";

        const text = document.createElement("p");
        text.classList.add("card-text");
        text.textContent = "Some quick example text to build on the card title and make up the bulk of the card’s content.";

        cardBody1.appendChild(title);
        cardBody1.appendChild(text);
        card.appendChild(cardBody1);

        const ul = document.createElement("ul");
        ul.classList.add("w-25", "alignement-gauche");

        const items = [
        { icon: "bi-geo-alt", text: "Localisation" },
        { icon: "bi-briefcase", text: "Job" },
        { icon: "bi-geo-alt", text: "An item" },
        { icon: "bi-geo-alt", text: "An item" }
        ];

        items.forEach(item => {
        const wrapper = document.createElement("div");
        wrapper.classList.add("d-flex", "justify-content-between", "mb-2");

        const icon = document.createElement("i");
        icon.classList.add("bi", item.icon);

        const li = document.createElement("li");
        li.classList.add("list-group-item");
        li.textContent = item.text;

        wrapper.appendChild(icon);
        wrapper.appendChild(li);
        ul.appendChild(wrapper);
        });

        card.appendChild(ul);

        const likeWrapper = document.createElement("div");
        likeWrapper.classList.add("d-flex", "justify-content-between", "mx-4", "w-75");

        const dislike = document.createElement("div");
        dislike.classList.add("fs-1", "text-dark", "mx-2");
        dislike.id = "!jaime";
        dislike.innerHTML = '<i class="bi bi-x-lg"></i>';

        const like = document.createElement("div");
        like.classList.add("fs-1", "text-primary");
        like.id = "jaime";
        like.innerHTML = '<i class="bi bi-heart-fill"></i>';

        likeWrapper.appendChild(dislike);
        likeWrapper.appendChild(like);
        card.appendChild(likeWrapper);

        // Card links
        const cardBody2 = document.createElement("div");
        cardBody2.classList.add("card-body");

        const link1 = document.createElement("a");
        link1.href = "#";
        link1.classList.add("card-link");
        link1.textContent = "Card link";

        const link2 = document.createElement("a");
        link2.href = "#";
        link2.classList.add("card-link");
        link2.textContent = "Another link";

        cardBody2.appendChild(link1);
        cardBody2.appendChild(link2);
        card.appendChild(cardBody2);

        // Final assembly
        container.appendChild(card);
        divProfils.appendChild(container);
}

async function RecupereProfils(){
    try{
        const response = await fetch('/api/obtenir_profil/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log("Profiles retrieved successfully.");
        const data = await response.json();
        console.log(data);
    }
    catch(error){
        console.error("Error fetching profiles:", error);
        console.log("Failed to retrieve profiles.");
    }
}

function initialisation() {
    creerCardProfil();
    console.log("Script loaded successfully.");
    RecupereProfils();
}

window.addEventListener('DOMContentLoaded', initialisation);
document.addEventListener("DOMContentLoaded", function () {

    const buttons = document.querySelectorAll('.btn-supprimer-image');

    buttons.forEach(btn => {
        btn.addEventListener('click', function () {

            const imageId = this.dataset.id;
            const url = window.urlSupprimerImage;
            const csrf = window.csrfToken;

            if (!imageId) {
                console.error("Pas d'ID image");
                return;
            }

            fetch(url, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrf,
                    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: new URLSearchParams({ image_id: imageId }).toString()
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const div = document.getElementById(`image-${imageId}`);
                    if (div) div.remove();
                } else {
                    alert(data.error || "Erreur lors de la suppression.");
                }
            })
            .catch(err => {
                console.error(err);
                alert("Erreur réseau.");
            });
        });
    });

});
