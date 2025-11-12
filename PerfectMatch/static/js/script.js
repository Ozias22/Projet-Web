
document.querySelectorAll('.btn-supprimer-image').forEach(button => {
    button.addEventListener('click', function() {
        const imageId = this.dataset.id;
        const csrfToken = '{{ csrf_token }}';
        
        fetch("{% url 'supprimer_image_ajax' %}", {
            method: "POST",
            headers: {
                "X-CSRFToken": csrfToken,
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: `image_id=${imageId}`
        })
        .then(response => response.json())
        .then(data => {
            if(data.success) {
                const imageDiv = document.getElementById(`image-${imageId}`);
                if(imageDiv) imageDiv.remove();
            } else {
                alert("Erreur lors de la suppression de l'image.");
            }
        })
        .catch(() => alert("Erreur lors de la suppression de l'image."));
    });
});