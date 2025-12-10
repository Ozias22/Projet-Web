"use strict";

// Données globales
const  divProfils = document.getElementById("bloc_profils");
const btnJaime = document.getElementById("jaime");
const btnJaimePas = document.getElementById("!jaime");
var profils;
var imagesProfils;
let isAnimating= false;
divProfils.classList.add('card-stack');
const imgDefaut = '/media/images/profiles/default.jpg';



function CalculerAge(unedate){
    let today = new Date();
    let birthDate = new Date(unedate);
    let age = today.getFullYear() - birthDate.getFullYear();
    let monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}

function creerCardProfil(unProfil,imagesProfil){
        // créer un container local pour chaque profil (éviter la réutilisation globale)
        const container = document.createElement("div");
        container.classList.add("col-md-8","position-relative");

        const card = document.createElement("div");
        card.classList.add("card", "w-100", "mb-4", "d-flex", "justify-content-center");

        // Image
        const img = document.createElement("img");
        img.src = imagesProfil === null? imgDefaut : imagesProfil[0];
        img.classList.add("card-img-top", "profile-avatar");
        img.alt = "image profil utilisateur";
        card.appendChild(img);

        // Card body
        const cardBody1 = document.createElement("div");
        cardBody1.classList.add("card-body");

        const nom = document.createElement("h5");
        nom.classList.add("card-title", "fw-semibold");
        nom.textContent = unProfil.user.username + ", " + CalculerAge(unProfil.user.birthday);

        const bio = document.createElement("p");
        bio.classList.add("card-text");
        bio.textContent = unProfil.bio;

        cardBody1.appendChild(nom);
        cardBody1.appendChild(bio);
        card.appendChild(cardBody1);

        const ul = document.createElement("ul");
        ul.classList.add("w-50", "alignement-gauche");

        const items = [
        { icon: "bi-geo-alt", text: `${unProfil.user.country}, ${unProfil.user.city}` },
        { icon: "bi-briefcase", text: unProfil.occupation },
        { icon: "bi-geo-alt", text: "" },
        { icon: "bi-geo-alt", text: "" }
        ];

        items.forEach(item => {
        const wrapper = document.createElement("div");
        wrapper.classList.add("d-flex", "justify-content-around", "mb-2", "mx-2");

        const icon = document.createElement("i");
        icon.classList.add("bi", item.icon);

        const li = document.createElement("li");
        li.classList.add("list-group-item");
        li.textContent = item.text;
        if(item.text == null || item.text === ""){
            icon.classList.add("d-none");
            li.classList.add("d-none");
        }

        wrapper.appendChild(icon);
        wrapper.appendChild(li);
        ul.appendChild(wrapper);
        });

        card.appendChild(ul);

        const likeWrapper = document.createElement("div");
        likeWrapper.classList.add("d-flex", "justify-content-between", "mx-4", "w-75");

        const dislike = document.createElement('button');
        dislike.classList.add("fs-1", "text-dark", "mx-2");
        dislike.id = "!jaime";
        dislike.innerHTML = '<i class="bi bi-x-lg"></i>';

        const like = document.createElement('button');
        like.classList.add("fs-1", "text-primary");
        like.id = "jaime";
        like.innerHTML = '<i class="bi bi-heart-fill"></i>';
        dislike.setAttribute('aria-label', 'dislike');
        like.setAttribute('aria-label', 'like');

        likeWrapper.appendChild(dislike);
        likeWrapper.appendChild(like);
        card.appendChild(likeWrapper);

        // Card links
        const cardBody2 = document.createElement("div");
        cardBody2.classList.add("card-body","d-block");

        for(let i=1;i<imagesProfil.length;i++){
            const blocImages = document.createElement("div");
            blocImages.className = 'bloc-images';
            const img2 = document.createElement("img");
            img2.src = imagesProfil[i];
            img2.classList.add("profile-avatar");
            img2.alt = "image profil utilisateur";
            blocImages.appendChild(img2);
            cardBody2.appendChild(blocImages);
        }
        card.appendChild(cardBody2);

        // badge visuel (Liked / Disliked)
        const badge = document.createElement('div');
        badge.classList.add('swipe-badge');
        badge.style.display = 'none';
        card.appendChild(badge);


        container.appendChild(card);
        container.dataset.userId = unProfil.user.id;
        // entry animation
        container.classList.add('card-enter');
        divProfils.appendChild(container);


        container.offsetHeight;
        container.classList.add('card-in');

        // handlers pour like / dislike
        like.addEventListener('click', () => { showBadge(badge, 'liked'); handleSwipe(container, 'right'); });
        dislike.addEventListener('click', () => { showBadge(badge, 'disliked'); handleSwipe(container, 'left'); });

        // --- Touch support: swipe par glissement pour mobiles---
        let startX = 0;
        let currentX = 0;
        const threshold = 80;

        container.addEventListener('touchstart', (ev) => {
            startX = ev.touches[0].clientX;
            container.style.transition = 'none';
        }, {passive: true});

        container.addEventListener('touchmove', (ev) => {
            if (ev.touches && ev.touches.length > 0) {
                currentX = ev.touches[0].clientX;
                const dx = currentX - startX;
                container.style.transform = `translateX(${dx}px)`;
                if (dx > 20) showBadge(badge, 'liked', Math.min(Math.abs(dx) / 120, 1));
                else if (dx < -20) showBadge(badge, 'disliked', Math.min(Math.abs(dx) / 120, 1));
                else badge.style.display = 'none';
            }
        }, {passive: true});

        container.addEventListener('touchend', () => {
            container.style.transition = '';
            const dx = currentX - startX;
            container.style.transform = '';
            badge.style.display = 'none';
            if (dx > threshold) {
                handleSwipe(container, 'right');
            } else if (dx < -threshold) {
                handleSwipe(container, 'left');
            }
        });

}

