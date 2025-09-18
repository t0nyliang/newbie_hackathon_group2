function loadGallery(memberId, containerId) {
    fetch(`/api/${memberId}`)
        .then(response => response.json())
        .then(images => {
            const container = document.getElementById(containerId);
            container.innerHTML = "";

            images.forEach(img => {
                const card = document.createElement("div");
                card.className = "gallery-item";

                const image = document.createElement("img");
                image.src = img.url;
                image.alt = img.caption;

                const caption = document.createElement("p");
                caption.textContent = img.caption;

                card.appendChild(image);
                card.appendChild(caption);
                container.appendChild(card);
            });
        })
        .catch(error => console.error("Error loading gallery:", error));
}
