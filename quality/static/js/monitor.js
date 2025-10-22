const form = document.getElementById('predictionForm');

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const formData = {
    ph: parseFloat(document.getElementById('ph').value),
    hardness: parseFloat(document.getElementById('hardness').value),
    chloramines: parseFloat(document.getElementById('chloramines').value),
    sulfate: parseFloat(document.getElementById('sulfate').value),
    organic_carbon: parseFloat(document.getElementById('organic_carbon').value),
    trihalomethanes: parseFloat(document.getElementById('trihalomethanes').value),
  };

  try {
    const response = await fetch('/predict/result', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(formData)
    });

    const data = await response.json();

    if (data.status === "success") {
      window.location.href = "/home/results";  // redirect silently
    } else {
      window.location.href = "/error";  // optional: redirect to error page
    }

  } catch (error) {
    console.error('Error:', error);
    // optional: redirect to error page instead of showing alert
    window.location.href = "/error";
  }
});
