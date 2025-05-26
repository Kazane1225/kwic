document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("kwic-form");
  const loading = document.getElementById("loading");

  if (form) {
    form.addEventListener("submit", () => {
      loading.style.display = "flex";
    });
  }

  window.addEventListener("load", () => {
    loading.style.display = "none";
  });
});
