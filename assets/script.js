const palette = [
  '#f7f1f3', // powder rose
  '#eadfe7', // dusty rose
  '#eef5f7', // mist blue
  '#dcebf0', // cloudy blue
  '#f3f1f7', // pale lavender
  '#e8e1ee', // lilac grey
  '#f1f5ef', // soft sage
  '#e3ebdc', // sage green
  '#f7f4ed', // warm ivory
  '#f0e5d6', // apricot cream
  '#edf3f0', // eucalyptus
  '#dce9e4', // soft mint
  '#f7f1ed', // pale clay
  '#f1e0dc', // terracotta blush
  '#eef2f6', // blue grey
  '#dfe6ef', // powder slate
  '#f4f2ee', // stone
  '#eee1cf', // sand
  '#f1f4ed', // olive mist
  '#e7e8d7', // muted olive
  '#f5eff2', // muted mauve
  '#e8dfe7', // orchid grey
  '#edf4f2', // sea glass
  '#dae9e8'  // teal mist
];

const motionPreference = window.matchMedia('(prefers-reduced-motion: reduce)');
let colorIndex = 0;
let colorTimer;

function setColor(index) {
  document.documentElement.style.setProperty('--canvas-color', palette[index]);
}

function configureColorCycle() {
  window.clearInterval(colorTimer);
  if (motionPreference.matches) {
    colorIndex = 0;
    setColor(colorIndex);
    return;
  }
  colorTimer = window.setInterval(() => {
    colorIndex = (colorIndex + 1) % palette.length;
    setColor(colorIndex);
  }, 5000);
}

configureColorCycle();
if (motionPreference.addEventListener) {
  motionPreference.addEventListener('change', configureColorCycle);
} else {
  motionPreference.addListener(configureColorCycle);
}

const menuButton = document.querySelector('.menu-toggle');
const primaryNav = document.querySelector('.primary-nav');

function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', 'Open navigation');
  primaryNav.removeAttribute('data-open');
}

menuButton.addEventListener('click', () => {
  const isOpen = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!isOpen));
  menuButton.setAttribute('aria-label', isOpen ? 'Open navigation' : 'Close navigation');
  if (isOpen) primaryNav.removeAttribute('data-open');
  else primaryNav.setAttribute('data-open', 'true');
});

primaryNav.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape') closeMenu();
});
window.addEventListener('resize', () => {
  if (window.innerWidth > 800) closeMenu();
});
