document.addEventListener("DOMContentLoaded", function () {
  setupTimer();

  // puzzles
  setupPianoPuzzle();
  setupMemoryPuzzle();
  setupRebusPuzzle();
  setupConnectionsPuzzle();
});

function setupTimer() {
  const timerEl = document.getElementById("timer");
  if (!timerEl) return;

  const started = timerEl.dataset.gameStarted === "yes";
  if (!started) {
    timerEl.textContent = "Time left: --";
    return;
  }

  const serverStartTime = parseFloat(timerEl.dataset.startTime);
  if (!serverStartTime) {
    timerEl.textContent = "Time left: --";
    return;
  }

  const timeLimit = parseInt(timerEl.dataset.limit);

  function updateTimer() {
    const now = Date.now() / 1000; // Convert to seconds
    const elapsed = Math.floor(now - serverStartTime);
    const remaining = Math.max(0, timeLimit - elapsed);

    timerEl.textContent = "Time left: " + formatTime(remaining);
    if (remaining <= 0) {
      window.location.href = "/game_over";
    }
  }

  updateTimer();
  setInterval(updateTimer, 1000);
}

function formatTime(seconds) {
  const s = Math.max(0, seconds);
  const mins = Math.floor(s / 60);
  const secs = s % 60;
  return mins + ":" + (secs < 10 ? "0" + secs : secs);
}


/* ===== Puzzle 1: Piano (keydown only) ===== */
function setupPianoPuzzle() {
  const status = document.getElementById("pianoStatus");
  const form = document.getElementById("pianoForm");
  const unlockBtn = document.getElementById("unlockBtn");
  if (!status || !form) return;

  const seq = ["a", "s", "d"];
  let idx = 0;

  document.addEventListener("keydown", function (ev) {
    const k = ev.key.toLowerCase();
    if (k !== "a" && k !== "s" && k !== "d") return;

    flashKey(k);

    if (k === seq[idx]) {
      idx++;
      status.textContent = "Good… (" + idx + "/" + seq.length + ")";
      if (idx === seq.length) {
        status.textContent = "Unlocked!";
        unlockBtn.style.display = "block";
        unlockBtn.click();
      }
    } else {
      idx = 0;
      status.textContent = "Wrong order. Restart.";
    }
  });
}

function flashKey(letter) {
  const map = { a: "keyA", s: "keyS", d: "keyD" };
  const id = map[letter];
  const rect = document.getElementById(id);
  if (!rect) return;

  rect.setAttribute("fill", "lightgreen");
  setTimeout(() => {
    rect.setAttribute("fill", "white");
  }, 200);
}

/* ===== Puzzle 2: Memory 1..7 ===== */
function setupMemoryPuzzle() {
  const display = document.getElementById("memDisplay");
  const startBtn = document.getElementById("memStart");
  const input = document.getElementById("memInput");
  const submit = document.getElementById("memSubmit");
  const status = document.getElementById("memStatus");
  const form = document.getElementById("memoryForm");
  const completeBtn = document.getElementById("completeBtn");
  if (!display || !startBtn || !input || !submit || !status || !form) return;

  input.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
      e.preventDefault();
    }
  });

  let level = 1;
  let current = "";

  function randDigits(n) {
    let s = "";
    for (let i = 0; i < n; i++) {
      s += Math.floor(Math.random() * 10);
    }
    return s;
  }

  function showLevel() {
    current = randDigits(level);
    display.textContent = current;
    status.textContent = "Memorize " + level + " digit(s).";
    input.value = "";
    const displayTime = Math.max(300, 800 - (level * 50));
    setTimeout(() => {
      display.textContent = "####";
    }, displayTime);
  }

  startBtn.onclick = function () {
    level = 1;
    showLevel();
  };

  submit.onclick = function () {
    const guess = input.value.trim();
    if (guess === current) {
      level++;
      if (level === 8) {
        status.textContent = "Calibration complete: MUSEUM";
        completeBtn.style.display = "block";
        completeBtn.click();
        return;
      }
      status.textContent = "Correct. Next.";
      showLevel();
    } else {
      status.textContent = "Incorrect — restarting.";
      level = 1;
      showLevel();
    }
  };
}

/* ===== Puzzle 3: Rebus (form but handled with fetch) ===== */
function setupRebusPuzzle() {
  const form = document.getElementById("rebusForm");
  if (!form) return;

  form.onsubmit = function () {
    return true;
  };
}

/* ===== Puzzle 4: Connections (images use your PNG names) ===== */
function setupConnectionsPuzzle() {
  const grid = document.getElementById("connGrid");
  const selCount = document.getElementById("selCount");
  const submitBtn = document.getElementById("submitGroup");
  const status = document.getElementById("connStatus");
  const digitsSlot = document.getElementById("digitsSlot");
  const form = document.getElementById("connectionsForm");
  const completeBtn = document.getElementById("completeBtn");
  if (!grid || !selCount || !submitBtn || !status || !digitsSlot || !form) return;

  // groups are based on your filenames/ids
  const groups = [
    { ids: ["coffee", "tea", "soda"], digit: "4" },
    { ids: ["guitar", "piano", "drums"], digit: "5" },
    { ids: ["hat", "shirt", "shoe"], digit: "3" },
    { ids: ["sun", "moon", "star"], digit: "1" },
  ];

  let selected = [];
  let locked = new Set();
  let digits = [];

  function renderDigits() {
    let out = "_ _ _ _";
    if (digits.length > 0) {
      out = digits.join(" ") + " " + "_ ".repeat(4 - digits.length).trim();
    }
    digitsSlot.textContent = out.trim();
  }

  function updateUI() {
    selCount.textContent = selected.length;
    submitBtn.disabled = (selected.length !== 3);
  }

  Array.from(grid.querySelectorAll(".conn-tile")).forEach((tile) => {
    tile.onclick = function () {
      const id = tile.dataset.item;
      if (locked.has(id)) return;

      if (selected.includes(id)) {
        selected = selected.filter(x => x !== id);
        tile.classList.remove("selected");
      } else {
        if (selected.length === 3) return;
        selected.push(id);
        tile.classList.add("selected");
      }
      updateUI();
    };
  });

  submitBtn.onclick = function () {
    if (selected.length !== 3) return;

    let found = null;
    for (let i = 0; i < groups.length; i++) {
      const g = groups[i];
      const a = selected.slice().sort().join(",");
      const b = g.ids.slice().sort().join(",");
      if (a === b) {
        found = g;
        break;
      }
    }

    if (!found) {
      status.textContent = "Not a group.";
      // unselect
      Array.from(grid.querySelectorAll(".conn-tile")).forEach((tile) => {
        tile.classList.remove("selected");
      });
      selected = [];
      updateUI();
      return;
    }

    // lock them
    found.ids.forEach((id) => {
      locked.add(id);
      const tile = grid.querySelector(`.conn-tile[data-item="${id}"]`);
      if (tile) {
        tile.classList.remove("selected");
        tile.classList.add("locked");
      }
    });

    digits.push(found.digit);
    status.textContent = "Correct. Digit: " + found.digit;
    selected = [];
    updateUI();
    renderDigits();

    if (digits.length === 4) {
      status.textContent = "All groups found. Keypad activated.";
      completeBtn.style.display = "block";
      completeBtn.click();
    }
  };

  updateUI();
  renderDigits();
}
