document.addEventListener("DOMContentLoaded", () => {
  const resetForm = document.getElementById("forgotPasswordForm");
  const errorMessage = document.getElementById("errorMessage");
  const errorText = document.getElementById("errorText");
  const successMessage = document.getElementById("successMessage");
  const successText = document.getElementById("successText");
  const passwordInput = document.getElementById("new_password");
  const passwordToggle = document.getElementById("passwordToggle");

  // Toggle password visibility
  passwordToggle.addEventListener("click", () => {
    const type = passwordInput.type === "password" ? "text" : "password";
    passwordInput.type = type;
    passwordToggle.innerHTML =
      type === "password"
        ? '<i class="fas fa-eye"></i>'
        : '<i class="fas fa-eye-slash"></i>';
  });

  // Handle password reset form submission
  resetForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const new_password = document.getElementById("new_password").value.trim();

    errorMessage.style.display = "none";
    successMessage.style.display = "none";

    if (!email || !new_password) {
      errorText.textContent = "Please fill in all required fields.";
      errorMessage.style.display = "flex";
      return;
    }

    try {
      const response = await fetch("/auth/forgot-password", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, new_password }),
      });

      const data = await response.json();

      if (response.ok) {
        successText.textContent =
          data.message || "Password reset successful!";
        successMessage.style.display = "flex";

        // Delay redirect so user can see success message
        setTimeout(() => {
          window.location.href = "/auth/"; // login page
        }, 1500);
      } else {
        errorText.textContent = data.message || "Password reset failed.";
        errorMessage.style.display = "flex";
      }
    } catch (error) {
      errorText.textContent = "Server error. Please try again later.";
      errorMessage.style.display = "flex";
    }
  });
});
