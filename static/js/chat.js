const analyzeBtn = document.getElementById('analyzeBtn');
const voiceBtn = document.getElementById('voiceBtn');
const voiceStatus = document.getElementById('voiceStatus');
const messageInput = document.getElementById('message');
const locationBtn = document.getElementById('locationBtn');
const locationStatus = document.getElementById('locationStatus');
const output = document.getElementById('chatOutput');
const bookingForm = document.getElementById('bookingForm');

function addBubble(text, role = 'bot') {
  const div = document.createElement('div');
  div.className = `bubble ${role === 'user' ? 'bubble-user' : 'bubble-bot'}`;
  div.textContent = text;
  output.appendChild(div);
  output.scrollTop = output.scrollHeight;
}

async function analyzeIssue() {
  const message = messageInput.value.trim();
  const city = document.getElementById('city').value.trim();
  const latitude = document.getElementById('latitude').value.trim();
  const longitude = document.getElementById('longitude').value.trim();

  if (!message) {
    addBubble('Please describe your issue.', 'bot');
    return;
  }

  addBubble(message, 'user');

  const res = await fetch('/api/chatbot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, city, latitude, longitude })
  });

  const data = await res.json();
  if (!data.provider) {
    addBubble(data.reply, 'bot');
    bookingForm.classList.add('hidden');
    return;
  }

  addBubble(`${data.reply}\nName: ${data.provider.name}\nDistance: ${data.provider.distance} km\nContact: ${data.provider.phone}\nETA: ${data.provider.eta} mins\nRating: ${data.provider.rating}`, 'bot');

  document.getElementById('provider_id').value = data.provider.id;
  document.getElementById('issue').value = message;
  document.getElementById('category').value = data.service;
  document.getElementById('book_city').value = data.location.city;
  document.getElementById('book_latitude').value = data.location.latitude;
  document.getElementById('book_longitude').value = data.location.longitude;
  bookingForm.classList.remove('hidden');
}

analyzeBtn?.addEventListener('click', analyzeIssue);

const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
if (SpeechRecognition) {
  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  voiceBtn?.addEventListener('click', () => {
    recognition.start();
    voiceStatus.textContent = 'Listening... speak now';
    voiceBtn.disabled = true;
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    messageInput.value = transcript;
    addBubble(`Voice captured: ${transcript}`, 'user');
    voiceStatus.textContent = 'Voice command captured. Click "Detect & Find Technician".';
  };

  recognition.onerror = () => {
    voiceStatus.textContent = 'Voice recognition failed. Please type your issue.';
  };

  recognition.onend = () => {
    voiceBtn.disabled = false;
  };
} else if (voiceStatus) {
  voiceStatus.textContent = 'Voice commands are not supported in this browser.';
  if (voiceBtn) voiceBtn.disabled = true;
}

locationBtn?.addEventListener('click', () => {
  if (!navigator.geolocation) {
    locationStatus.textContent = 'Geolocation not supported. Please enter city manually.';
    return;
  }

  locationStatus.textContent = 'Fetching your current location...';
  locationBtn.disabled = true;

  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      document.getElementById('latitude').value = latitude.toFixed(6);
      document.getElementById('longitude').value = longitude.toFixed(6);
      locationStatus.textContent = `Location captured: ${latitude.toFixed(4)}, ${longitude.toFixed(4)}`;
      locationBtn.disabled = false;
      addBubble('📍 Location captured from GPS. You can now detect nearest technician.', 'bot');
    },
    () => {
      locationStatus.textContent = 'Could not get location. Please allow permission or enter city manually.';
      locationBtn.disabled = false;
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  );
});
