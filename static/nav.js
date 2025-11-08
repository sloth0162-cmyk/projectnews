// Create navbar structure
const header = document.querySelector('header');
const nav = document.createElement('nav');
nav.className = 'navbar';

// Logo
const logo = document.createElement('div');
logo.className = 'logo-text';
logo.textContent = 'FinPulse Daily';

// Navigation links
const navLinks = document.createElement('ul');
navLinks.className = 'nav-links';

const links = [
  { text: 'Home', href: '/dashboard' },
  { text: 'Finance', href: '/finance' },
  { text: 'Crypto', href: 'crypto.html' },
  { text: 'Business', href: 'business.html' },
  { text: 'Editorial', href: '/editorial' },
  { text: 'About', href: 'about.html' }
];

links.forEach(({ text, href }) => {
  const li = document.createElement('li');
  const a = document.createElement('a');
  a.textContent = text;
  a.href = href;
  li.appendChild(a);
  navLinks.appendChild(li);
});

// Right section container
const navRight = document.createElement('div');
navRight.className = 'nav-right';

// Notification bell
const notifContainer = document.createElement('div');
notifContainer.className = 'notif-container';
notifContainer.innerHTML = `
  <i class="fa-solid fa-bell notif-icon"></i>
  <div class="notif-dropdown hidden">
    <p class="notif-title">Notifications</p>
    <div class="notif-item">No new notifications</div>
  </div>
`;

// Profile section
const profileContainer = document.createElement('div');
profileContainer.className = 'profile-container';
profileContainer.innerHTML = `
  <img src="https://cdn-icons-png.flaticon.com/512/847/847969.png" alt="Profile" class="profile-icon">
  <div class="dropdown-menu hidden">
    <div class="dropdown-item"><i class="fas fa-cog"></i> Settings</div>
    <hr class="dropdown-divider">
    <div class="dropdown-item google-signin">Sign in with Google</div>
  </div>
`;

// Hamburger menu
const hamburger = document.createElement('div');
hamburger.className = 'hamburger';
hamburger.innerHTML = '<span></span><span></span><span></span>';

// Assemble navbar
navRight.append(notifContainer, profileContainer, hamburger);
nav.append(logo, navLinks, navRight);
header.appendChild(nav);

// Mobile menu
const mobileMenu = document.createElement('div');
mobileMenu.className = 'mobile-menu';
const mobileNav = document.createElement('ul');
mobileNav.className = 'mobile-nav-links';
links.forEach(({ text, href }) => {
  const li = document.createElement('li');
  const a = document.createElement('a');
  a.textContent = text;
  a.href = href;
  li.appendChild(a);
  mobileNav.appendChild(li);
});

const mobileProfile = document.createElement('div');
mobileProfile.className = 'mobile-profile-section';
mobileProfile.innerHTML = `
  <div class="mobile-profile-info">
    <img src="https://cdn-icons-png.flaticon.com/512/847/847969.png" alt="Profile" class="profile-icon">
    <div class="mobile-profile-name">User Profile</div>
  </div>
  <div class="dropdown-item"><i class="fas fa-cog"></i> Settings</div>
  <hr class="dropdown-divider">
  <div class="dropdown-item google-signin">Sign in with Google</div>
`;

mobileMenu.append(mobileNav, mobileProfile);
document.body.appendChild(mobileMenu);

// Overlay
const overlay = document.createElement('div');
overlay.className = 'menu-overlay';
document.body.appendChild(overlay);

// Elements
const bellIcon = notifContainer.querySelector('.notif-icon');
const notifDropdown = notifContainer.querySelector('.notif-dropdown');
const profileIcon = profileContainer.querySelector('.profile-icon');
const dropdown = profileContainer.querySelector('.dropdown-menu');

// Functions
function toggleMobileMenu() {
  const isActive = mobileMenu.classList.contains('active');
  
  if (isActive) {
    closeMobileMenu();
  } else {
    hamburger.classList.add('active');
    mobileMenu.classList.add('active');
    overlay.classList.add('active');
    document.body.style.overflow = 'hidden';
  }
}

function closeMobileMenu() {
  hamburger.classList.remove('active');
  mobileMenu.classList.remove('active');
  overlay.classList.remove('active');
  document.body.style.overflow = '';
}

function closeDropdowns() {
  notifDropdown.classList.add('hidden');
  dropdown.classList.add('hidden');
}

// Events
hamburger.addEventListener('click', (e) => {
  e.stopPropagation();
  toggleMobileMenu();
});

overlay.addEventListener('click', (e) => {
  e.stopPropagation();
  closeMobileMenu();
});

mobileNav.querySelectorAll('a').forEach(link => {
  link.addEventListener('click', () => {
    closeMobileMenu();
  });
});

profileIcon.addEventListener('click', (e) => {
  e.stopPropagation();
  dropdown.classList.toggle('hidden');
  notifDropdown.classList.add('hidden');
});

bellIcon.addEventListener('click', (e) => {
  e.stopPropagation();
  notifDropdown.classList.toggle('hidden');
  dropdown.classList.add('hidden');
});

document.addEventListener('click', (e) => {
  if (!notifContainer.contains(e.target) && !profileContainer.contains(e.target)) {
    closeDropdowns();
  }
});

// Prevent dropdown clicks from closing
notifDropdown.addEventListener('click', (e) => e.stopPropagation());
dropdown.addEventListener('click', (e) => e.stopPropagation());

// Google Sign-In
document.querySelectorAll('.google-signin').forEach(btn => {
  btn.addEventListener('click', () => {
    window.location.href = '/auth/login';
  });
});

// Scroll effect
let lastScrollY = window.scrollY;
window.addEventListener('scroll', () => {
  if (window.scrollY > 50) {
    nav.classList.add('scrolled');
  } else {
    nav.classList.remove('scrolled');
  }
  lastScrollY = window.scrollY;
});

// Resize handler - close mobile menu when resizing to desktop
let resizeTimer;
window.addEventListener('resize', () => {
  clearTimeout(resizeTimer);
  resizeTimer = setTimeout(() => {
    if (window.innerWidth > 768) {
      closeMobileMenu();
    }
  }, 250);
});