// signup.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("signupForm");
    const inputs = form.querySelectorAll("input");
    const password = form.querySelector("input[name='password']");
    const confirmPassword = form.querySelector("input[name='confirm_password']");
    const submitBtn = form.querySelector("button[type='submit']");
  
    // Fade-in animation
    form.style.opacity = 0;
    form.style.transition = "opacity 1s ease-in-out";
    setTimeout(() => {
      form.style.opacity = 1;
    }, 100);
  
    form.addEventListener("submit", (e) => {
      let hasError = false;
  
      inputs.forEach(input => {
        if (!input.value.trim()) {
          alert(`Please fill in your ${input.name.replace('_', ' ')}.`);
          hasError = true;
        }
      });
  
      if (password.value !== confirmPassword.value) {
        alert("Passwords do not match.");
        hasError = true;
      }
  
      if (hasError) {
        e.preventDefault();
        return;
      }
  
      // Show loading state
      submitBtn.disabled = true;
      submitBtn.textContent = "Signing up...";
    });
  });
  