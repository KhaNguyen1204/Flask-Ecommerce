function previewProfile(event) {
    const [file] = event.target.files;
    const preview = document.getElementById('profilePreview');
    if (file) {
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
    } else {
        preview.src = '';
        preview.style.display = 'none';
    }
}
