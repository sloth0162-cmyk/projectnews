/**
 * SLOTH NEWS NETWORK (SNN)
 * Dynamic News Channel Header & Broadcast Bar System
 */

document.addEventListener("DOMContentLoaded", () => {
  const header = document.querySelector("header");
  if (!header) return;

  // Retrieve user data from context or window
  const user = window.NAV_USER || (window.CURRENT_USER_DATA || {});
  const isLoggedIn = user && user.loggedIn === true;
  const userName = user.name || "Subscriber";
  const avatar = user.avatar || "https://cdn-icons-png.flaticon.com/512/847/847969.png";

  const currentPath = window.location.pathname;
  const currentHash = window.location.hash;

  // Channel Category Links
  const navCategories = [
    { label: "Front Page", url: "/" },
    { label: "Top Stories", url: "/#top-headlines" },
    { label: "Markets & Finance", url: "/finance" },
    { label: "Crypto Desk", url: "/secondpage#crypto" },
    { label: "Business", url: "/secondpage#business" },
    { label: "Tech & AI", url: "/secondpage#tech" },
    { label: "India National", url: "/secondpage#indianmarket" },
    { label: "Editorial & Opinion", url: "/editorial" },
    { label: "Wire Archive", url: "/thirdpage" },
    { label: "About Bureau", url: "/about" },
  ];

  // Format real-time live clock
  function getFormattedLiveTime() {
    const now = new Date();
    const options = {
      weekday: "long",
      year: "numeric",
      month: "short",
      day: "numeric",
    };
    const dateStr = now.toLocaleDateString("en-US", options);
    const timeStr = now.toLocaleTimeString("en-US", {
      hour: "2-digit",
      minute: "2-digit",
      second: "2-digit",
      hour12: false,
    });
    return { dateStr, timeStr };
  }

  const { dateStr, timeStr } = getFormattedLiveTime();

  // Master Header Structure
  header.className = "news-header-master";
  header.innerHTML = `
    <!-- 1. Top Broadcast & Edition Strip -->
    <div class="news-broadcast-strip">
      <div class="broadcast-live-badge">
        <span class="live-dot" aria-hidden="true"></span>
        <span>LIVE NEWSROOM</span>
      </div>

      <div class="broadcast-meta-strip">
        <span id="live-broadcast-clock">
          <i class="fa-regular fa-clock text-slate-400 mr-1"></i>
          <strong>${dateStr}</strong> | <span id="live-ticker-time">${timeStr}</span> IST
        </span>
        <span class="text-slate-600">•</span>
        <span>GLOBAL & INDIA EDITION</span>
        <span class="text-slate-600">•</span>
        <a href="/secondpage#stockmarket" class="hover:text-red-400">
          <i class="fa-solid fa-chart-line text-emerald-400 mr-1"></i>Market Wire
        </a>
        <span class="text-slate-600">•</span>
        <a href="/editorial" class="hover:text-red-400">
          <i class="fa-solid fa-pen-nib text-amber-400 mr-1"></i>Daily Op-Ed
        </a>
      </div>

      <div class="flex items-center gap-3">
        <a href="/about" class="text-xs text-slate-300 hover:text-white transition">
          Ethics & Standards
        </a>
        ${
          !isLoggedIn
            ? `<a href="/auth/login" class="bg-red-600 hover:bg-red-700 text-white px-2.5 py-1 rounded text-xs font-bold uppercase tracking-wider transition">Sign In</a>`
            : `<a href="/profile" class="text-xs text-slate-200 hover:text-white font-medium">My Account</a>`
        }
      </div>
    </div>

    <!-- 2. Authoritative News Masthead -->
    <div class="news-masthead">
      <div class="masthead-left">
        <div class="masthead-weather">
          <i class="fa-solid fa-cloud-sun"></i>
          <div>
            <div class="font-bold text-slate-800 text-xs">26°C New Delhi</div>
            <div class="text-[11px] text-slate-500">Air Quality: Moderate • Markets Open</div>
          </div>
        </div>
      </div>

      <div class="masthead-brand-center">
        <a href="/" class="masthead-logo">
          <h1 class="masthead-title">
            SLOTH <span>NEWS</span>
          </h1>
          <span class="masthead-tagline">
            The Independent 24/7 Global Intelligence & Broadcast Network
          </span>
        </a>
      </div>

      <div class="masthead-right">
        <button type="button" class="btn-listen-brief" id="listenLiveBtn" title="Listen to 60s News Summary">
          <i class="fa-solid fa-headphones"></i>
          <span>Audio Brief</span>
        </button>

        <a href="/#top-headlines" class="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-bold rounded bg-slate-900 text-white hover:bg-red-600 transition">
          <i class="fa-solid fa-bolt text-amber-400"></i> Top Stories
        </a>

        <!-- User Profile Trigger -->
        <div class="user-menu-wrap">
          <button type="button" class="user-avatar-btn" id="userMenuBtn" aria-label="Account menu" aria-expanded="false">
            <img src="${avatar}" alt="User Avatar" class="user-avatar-img">
            <i class="fa-solid fa-chevron-down text-slate-500 text-[10px] pr-1"></i>
          </button>

          <div class="user-dropdown-card" id="userDropdown">
            <div class="dropdown-user-header">
              <div class="dropdown-user-name">${userName}</div>
              <div class="dropdown-user-role">${isLoggedIn ? "Verified Subscriber" : "Guest Reader"}</div>
            </div>
            ${
              isLoggedIn
                ? `
                  <a href="/profile"><i class="fa-solid fa-user text-slate-400"></i> My Profile</a>
                  <a href="/profile#bookmarks"><i class="fa-solid fa-bookmark text-slate-400"></i> Saved Articles</a>
                  <a href="/editorial"><i class="fa-solid fa-pen-fancy text-slate-400"></i> Editorial Desk</a>
                  <a href="/run_pipeline"><i class="fa-solid fa-gears text-slate-400"></i> Newsroom Pipeline</a>
                  <a href="/profile#settings"><i class="fa-solid fa-sliders text-slate-400"></i> Preferences</a>
                  <hr class="my-1 border-slate-200">
                  <a href="/auth/login" class="text-red-600 hover:text-red-700">
                    <i class="fa-solid fa-arrow-right-from-bracket text-red-500"></i> Sign Out
                  </a>
                `
                : `
                  <a href="/profile"><i class="fa-solid fa-user text-slate-400"></i> Reader Profile</a>
                  <a href="/auth/login" class="text-red-600 font-bold">
                    <i class="fa-brands fa-google text-red-500"></i> Sign in with Google
                  </a>
                `
            }
          </div>
        </div>

        <button type="button" class="news-hamburger" id="newsHamburger" aria-label="Open mobile navigation">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>

    <!-- 3. Sticky Channel Navigation Bar -->
    <nav class="news-channel-nav" aria-label="Main News Channels">
      <div class="news-nav-inner">
        <ul class="channel-links" id="channelLinksList"></ul>

        <div class="channel-actions"> 
          <form action="/" method="GET" class="relative hidden md:flex items-center" role="search">
            <input
              type="text"
              name="search"
              placeholder="Search wire & archives..."
              class="w-48 focus:w-64 transition-all duration-300 py-1.5 pl-8 pr-3 text-xs bg-slate-100 border border-slate-200 rounded-full focus:outline-none focus:border-red-500 focus:bg-white text-slate-800"
            />
            <i class="fa-solid fa-magnifying-glass absolute left-2.5 text-slate-400 text-xs"></i>
          </form>
        </div>
      </div>
    </nav>
  `;

  // Populate navigation links
  const channelLinksList = document.getElementById("channelLinksList");
  navCategories.forEach((cat) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = cat.url;
    a.textContent = cat.label;

    // Check active route
    if (
      currentPath === cat.url ||
      (cat.url.includes("#") && currentPath + currentHash === cat.url) ||
      (currentPath === "/" && cat.url === "/")
    ) {
      if (cat.url !== "/" || (currentPath === "/" && !currentHash)) {
        a.classList.add("active");
      }
    }

    li.appendChild(a);
    channelLinksList.appendChild(li);
  });

  // Create Mobile Drawer
  const mobileDrawerOverlay = document.createElement("div");
  mobileDrawerOverlay.className = "mobile-drawer-overlay";
  mobileDrawerOverlay.id = "mobileOverlay";

  const mobileDrawer = document.createElement("div");
  mobileDrawer.className = "mobile-drawer";
  mobileDrawer.id = "mobileDrawer";
  mobileDrawer.innerHTML = `
    <div class="drawer-header">
      <div class="font-extrabold text-lg tracking-tight font-serif text-slate-900">
        SLOTH <span class="text-red-600">NEWS</span>
      </div>
      <button type="button" class="drawer-close-btn" id="drawerCloseBtn" aria-label="Close menu">
        <i class="fa-solid fa-xmark"></i>
      </button>
    </div>

    <div class="p-4 border-b border-slate-100 bg-slate-50">
      <div class="flex items-center gap-3">
        <img src="${avatar}" alt="" class="w-10 h-10 rounded-full border border-slate-300">
        <div>
          <div class="font-bold text-sm text-slate-800">${userName}</div>
          <div class="text-xs text-slate-500">${isLoggedIn ? "Subscriber" : "Guest"}</div>
        </div>
      </div>
    </div>

    <ul class="drawer-links" id="drawerLinksList"></ul>

    <div class="p-4 border-t border-slate-200 mt-auto bg-slate-50">
      <div class="text-xs text-slate-500 text-center mb-2">
        Sloth News Channel • Global Edition
      </div>
      ${
        isLoggedIn
          ? `<a href="/profile" class="block w-full py-2 text-center text-xs font-bold bg-slate-900 text-white rounded">Profile & Bookmarks</a>`
          : `<a href="/auth/login" class="block w-full py-2 text-center text-xs font-bold bg-red-600 text-white rounded">Sign In with Google</a>`
      }
    </div>
  `;

  document.body.appendChild(mobileDrawerOverlay);
  document.body.appendChild(mobileDrawer);

  // Populate Mobile Drawer Links
  const drawerLinksList = mobileDrawer.querySelector("#drawerLinksList");
  navCategories.forEach((cat) => {
    const li = document.createElement("li");
    const a = document.createElement("a");
    a.href = cat.url;
    a.textContent = cat.label;
    li.appendChild(a);
    drawerLinksList.appendChild(li);
  });

  // Setup Mobile Drawer Interaction
  const hamburgerBtn = document.getElementById("newsHamburger");
  const drawerCloseBtn = document.getElementById("drawerCloseBtn");

  function openDrawer() {
    mobileDrawer.classList.add("active");
    mobileDrawerOverlay.classList.add("active");
    document.body.style.overflow = "hidden";
  }

  function closeDrawer() {
    mobileDrawer.classList.remove("active");
    mobileDrawerOverlay.classList.remove("active");
    document.body.style.overflow = "";
  }

  if (hamburgerBtn) hamburgerBtn.addEventListener("click", openDrawer);
  if (drawerCloseBtn) drawerCloseBtn.addEventListener("click", closeDrawer);
  if (mobileDrawerOverlay) mobileDrawerOverlay.addEventListener("click", closeDrawer);

  // Setup User Dropdown
  const userMenuBtn = document.getElementById("userMenuBtn");
  const userDropdown = document.getElementById("userDropdown");

  if (userMenuBtn && userDropdown) {
    userMenuBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      userDropdown.classList.toggle("show");
      userMenuBtn.setAttribute("aria-expanded", userDropdown.classList.contains("show"));
    });

    document.addEventListener("click", (e) => {
      if (!userDropdown.contains(e.target) && !userMenuBtn.contains(e.target)) {
        userDropdown.classList.remove("show");
        userMenuBtn.setAttribute("aria-expanded", "false");
      }
    });
  }

  // Audio briefing audio simulator / alert toast
  const listenLiveBtn = document.getElementById("listenLiveBtn");
  if (listenLiveBtn) {
    listenLiveBtn.addEventListener("click", () => {
      showNewsToast("🎙️ Sloth News Daily 60-Second Audio Briefing loading...");
    });
  }

  // Live real-time clock ticking
  setInterval(() => {
    const clockEl = document.getElementById("live-ticker-time");
    if (clockEl) {
      const now = new Date();
      clockEl.textContent = now.toLocaleTimeString("en-US", {
        hour: "2-digit",
        minute: "2-digit",
        second: "2-digit",
        hour12: false,
      });
    }
  }, 1000);
});

// Helper Toast Notification
function showNewsToast(message) {
  let toast = document.getElementById("newsToast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "newsToast";
    toast.className = "news-toast";
    document.body.appendChild(toast);
  }
  toast.innerHTML = `<i class="fa-solid fa-circle-info text-red-400 mr-2"></i> ${message}`;
  toast.classList.add("show");
  setTimeout(() => {
    toast.classList.remove("show");
  }, 3500);
}
