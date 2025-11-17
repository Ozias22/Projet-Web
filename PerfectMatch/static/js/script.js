"use strict";

const  divProfils = document.getElementById("bloc_profils");

function creerCardProfil(unProfil,imagesProfil){
        const container = document.createElement("div");
        container.classList.add("col-md-8");

        const card = document.createElement("div");
        card.classList.add("card", "w-100", "mb-4");

        // Image
        const img = document.createElement("img");
        img.src = imagesProfil[0];
        img.classList.add("card-img-top");
        img.alt = "image profil utilisateur";
        card.appendChild(img);

        // Card body
        const cardBody1 = document.createElement("div");
        cardBody1.classList.add("card-body");

        const nom = document.createElement("h5");
        nom.classList.add("card-title", "fw-semibold");
        nom.textContent = unProfil.name;

        const bio = document.createElement("p");
        bio.classList.add("card-text");
        bio.textContent = unProfil.bio;

        cardBody1.appendChild(nom);
        cardBody1.appendChild(bio);
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

function afficherProfils(){
    let response = RecupereProfils()
    let profils = response.values.profiles;
    let imagesProfils = response.values.images;
    var unProfil = profils.pop();
    var imagesProfil = [];
    for(let img of imagesProfils){
        if(img.user_id === unProfil.user_id){
            imagesProfil.push(img.image);
        }
    }
    creerCardProfil(unProfil,imagesProfil);
}

async function RecupereProfils(){
    try{
        const response = await fetch('/api/obtenir_profil/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log("Profiles retrieved successfully.");
        const data = response.json();
        return data;
    }
    catch(error){
        console.error("Error fetching profiles:", error);
        console.log("Failed to retrieve profiles.");
    }
}

function initialisation() {
    console.log("Script loaded successfully.");
    afficherProfils();
}

window.addEventListener('DOMContentLoaded', initialisation);