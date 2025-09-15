document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const loadingOverlay = document.querySelector(".loading-overlay");

  form.addEventListener("submit", function (event) {
    loadingOverlay.classList.add("active");

    setTimeout(() => {
      form.submit();
    }, 1000);
  });
});
