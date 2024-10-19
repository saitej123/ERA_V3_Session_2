document.addEventListener('DOMContentLoaded', () => {
    const animalCheckboxes = document.querySelectorAll('input[name="animal"]');
    const animalImage = document.getElementById('animalImage');
    const fileInput = document.getElementById('fileInput');
    const fileInfo = document.getElementById('fileInfo');

    animalCheckboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            animalCheckboxes.forEach(cb => {
                if (cb !== e.target) cb.checked = false;
            });

            const animal = e.target.value;
            if (e.target.checked) {
                animalImage.src = `/images/${animal}.jpg`;
                animalImage.style.display = 'block';
            } else {
                animalImage.style.display = 'none';
            }
        });
    });

    fileInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append('file', file);

            fetch('/upload_file', {
                method: 'POST',
                body: formData
            })
                .then(response => response.json())
                .then(data => {
                    fileInfo.innerHTML = `
                        <p class="text-lg"><span class="font-bold">File Name:</span> ${data.filename}</p>
                        <p class="text-lg"><span class="font-bold">File Size:</span> ${data.file_size} bytes</p>
                        <p class="text-lg"><span class="font-bold">File Type:</span> ${data.file_type}</p>
                    `;
                })
                .catch(error => console.error('Error:', error));
        }
    });
});
