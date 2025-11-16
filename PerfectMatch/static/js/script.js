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
