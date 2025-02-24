document.getElementById('uploadForm').addEventListener('submit', async (event) => {
    event.preventDefault();

    const fileInput = document.getElementById('fileInput');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/convert', {
        method: 'POST',
        body: formData
    });

    const result = await response.json();
    document.getElementById('result').textContent = result.message;
});
