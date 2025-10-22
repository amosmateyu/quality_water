document.addEventListener("DOMContentLoaded", () => {
  const signupForm = document.getElementById("signupForm");
  const errorMessage = document.getElementById("errorMessage");
  const errorText = document.getElementById("errorText");
  const successMessage = document.getElementById("successMessage");
  const successText = document.getElementById("successText");

  signupForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();

    try {
      const response = await fetch("/auth/signup", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        // ✅ Show success message
        successText.textContent = "Account created successfully!";
        successMessage.style.display = "flex";

        // ✅ Redirect to home after short delay
        setTimeout(() => {
          window.location.href = "/home/";
        }, 1000); // 1.5 seconds delay
      } else {
        errorText.textContent = data.message || "Error occurred.";
        errorMessage.style.display = "flex";
      }
    } catch (err) {
      errorText.textContent = "Server error.";
      errorMessage.style.display = "flex";
    }
  });
});
