// Links that leave the site open in a new tab.
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("a[href^='http']").forEach((a) => {
    if (a.hostname !== location.hostname) { a.target = "_blank"; a.rel = "noopener"; }
  });
});