async function DefinirDonnees(){
    let response = await RecupereProfils()
    if (!response) {
        console.error("Aucune donnée reçue.");
        return;
    }
    profils = response.profiles;
    if (!Array.isArray(profils)) {
        console.error("Le champ 'profiles' n'est pas un tableau :", profils);
        return;
    }
    imagesProfils = response.Images || [];
    if (profils.length === 0) {
        console.warn("Aucun profil disponible à afficher.");
        return;
    }
    console.log(profils);
}

function afficherProfils(){

    var unProfil = profils.pop();
    var imagesProfil = [];
    for(let img of imagesProfils){
        if(img.user_id === unProfil.user.id){
            imagesProfil.push(img.image);
        }
    }
        // fallback image si aucune image disponible
        if (imagesProfil.length === 0) {
            imagesProfil.push(imgDefaut);
        }
        creerCardProfil(unProfil, imagesProfil);
    }
function showBadge(badge, type, intensity = 1) {
    if (!badge) return;
    badge.style.display = 'block';
    badge.style.opacity = String(Math.min(Math.max(intensity, 0.2), 1));
    badge.textContent = type === 'liked' ? 'Liked' : 'Disliked';
    badge.classList.remove('liked', 'disliked');
    badge.classList.add(type === 'liked' ? 'liked' : 'disliked');
}

async function handleSwipe(container, direction) {
    if (isAnimating) return;
    isAnimating = true;
    const className = direction === 'right' ? 'swipe-right' : 'swipe-left';
    container.classList.add(className);

    var data = await action_like(container,direction);
    gestionInteractions(data);
    // attendre la transition
    const onEnd = (e) => {
        if (e.propertyName && e.propertyName !== 'transform') return;
        container.removeEventListener('transitionend', onEnd);
        container.remove();
        isAnimating = false;
        // afficher le profil suivant
        afficherProfils();
    };
    container.addEventListener('transitionend', onEnd);
}

async function action_like(container,direction){
    try {
        const userId = container.dataset.userId;
        const response = await fetch('/api/action_like/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ user_id: userId, action: direction === 'right' ? 'like' : 'dislike' })
        });
        const data = await response.json();
        console.log('action_like response', data);
        return data;
    } catch (e) {
        console.error('Failed to send like/dislike', e);
    }
}

function creerModalMatch(contenu,match_id){
    const modal = document.createElement('div');
    modal.className = 'modal fade';
    modal.id = 'myModal';
    modal.setAttribute('tabindex', '-1');
    modal.setAttribute('aria-labelledby', 'myModalLabel');
    modal.setAttribute('aria-hidden', 'true');

    modal.innerHTML = `
    <div class="modal-dialog">
        <div class="modal-content">
        <div class="modal-header">
            <h5 class="modal-title" id="myModalLabel">Titre du Modal</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Fermer"></button>
        </div>
        <div class="modal-body">
            ${contenu}
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fermer</button>
            <a href="/compatibilite/${match_id}/" class="btn btn-success">Test de Compatibilité</a>
        </div>
        </div>
    </div>`;

    // let btnModalTest = document.getElementById('btnModalTest');
    // btnModalTest.addEventListener('click', testCompatibilite(match_id));
    document.body.appendChild(modal);

}

