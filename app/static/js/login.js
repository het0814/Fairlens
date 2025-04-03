// login.js

document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("loginForm");
    const usernameInput = form.querySelector("input[name='username']");
    const passwordInput = form.querySelector("input[name='password']");
    const submitBtn = form.querySelector("button[type='submit']");
  
    // Add fade-in animation to form
    form.style.opacity = 0;
    form.style.transition = "opacity 1s ease-in-out";
    setTimeout(() => {
      form.style.opacity = 1;
    }, 100);
  
    form.addEventListener("submit", (e) => {
      let hasError = false;
  
      if (!usernameInput.value.trim()) {
        alert("Please enter your username.");
        hasError = true;
      } else if (!passwordInput.value.trim()) {
        alert("Please enter your password.");
        hasError = true;
      }
  
      if (hasError) {
        e.preventDefault();
        return;
      }
  
      // Show loading state
      submitBtn.disabled = true;
      submitBtn.textContent = "Logging in...";
    });
  });
  