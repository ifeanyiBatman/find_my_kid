// Add video feed update functionality with error handling
function updateVideoFeed() {
  const rawUrl = document.getElementById("camera-url").value;
  const videoFeed = document.getElementById("video-feed");
  const statusMsg = document.getElementById("video-status");

  // Reset status
  statusMsg.classList.add("hidden");

  // Add cache-busting parameter to ensure fresh stream
  const timestamp = new Date().getTime();
  const streamUrl = `${rawUrl}?t=${timestamp}`;
  console.log("Loading video feed from:", streamUrl);

  // Set image source directly
  videoFeed.src = streamUrl;

  // Add error handler
  videoFeed.onerror = function () {
    console.error("Failed to load video feed from URL:", streamUrl);
    statusMsg.classList.remove("hidden");
  };
}

// Update marker position from UI
function updateMarkerPosition() {
  const latInput = document.getElementById("gps-lat").value.replace(/,/g, ".");
  const lngInput = document.getElementById("gps-lng").value.replace(/,/g, ".");
  const lat = parseFloat(latInput);
  const lng = parseFloat(lngInput);

  console.log("Updating marker to:", lat, lng);

  if (!isNaN(lat) && !isNaN(lng)) {
    updateMarkerUI(new L.LatLng(lat, lng));
  } else {
    alert("Please enter valid latitude and longitude numbers");
  }
}

// Update marker position on map
function updateMarkerUI(latLng) {
  marker.setLatLng(latLng);
  map.panTo(latLng);
  marker
    .bindPopup(
      `Ward Location: ${latLng.lat.toFixed(4)}, ${latLng.lng.toFixed(4)}`,
    )
    .openPopup();
}

// Initialize Leaflet map
const map = L.map("map").setView([6.3754, 7.5209], 13);
L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
  attribution:
    '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
}).addTo(map);

// Add marker for ward
const marker = L.marker([6.3754, 7.5209]).addTo(map);
marker.bindPopup("Ward Location").openPopup();

// Connect to WebSocket for GPS updates
const socket = new WebSocket("ws://localhost:8000/ws/gps");

socket.onmessage = function (event) {
  const data = JSON.parse(event.data);
  const newLatLng = new L.LatLng(data.lat, data.lng);
  updateMarkerUI(newLatLng);
};

socket.onerror = function (error) {
  console.error("WebSocket error:", error);
};
