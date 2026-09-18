const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
const revealItems = document.querySelectorAll(".reveal");

if (reducedMotion || !("IntersectionObserver" in window)) {
  revealItems.forEach((item) => item.classList.add("is-visible"));
} else {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-visible");
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12 }
  );

  revealItems.forEach((item) => observer.observe(item));
}

const dialog = document.querySelector(".dashboard-dialog");
const openDashboard = document.querySelector("[data-open-dashboard]");
const closeDashboard = document.querySelector("[data-close-dashboard]");

openDashboard?.addEventListener("click", () => dialog?.showModal());
closeDashboard?.addEventListener("click", () => dialog?.close());

dialog?.addEventListener("click", (event) => {
  if (event.target === dialog) dialog.close();
});

const verseToggle = document.querySelector("[data-verse-toggle]");
const verseToast = document.querySelector(".verse-toast");
const switchKicker = document.querySelector("[data-switch-kicker]");
const switchCopy = document.querySelector("[data-switch-copy]");
const spideySense = document.querySelector(".spidey-sense");
const webDrop = document.querySelector(".web-drop");
let keySequence = "";
let toastTimer;
let senseTimer;
let dropTimer;

const toggleVerseMode = () => {
  const scrollPosition = { left: window.scrollX, top: window.scrollY };
  const active = document.body.classList.toggle("verse-mode");
  verseToggle?.setAttribute("aria-pressed", String(active));

  window.requestAnimationFrame(() => window.scrollTo(scrollPosition));

  if (switchKicker && switchCopy) {
    switchKicker.textContent = active ? "Dimension 42" : "Spidey sense?";
    switchCopy.textContent = active
      ? "Tingles detected. Press 4, then 2 — or tap to return."
      : "Feeling a tingle? Press 4, then 2 — or tap.";
  }

  if (spideySense) {
    spideySense.classList.remove("is-firing");
    void spideySense.offsetWidth;
    spideySense.classList.add("is-firing");
    window.clearTimeout(senseTimer);
    senseTimer = window.setTimeout(() => spideySense.classList.remove("is-firing"), 1450);
  }

  if (webDrop) {
    webDrop.classList.remove("is-dropping");
    window.clearTimeout(dropTimer);

    if (active) {
      void webDrop.offsetWidth;
      webDrop.classList.add("is-dropping");
      dropTimer = window.setTimeout(() => webDrop.classList.remove("is-dropping"), 4200);
    }
  }

  if (verseToast) {
    verseToast.textContent = active ? "Earth-42 mode activated" : "Returned to the baseline universe";
    verseToast.classList.add("is-active");
    window.clearTimeout(toastTimer);
    toastTimer = window.setTimeout(() => verseToast.classList.remove("is-active"), 1800);
  }
};

verseToggle?.addEventListener("click", toggleVerseMode);

window.addEventListener("keydown", (event) => {
  if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return;

  keySequence = (keySequence + event.key).slice(-2);
  if (keySequence === "42") {
    toggleVerseMode();
    keySequence = "";
  }
});
