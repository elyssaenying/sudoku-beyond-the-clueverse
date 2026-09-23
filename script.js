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
const sudokuGrid = document.querySelector(".sudoku-grid");
const puzzleStatus = document.querySelector(".puzzle-status");
const restartPuzzle = document.querySelector("[data-restart-puzzle]");
const puzzleInputs = [];

if (sudokuGrid?.dataset.solution?.length === 81) {
  [...sudokuGrid.children].forEach((cell, index) => {
    if (cell.textContent.trim()) return;

    const input = document.createElement("input");
    input.type = "text";
    input.inputMode = "numeric";
    input.maxLength = 1;
    input.autocomplete = "off";
    input.spellcheck = false;
    input.className = "sudoku-input";
    input.dataset.answer = sudokuGrid.dataset.solution[index];
    input.setAttribute("aria-label", `Sudoku row ${Math.floor(index / 9) + 1}, column ${(index % 9) + 1}`);
    cell.replaceWith(input);
    puzzleInputs.push(input);
  });
}

const clueCodeCells = document.querySelectorAll("[data-clue-code]");
let keySequence = "";
let tappedSequence = "";
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
      ? "Tingles detected. Press 4, then 2, or tap to return."
      : "Feeling a tingle? Press 4, then 2, or tap.";
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

const updatePuzzleProgress = () => {
  const correctCount = puzzleInputs.filter((input) => input.value === input.dataset.answer).length;

  if (correctCount === puzzleInputs.length && puzzleInputs.length > 0) {
    sudokuGrid?.classList.add("is-solved");
    puzzleStatus.textContent = "Solved! Every entry is correct.";
    restartPuzzle.textContent = "Play again";
    return;
  }

  sudokuGrid?.classList.remove("is-solved");
  puzzleStatus.textContent = `${correctCount} of ${puzzleInputs.length} empty cells completed correctly.`;
  restartPuzzle.textContent = "Restart";
};

puzzleInputs.forEach((input, inputIndex) => {
  input.addEventListener("input", () => {
    const digit = input.value.replace(/[^1-9]/g, "").slice(-1);
    input.value = digit;
    input.classList.remove("is-wrong", "is-correct");
    input.setAttribute("aria-invalid", "false");

    if (!digit) {
      updatePuzzleProgress();
      return;
    }

    if (digit !== input.dataset.answer) {
      input.classList.add("is-wrong");
      input.setAttribute("aria-invalid", "true");
      puzzleStatus.textContent = "That number is not correct for this cell. Try again.";
      return;
    }

    input.classList.add("is-correct");
    updatePuzzleProgress();

    const nextEmptyInput = puzzleInputs.slice(inputIndex + 1).find((candidate) => !candidate.value);
    nextEmptyInput?.focus();
  });

  input.addEventListener("keydown", (event) => {
    if ((event.key === "Backspace" || event.key === "Delete") && !input.value) {
      puzzleInputs[inputIndex - 1]?.focus();
    }
  });
});

restartPuzzle?.addEventListener("click", () => {
  puzzleInputs.forEach((input) => {
    input.value = "";
    input.classList.remove("is-wrong", "is-correct");
    input.setAttribute("aria-invalid", "false");
  });
  sudokuGrid?.classList.remove("is-solved");
  puzzleStatus.textContent = "Puzzle restarted. Fill the empty cells to try again.";
  restartPuzzle.textContent = "Restart";
  puzzleInputs[0]?.focus();
});

const enterClueCode = (digit) => {
  tappedSequence = (tappedSequence + digit).slice(-2);
  sudokuGrid?.classList.toggle("is-code-armed", tappedSequence === "4");

  if (tappedSequence === "42") {
    toggleVerseMode();
    tappedSequence = "";
    sudokuGrid?.classList.remove("is-code-armed");
  } else if (tappedSequence !== "4") {
    tappedSequence = "";
  }
};

clueCodeCells.forEach((cell) => {
  cell.addEventListener("click", () => enterClueCode(cell.dataset.clueCode));
  cell.addEventListener("keydown", (event) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      enterClueCode(cell.dataset.clueCode);
    }
  });
});

window.addEventListener("keydown", (event) => {
  if (event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return;

  keySequence = (keySequence + event.key).slice(-2);
  if (keySequence === "42") {
    toggleVerseMode();
    keySequence = "";
  }
});
