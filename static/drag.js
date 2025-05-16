const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-upload');
const form = document.getElementById('kwic-form');

// ✅ ページ全体のデフォルト動作を防止（特にファイルをタブで開く動作）
['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
  window.addEventListener(eventName, e => {
    e.preventDefault();
    e.stopPropagation();
  }, false);
});

dropArea.addEventListener('click', () => fileInput.click());

dropArea.addEventListener('dragover', e => {
  e.preventDefault();
  e.dataTransfer.dropEffect = "copy";
  dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', e => {
  e.preventDefault();
  dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', e => {
  e.preventDefault();
  dropArea.classList.remove('dragover');

  if (e.dataTransfer.files.length > 0) {
    const file = e.dataTransfer.files[0];
    fileInput.files = e.dataTransfer.files;

    const formData = new FormData(form);
    formData.set('file', file);

    fetch("/ajax", {
      method: "POST",
      body: formData
    })
    .then(res => res.json())
    .then(data => {
      const ul = document.querySelector("ul");
      ul.innerHTML = "";
      data.results.forEach(([line, token_after, _]) => {
        const li = document.createElement("li");
        li.innerHTML = `${line} ⟶ NEXT: ${token_after}`;
        ul.appendChild(li);
      });
    })
    .catch(err => console.error("Upload failed", err));
  }
});
