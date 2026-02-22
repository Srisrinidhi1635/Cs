const analyzeBtn = document.getElementById('analyzeBtn');
const output = document.getElementById('chatOutput');
const bookingForm = document.getElementById('bookingForm');

analyzeBtn?.addEventListener('click', async () => {
  const message = document.getElementById('message').value.trim();
  const city = document.getElementById('city').value.trim();
  const latitude = document.getElementById('latitude').value.trim();
  const longitude = document.getElementById('longitude').value.trim();

  if (!message) {
    output.textContent = 'Please describe your issue.';
    return;
  }

  const res = await fetch('/api/chatbot', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message, city, latitude, longitude })
  });

  const data = await res.json();
  if (!data.provider) {
    output.textContent = data.reply;
    bookingForm.classList.add('hidden');
    return;
  }

  output.textContent = `${data.reply}\n\nTechnician Details:\n- Name: ${data.provider.name}\n- Distance: ${data.provider.distance} km\n- Contact: ${data.provider.phone}\n- ETA: ${data.provider.eta} minutes\n- Rating: ${data.provider.rating}`;

  document.getElementById('provider_id').value = data.provider.id;
  document.getElementById('issue').value = message;
  document.getElementById('category').value = data.service;
  document.getElementById('book_city').value = data.location.city;
  document.getElementById('book_latitude').value = data.location.latitude;
  document.getElementById('book_longitude').value = data.location.longitude;
  bookingForm.classList.remove('hidden');
});
