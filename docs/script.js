const observer = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target); // Stops checking — one-time fade
    }
  });
});

window.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('p:not(.no-fade)').forEach(el => {
    observer.observe(el);
  });
});

const header = document.querySelectorAll('li');
let lastScrollY = window.scrollY;

window.addEventListener('scroll', () => {
  const currentScrollY = window.scrollY;

  if (currentScrollY > 0) {
    header.forEach(item => item.classList.add('shrunk'));
  } else {
    header.forEach(item => item.classList.remove('shrunk'));
  }

  lastScrollY = currentScrollY;
  // Image viewer functionality
  document.querySelectorAll('img:not(.unviewable)').forEach(img => {
    img.addEventListener('click', () => {
      const viewer = document.getElementById('image-viewer');
      const viewerImg = document.getElementById('image-viewer-img');
      viewerImg.src = img.src;
      viewer.style.display = 'flex';
    });
  });
});