function testCompatibilite(match_id){
    fetch(`/api/compatibilite/${match_id}/`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: 'param1=valeur1&param2=valeur2'
    });
}
function gestionInteractions(data){
    if (data.result === 'liked') {
        if (data.mutual) {
            // Afficher un modal ou une notification de "match"
            let contenu = `Félicitations ! ${data.utilisateur} vous aime aussi!, vérifiez si vous êtes compatibles en cliquant sur le bouton ci-dessous.`;
            creerModalMatch(contenu,data.match);
            const myModal = new bootstrap.Modal(document.getElementById('myModal'));
            myModal.show();
        }
    }
}

function testCompatibilite(match_id){
    fetch(`/api/compatibilite/${match_id}/`, {
    method: 'GET',
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: 'param1=valeur1&param2=valeur2'
});

}

async function RecupereProfils(){
    try{
        const response = await fetch('/api/obtenir_profil/');
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        console.log("Profiles retrieved successfully.");
        // attendre la résolution du JSON
        const data = await response.json();
        console.log("Données reçues :", data);
        return data;
    }
    catch(error){
        console.error("Error fetching profiles:", error);
        console.log("Failed to retrieve profiles.");
    }
}

// Toggle filter panel
document.getElementById("btn-filters").addEventListener("click", () => {
    const panel = document.getElementById("filter-panel");
    panel.style.display = panel.style.display === "none" ? "block" : "none";
});

// Apply filters
document.getElementById("apply-filters").addEventListener("click", async () => {

    const gender = document.getElementById("filter-gender").value;
    const country = document.getElementById("filter-country").value;
    const city = document.getElementById("filter-city").value;
    const minAge = document.getElementById("filter-age-min").value;
    const maxAge = document.getElementById("filter-age-max").value;

    // Build query string
    const params = new URLSearchParams();

    if (gender) params.append("gender", gender);
    if (country) params.append("country", country);
    if (city) params.append("city", city);
    if (minAge) params.append("min_age", minAge);
    if (maxAge) params.append("max_age", maxAge);

    const url = `/api/obtenir_profil/?${params.toString()}`;

    console.log("Calling:", url);

    const response = await fetch(url);
    const data = await response.json();

    profils = data.profiles;
    imagesProfils = data.Images;

    divProfils.innerHTML = ""; // Clear old stack
    afficherProfils();         // Show filtered stack
});



function initialisation() {
    console.log("Script loaded successfully.");
    DefinirDonnees().then(afficherProfils);
    supprimerImage();
    // afficherProfils()
    applyFilters();
}

window.addEventListener('DOMContentLoaded', initialisation);
function applyFilters() {
    const filterForm = document.getElementById("filter-panel");
    const applyBtn = document.getElementById("apply-filters");

    if (filterForm) {
        filterForm.addEventListener("submit", function (e) {
            e.preventDefault();

            console.log("Applicage des filtres...");

            const gender = document.getElementById("filter-gender").value;
            const country = document.getElementById("filter-country").value;
            const city = document.getElementById("filter-city").value;
            const minAge = document.getElementById("filter-age-min").value;
            const maxAge = document.getElementById("filter-age-max").value;

            applyFilters({
                gender,
                country,
                city,
                minAge,
                maxAge
            });
        });
    }
}


function supprimerImage() {
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

}

function toggleNotifications() {
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
                            <a href="/discussions/" class="btn btn-sm btn-success mt-1">Voir</a>
                        </div>
                    `;
                });
            }

            popup.style.display = "block";
        })
        .catch(err => console.error("Erreur notifications:", err));
}

document.addEventListener("DOMContentLoaded", () => {

    const filterForm = document.getElementById("filter-panel");
    const applyBtn = document.getElementById("apply-filters");

    if (filterForm) {
        filterForm.addEventListener("submit", function (e) {
            e.preventDefault();

            console.log("Applicage des filtres...");

            const gender = document.getElementById("filter-gender").value;
            const country = document.getElementById("filter-country").value;
            const city = document.getElementById("filter-city").value;
            const minAge = document.getElementById("filter-age-min").value;
            const maxAge = document.getElementById("filter-age-max").value;

            applyFilters({
                gender,
                country,
                city,
                minAge,
                maxAge
            });
        });
    }
});
