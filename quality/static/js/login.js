
document.addEventListener("DOMContentLoaded", () => {
  const loginForm = document.getElementById("loginForm");
  const errorMessage = document.getElementById("errorMessage");
  const errorText = document.getElementById("errorText");
  const successMessage = document.getElementById("successMessage");
  const successText = document.getElementById("successText");

  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
      const response = await fetch("/auth/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (response.ok) {
        successText.textContent = "Login successful!";
        successMessage.style.display = "flex";
         // ✅ Redirect to home after short delay
 setTimeout(() => {
  window.location.href = "/home/";
}, 1000); // 1.5 seconds delay
      } else {
        errorText.textContent = data.message || "Login failed.";
        errorMessage.style.display = "flex";
      }
    } catch (err) {
      errorText.textContent = "Server error.";
      errorMessage.style.display = "flex";
    }
  });
});

