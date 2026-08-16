document.addEventListener("DOMContentLoaded", () => {
  // Menu
  const mobileMenuButton = document.getElementById("mobile-menu-button");
  const mobileMenu = document.getElementById("mobile-menu");

  if (mobileMenuButton && mobileMenu) {
    mobileMenuButton.addEventListener("click", () => {
      const isOpen = !mobileMenu.classList.contains("hidden");
      mobileMenu.classList.toggle("hidden");
      mobileMenuButton.setAttribute("aria-expanded", String(!isOpen));
    });
  }

  // Année actuelle
  const currentYear = new Date().getUTCFullYear();
  document.getElementById("currentYear").textContent = currentYear;

  // Historique
  const STORAGE_KEY = "stack-detector-history";
  const historyList = document.getElementById("historyList");
  const clearHistoryBtn = document.getElementById("clearHistoryBtn");
  const form = document.getElementById("stackForm");
  const inputUrl = document.getElementById("url");

  const readHistory = () => {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY) || "[]");
    } catch {
      return [];
    }
  };

  const writeHistory = (items) => {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(items.slice(0, 20)));
  };

  const renderHistory = () => {
    const items = readHistory();

    if (!historyList) return;

    if (!items.length) {
      historyList.innerHTML = "";
      return;
    }

    historyList.innerHTML = items
      .map(
        (url) => `
                <li class="border border-slate-200 rounded-lg overflow-hidden select-none">
                  <a
                    href="/result?url=${encodeURIComponent(url)}"
                    class="block px-3 py-2 text-xs text-slate-600 hover:bg-slate-50 transition-colors truncate"
                    title="${url}"
                  >
                    ${url}
                  </a>
                </li>
              `,
      )
      .join("");
  };

  const addHistoryEntry = (value) => {
    const url = (value || "").trim();
    if (!url) return;

    const items = readHistory().filter((item) => item !== url);
    items.unshift(url);
    writeHistory(items);
    renderHistory();
  };

  if (form && inputUrl) {
    form.addEventListener("submit", () => {
      addHistoryEntry(inputUrl.value);
    });
  }

  if (clearHistoryBtn) {
    clearHistoryBtn.addEventListener("click", () => {
      localStorage.removeItem(STORAGE_KEY);
      renderHistory();
    });
  }

  renderHistory();
});
