document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("header");
  if (!header) return;

  // User details provided by Flask
  const user = window.NAV_USER || {};
  const isLoggedIn = user.loggedIn === true;
  const userName = user.name || "User";
  const avatar =
    user.avatar || "https://cdn-icons-png.flaticon.com/512/847/847969.png";

  const escapeHTML = (value) =>
    String(value).replace(/[&<>"']/g, (char) => ({
      "&": "&amp;",
      "<": "&lt;",
      ">": "&gt;",
      '"': "&quot;",
      "'": "&#39;",
    })[char]);

  // Navigation links
  const links = [
    ["Home", "/"],
    ["Finance", "/finance"],
    ["Crypto", "/secondpage#crypto"],
    ["Business", "/secondpage#business"],
    ["Editorial", "/editorial"],
    ["About", "/about"],
  ];

  function createLinks(container) {
    links.forEach(([name, url]) => {
      const li = document.createElement("li");
      const a = document.createElement("a");

      a.textContent = name;
      a.href = url;

      li.appendChild(a);
      container.appendChild(li);
    });
  }

  // Navbar
  const nav = document.createElement("nav");
  nav.className = "navbar";

  nav.innerHTML = `
    <a class="logo-text" href="/">Sloth Newz</a>
    <ul class="nav-links"></ul>
    <div class="nav-right">
      <div class="notif-container">
        <button type="button" class="notif-icon" aria-label="Notifications"
          aria-expanded="false">
          <i class="fa-solid fa-bell"></i>
        </button>
        <div class="notif-dropdown hidden">
          <p class="notif-title">Notifications</p>
          <div class="notif-item">No new notifications</div>
        </div>
      </div>

      <div class="profile-container">
        <button type="button" class="profile-trigger"
          aria-label="Open profile menu" aria-expanded="false">
          <img src="${escapeHTML(avatar)}" alt="Profile" class="profile-icon">
        </button>

        <div class="dropdown-menu hidden">
          ${
            isLoggedIn
              ? `
                <div class="dropdown-item profile-name">
                  ${escapeHTML(userName)}
                </div>
                <hr class="dropdown-divider">
                <a class="dropdown-item" href="/profile">
                  <i class="fas fa-user"></i> My Profile
                </a>
                <a class="dropdown-item" href="/profile">
                  <i class="fas fa-cog"></i> Settings
                </a>
                <hr class="dropdown-divider">
                <button type="button" class="dropdown-item logout-button">
                  <i class="fas fa-sign-out-alt"></i> Sign out
                </button>
              `
              : `
                <a class="dropdown-item" href="/profile">
                  <i class="fas fa-user"></i> Profile
                </a>
                <button type="button" class="dropdown-item google-signin">
                  <i class="fab fa-google"></i> Sign in with Google
                </button>
              `
          }
        </div>
      </div>

      <button type="button" class="hamburger"
        aria-label="Toggle navigation" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  `;

  createLinks(nav.querySelector(".nav-links"));
  header.replaceChildren(nav);

  // Mobile menu
  const mobileMenu = document.createElement("div");
  mobileMenu.className = "mobile-menu";

  const mobileLinks = document.createElement("ul");
  mobileLinks.className = "mobile-nav-links";
  createLinks(mobileLinks);

  const mobileProfile = document.createElement("div");
  mobileProfile.className = "mobile-profile-section";

  mobileProfile.innerHTML = isLoggedIn
    ? `
      <div class="mobile-profile-info">
        <img src="${escapeHTML(avatar)}" alt="Profile" class="profile-icon">
        <div class="mobile-profile-name">${escapeHTML(userName)}</div>
      </div>
      <a class="dropdown-item" href="/profile">My Profile</a>
      <button type="button" class="dropdown-item logout-button">
        Sign out
      </button>
    `
    : `
      <div class="mobile-profile-info">
        <img src="${escapeHTML(avatar)}" alt="Profile" class="profile-icon">
        <div class="mobile-profile-name">Guest</div>
      </div>
      <button type="button" class="dropdown-item google-signin">
        <i class="fab fa-google"></i> Sign in with Google
      </button>
    `;

  mobileMenu.append(mobileLinks, mobileProfile);
  document.body.appendChild(mobileMenu);

  const overlay = document.createElement("div");
  overlay.className = "menu-overlay";
  document.body.appendChild(overlay);

  // Dropdowns
  const bellButton = nav.querySelector(".notif-icon");
  const notifDropdown = nav.querySelector(".notif-dropdown");
  const profileButton = nav.querySelector(".profile-trigger");
  const profileDropdown = nav.querySelector(".dropdown-menu");

  function toggleDropdown(button, dropdown) {
    const open = dropdown.classList.contains("hidden");

    closeDropdowns();
    dropdown.classList.toggle("hidden", !open);
    button.setAttribute("aria-expanded", String(open));
  }

  function closeDropdowns() {
    notifDropdown.classList.add("hidden");
    profileDropdown.classList.add("hidden");
    bellButton.setAttribute("aria-expanded", "false");
    profileButton.setAttribute("aria-expanded", "false");
  }

  bellButton.addEventListener("click", (event) => {
    event.stopPropagation();
    toggleDropdown(bellButton, notifDropdown);
  });

  profileButton.addEventListener("click", (event) => {
    event.stopPropagation();
    toggleDropdown(profileButton, profileDropdown);
  });

  document.addEventListener("click", (event) => {
    if (!nav.contains(event.target)) closeDropdowns();
  });

  // Authentication: Flask handles the actual login and logout
  document.querySelectorAll(".google-signin").forEach((button) => {
    button.addEventListener("click", () => {
      window.location.href = "/auth/login";
    });
  });

  document.querySelectorAll(".logout-button").forEach((button) => {
    button.addEventListener("click", () => {
      window.location.href = "/auth/logout";
    });
  });

  // Mobile menu
  const hamburger = nav.querySelector(".hamburger");

  function closeMobileMenu() {
    mobileMenu.classList.remove("active");
    overlay.classList.remove("active");
    hamburger.classList.remove("active");
    hamburger.setAttribute("aria-expanded", "false");
    document.body.style.overflow = "";
  }

  hamburger.addEventListener("click", () => {
    const open = !mobileMenu.classList.contains("active");

    mobileMenu.classList.toggle("active", open);
    overlay.classList.toggle("active", open);
    hamburger.classList.toggle("active", open);
    hamburger.setAttribute("aria-expanded", String(open));
    document.body.style.overflow = open ? "hidden" : "";
  });

  overlay.addEventListener("click", closeMobileMenu);

  mobileLinks.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMobileMenu);
  });

  // Navbar scroll effect
  window.addEventListener("scroll", () => {
    nav.classList.toggle("scrolled", window.scrollY > 50);
  }, { passive: true });

  // Close mobile menu when returning to desktop
  window.addEventListener("resize", () => {
    if (window.innerWidth > 768) closeMobileMenu();
  });
});