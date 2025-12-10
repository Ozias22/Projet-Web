`use strict`

document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll('.card-abonnement').forEach(card => {
  card.addEventListener('click', () => {
    // Retirer la classe active de toutes les cartes
    document.querySelectorAll('.card-abonnement').forEach(c => c.classList.remove('active'))

    // Ajouter la classe active à la carte cliquée
    card.classList.add('active')

    // Mettre à jour la valeur du champ caché
    document.getElementById('id_type_abonement').value = card.dataset.value
  })
})
});