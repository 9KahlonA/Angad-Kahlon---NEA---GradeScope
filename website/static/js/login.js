document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form");
  const loadingOverlay = document.querySelector(".loading-overlay");

  form.addEventListener("submit", function (event) {
    // Show loading animation
    loadingOverlay.classList.add("active");

    // Simulate fade-out and fade-in effect
    setTimeout(() => {
      form.submit();
    }, 1000); // Adjust delay as needed
  });
});
