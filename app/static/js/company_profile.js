document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const submitBtn = document.getElementById('submitBtn');
  
    form.classList.add('fade-in');
  
    form.addEventListener('submit', (e) => {
      const fields = form.querySelectorAll('input[type="text"], input[type="email"], input[type="file"]');
      let valid = true;
  
      fields.forEach(field => {
        if (!field.value.trim()) {
          alert("Please fill out all fields.");
          field.focus();
          valid = false;
          e.preventDefault();
          return false;
        }
      });
  
      const fileInput = form.querySelector('input[type="file"]');
      if (fileInput && fileInput.value) {
        const validTypes = ['.csv', '.xlsx'];
        const fileName = fileInput.value.toLowerCase();
        if (!validTypes.some(type => fileName.endsWith(type))) {
          alert("Please upload a .csv or .xlsx file.");
          e.preventDefault();
          return;
        }
      }
  
      if (valid) {
        submitBtn.disabled = true;
        submitBtn.textContent = "Saving...";
      }
    });
  });
  