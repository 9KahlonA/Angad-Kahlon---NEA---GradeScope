// Wait for the DOM to fully load before running the script
document.addEventListener("DOMContentLoaded", function () {
  // Select the login form element
  const form = document.querySelector("form");
  // Select the loading overlay element
  const loadingOverlay = document.querySelector(".loading-overlay");

  // Add an event listener for the form's submit event
  form.addEventListener("submit", function (event) {
    // Show the loading overlay when the form is submitted
    loadingOverlay.classList.add("active");

    // Simulate a delay (e.g., for server processing) before submitting the form
    setTimeout(() => {
      form.submit(); // Submit the form after the delay
    }, 1000); // Delay duration in milliseconds
  });
});
