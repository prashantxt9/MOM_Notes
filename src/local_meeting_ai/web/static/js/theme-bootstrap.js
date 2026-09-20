(() => {
  "use strict";

  const storageKey = "meet2notes-ui-theme";
  let preference = "light";
  try {
    const saved = window.localStorage.getItem(storageKey);
    if (saved === "dark") {
      preference = "dark";
    } else {
      preference = "light";
      window.localStorage.setItem(storageKey, "light");
    }
  } catch (_error) {
    // The persistent API preference will be applied once the application loads.
  }
  const resolved = preference;
  document.documentElement.dataset.themePreference = preference;
  document.documentElement.dataset.theme = resolved;
  try {
    if (window.localStorage.getItem("meet2notes-sidebar-collapsed") === "true"
        && window.matchMedia("(min-width: 821px)").matches) {
      document.documentElement.classList.add("sidebar-collapsed");
    }
  } catch (_error) {
    // The sidebar defaults to expanded when browser storage is unavailable.
  }
})();
