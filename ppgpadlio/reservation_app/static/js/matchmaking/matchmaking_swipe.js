// matchmaking_swipe.js
console.log("JS chargé !");

const cardsContainer = document.getElementById('match-cards');
let cards = Array.from(cardsContainer.getElementsByClassName('card'));
let currentIndex = cards.length - 1;

// Fonction pour récupérer le cookie CSRF (nécessaire pour POST dans Django)
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let c of cookies) {
      c = c.trim();
      if (c.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(c.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

function resetCard(card) {
  card.style.transition = 'transform 0.3s ease';
  card.style.transform = 'translateX(0) rotate(0deg)';
}

// Swipe avec bouton
document.getElementById('btn-like').addEventListener('click', () => {
  handleSwipe('like');
});

document.getElementById('btn-refuse').addEventListener('click', () => {
  handleSwipe('refuse');
});

// Swipe avec souris ou doigt
function setupDragSwipe(cardElement) {
  let startX = 0;
  let currentX = 0;
  let isDragging = false;

  // Desktop
  cardElement.addEventListener('mousedown', (e) => {
    isDragging = true;
    startX = e.pageX;
    cardElement.style.transition = 'none';
  });

  document.addEventListener('mousemove', (e) => {
    if (!isDragging) return;
    currentX = e.pageX;
    let deltaX = currentX - startX;
    cardElement.style.transform = `translateX(${deltaX}px) rotate(${deltaX * 0.1}deg)`;
  });

  document.addEventListener('mouseup', () => {
    if (!isDragging) return;
    isDragging = false;
    let deltaX = currentX - startX;

    if (deltaX > 100) {
      handleSwipe('like');
    } else if (deltaX < -100) {
      handleSwipe('refuse');
    } else {
      resetCard(cardElement);
    }
  });

  // Mobile
  cardElement.addEventListener('touchstart', (e) => {
    isDragging = true;
    startX = e.touches[0].clientX;
    cardElement.style.transition = 'none';
  });

  cardElement.addEventListener('touchmove', (e) => {
    if (!isDragging) return;
    currentX = e.touches[0].clientX;
    let deltaX = currentX - startX;
    cardElement.style.transform = `translateX(${deltaX}px) rotate(${deltaX * 0.1}deg)`;
  });

  cardElement.addEventListener('touchend', () => {
    if (!isDragging) return;
    isDragging = false;
    let deltaX = currentX - startX;

    if (deltaX > 100) {
      handleSwipe('like');
    } else if (deltaX < -100) {
      handleSwipe('refuse');
    } else {
      resetCard(cardElement);
    }
  });
}

function updateCards() {
  cards = Array.from(cardsContainer.getElementsByClassName('card'));
  currentIndex = cards.length - 1;

  if (cards[currentIndex]) {
    setupDragSwipe(cards[currentIndex]);
  }
}

function handleSwipe(direction) {
  if (currentIndex < 0) {
    alert("Plus de cartes !");
    return;
  }

  const card = cards[currentIndex];
  const userId = card.getAttribute('data-user-id');

  // Animation de sortie
  card.style.transition = 'transform 0.5s ease, opacity 0.5s ease';
  card.style.transform = direction === 'like'
    ? 'translateX(500px) rotate(30deg)'
    : 'translateX(-500px) rotate(-30deg)';
  card.style.opacity = '0';

  // Supprimer la carte après animation
  setTimeout(() => {
    card.remove();
    updateCards();
  }, 500);

  // Envoi décision au backend
fetch(`/matchmaking/choix/${userId}/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCookie('csrftoken')
    },
    body: JSON.stringify({
      user_id: userId,
      choix: direction
    })
  }).then(res => res.json())
    .then(data => {
      console.log('Réponse serveur:', data);

      if (data.status === 'match') {
        showMatchPopup(data.message, data.contact);
      } else if (data.status === 'like enregistré') {
        console.log('Like bien enregistré.');
      }
    }).catch(err => console.error('Erreur:', err));
}



function showMatchPopup(message, contact) {
  const popup = document.getElementById('match-popup');
  popup.innerHTML = `
    <img src="https://i.ibb.co/8g8MxPp2/match.png" 
         alt="Match !" 
         style="width: 350px; margin-bottom: 20px; border-radius: 15px;">
    <div style="margin-bottom: 15px; font-size: 1.6rem; font-weight: 700;">${message}</div>
    <div>Email: <a href="mailto:${contact.email}" style="color:#fff; text-decoration: underline;">${contact.email}</a></div>
    <div>Téléphone: <a href="tel:${contact.tel}" style="color:#fff; text-decoration: underline;">${contact.tel}</a></div>
  `;

  document.body.classList.add('show-popup');

  popup.style.opacity = '1';
  popup.style.pointerEvents = 'auto';
  popup.style.transform = 'translate(-50%, -50%) scale(1)';

  setTimeout(() => {
    popup.style.opacity = '0';
    popup.style.pointerEvents = 'none';
    popup.style.transform = 'translate(-50%, -50%) scale(0.8)';
    document.body.classList.remove('show-popup');
  }, 5000);
}




// Initialisation
if (cards.length > 0) {
  setupDragSwipe(cards[currentIndex]);
}
