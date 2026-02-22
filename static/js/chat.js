const analyzeBtn = document.getElementById('analyzeBtn');
const output = document.getElementById('chatOutput');
const bookingForm = document.getElementById('bookingForm');

function addBubble(text, role = 'bot') {
  const div = document.createElement('div');
  div.className = `bubble ${role === 'user' ? 'bubble-user' : 'bubble-bot'}`;
  div.textContent = text;
  output.appendChild(div);
  output.scrollTop = output.scrollHeight;
}

analyzeBtn?.addEventListener('click', async () => {
  const message = document.getElementById('message').value.trim();
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
});
