document.addEventListener("DOMContentLoaded", async () => {
    try {
      // --- Fetch latest water data from backend ---
      const response = await fetch("/analysis/water");
      const data = await response.json();
  
      const sample = data.sample;
      const check = data.check_results;
      const finalStatus = data.final_status;
  
      // --- Update Water Parameters ---
      const parameters = [
        "ph",
        "hardness",
        "chloramines",
        "sulfate",
        "trihalomethanes",
        "organic_carbon"
      ];
  
      parameters.forEach((param) => {
        const element = document.getElementById(param);
        element.textContent = sample[param].toFixed(2);
        element.style.color = "green";
      });
  
      // --- WHO Risk Analysis ---
      const abnormalText = check.abnormal.length
        ? `${check.abnormal.join(", ")} are out of WHO standards.`
        : "All parameters meet WHO standards.";
      document.getElementById("risk-analysis").textContent = abnormalText;
      document.getElementById("risk-analysis").style.color = "green";
  
      // --- Water Status Display ---
      const statusElement = document.getElementById("water-status");
      const recElement = document.getElementById("recommendations");
  
      if (finalStatus === "Safe") {
        statusElement.textContent = "Water is safe for consumption.";
        recElement.innerHTML = "No recommendations. All parameters are within safe limits.";
      } else {
        statusElement.textContent = "Water is unsafe for consumption.";
        if (check.recommendations.length > 0) {
          recElement.innerHTML =
            "<strong>Recommended Actions:</strong><br>• " +
            check.recommendations.join("<br>• ");
        } else {
          recElement.innerHTML =
            "Please investigate the water source for possible contamination.";
        }
      }
  
      // --- Make all text green regardless of status ---
      statusElement.style.color = "green";
      recElement.style.color = "green";
    } catch (error) {
      console.error("Error loading water data:", error);
      document.getElementById("water-status").textContent = "Failed to load water status.";
      document.getElementById("risk-analysis").textContent = "Could not load water risk analysis.";
      document.getElementById("recommendations").textContent = "Failed to load recommendations.";
  
      // Keep all error messages green
      document.getElementById("water-status").style.color = "green";
      document.getElementById("risk-analysis").style.color = "green";
      document.getElementById("recommendations").style.color = "green";
    }
  });
  