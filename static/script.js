function flipCard(card) {
  card.classList.toggle("flipped");
}

document.addEventListener("DOMContentLoaded", () => {
  const fileInput = document.getElementById("pdf-input");
  const fileNamePreview = document.getElementById("file-name-preview");
  const dropzoneText = document.querySelector(".upload-text");

  if (fileInput && fileNamePreview) {
    fileInput.addEventListener("change", (e) => {
      const file = e.target.files[0];
      if (file) {
        fileNamePreview.textContent = `Selected: ${file.name}`;
        fileNamePreview.style.display = "block";
        if (dropzoneText) {
          dropzoneText.textContent = "Replace Selected File";
        }
      } else {
        fileNamePreview.style.display = "none";
        if (dropzoneText) {
          dropzoneText.textContent = "Choose a research paper PDF";
        }
      }
    });

    // Visual drag & drop indicators
    const dropzone = document.querySelector(".dropzone");
    if (dropzone) {
      ['dragenter', 'dragover'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          dropzone.classList.add('dragover');
        }, false);
      });

      ['dragleave', 'drop'].forEach(eventName => {
        dropzone.addEventListener(eventName, (e) => {
          e.preventDefault();
          dropzone.classList.remove('dragover');
        }, false);
      });
    }
  }
});