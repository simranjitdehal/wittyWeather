function getWeather() {
  const city = document.getElementById("city").value.trim();
  if (!city) return alert("Please enter a city name!");

  const token = localStorage.getItem("token"); // get JWT

  fetch(`http://127.0.0.1:5000/get_weather?city=${city}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${token}` // send JWT for authentication
    }
  })
    .then(response => {
      if (!response.ok) {
        if (response.status === 401) {
          alert("Unauthorized! Please login again.");
          window.location.href = "login.html";
        }
        throw new Error("HTTP error " + response.status);
      }
      return response.json();
    })
    .then(data => {
      const container = document.getElementById("result");
      container.style.display = "block";
      container.innerHTML = `
        <div class="metric"><strong>City:</strong> ${data.city}</div>
        <div class="metric"><strong>Weather:</strong> ${data.description}</div>
        <div class="metric"><strong>Temperature:</strong> ${data.temperature}°C</div>
        <div class="joke">${data.funny_temperature}</div>
        <div class="metric"><strong>Humidity:</strong> ${data.humidity}%</div>
        <div class="joke">${data.funny_humidity}</div>
        <div class="metric"><strong>Wind Speed:</strong> ${data.wind_speed} km/h</div>
        <div class="joke">${data.funny_wind}</div>
        <div class="metric"><strong>Cloudiness:</strong> ${data.cloudiness}%</div>
        <div class="joke">${data.funny_clouds}</div>
      `;
    })
    .catch(error => {
      console.error("Error:", error);
      alert("Failed to fetch weather data. Make sure your backend is running!");
    });
}
