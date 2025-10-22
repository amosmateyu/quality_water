const menuToggle = document.querySelector('.menu-toggle');
const navLinks = document.querySelector('.nav-links');
menuToggle.addEventListener('click', (e) => {
  navLinks.classList.toggle('active');
  e.stopPropagation();
});
document.addEventListener('click', (e) => {
  if (!navLinks.contains(e.target) && !menuToggle.contains(e.target)) {
    navLinks.classList.remove('active');
  }
});
document.querySelectorAll('.input-wrapper input').forEach(input => {
  const wrapper = input.parentElement;
  input.addEventListener('input', () => {
    wrapper.classList.toggle('active', input.value.trim() !== '');
  });
});