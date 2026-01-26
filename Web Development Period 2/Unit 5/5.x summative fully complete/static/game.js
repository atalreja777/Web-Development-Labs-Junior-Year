document.addEventListener("DOMContentLoaded", function () {
  setupTimer();

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

  const currentPath = window.location.pathname;
  const shouldRedirect = !currentPath.includes('/victory') && !currentPath.includes('/game_over');

  function updateTimer() {
    const now = Date.now() / 1000; // to seconds
    const elapsed = Math.floor(now - serverStartTime);
    const remaining = Math.max(0, timeLimit - elapsed);

    timerEl.textContent = "Time left: "+formatTime(remaining);
    if (remaining <= 0 && shouldRedirect) {
      window.location.href ="/game_over";
    }
  }

  updateTimer();
  setInterval(updateTimer, 1000);
}

function formatTime(seconds) {
  const s =Math.max(0, seconds);
  const mins= Math.floor(s / 60);
  const secs= s % 60;
  return mins+ ":" +(secs < 10 ? "0" + secs : secs);
}

function setupMemoryPuzzle() {
  const display =document.getElementById("mem-display");
  const startBtn= document.getElementById("mem-start");
  const input =document.getElementById("mem-input");
  const submit= document.getElementById("mem-submit");
  const status=document.getElementById("mem-status");
  const form=document.getElementById("memory-form");
  const completeBtn=document.getElementById("complete-btn");
  const finalCodeSection= document.getElementById("final-code-section");
  const codeDisplay =document.getElementById("code-display");
  if (!display || !startBtn || !input || !submit || !status || !form) return;

  input.addEventListener("keydown", function(e) {
    if (e.key === "Enter") {
      e.preventDefault();  // weird bug, enter key was submitting the form
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
    const disT = Math.max(300, 800 - (level * 50));
    setTimeout(() => {
      display.textContent = "####";
    }, disT);
  }

  startBtn.addEventListener("click", function () {
    level = 1;
    showLevel();
  });

  submit.addEventListener("click", function () {
    const guess = input.value.trim();
    if (guess === current) {
      level++;
      if (level === 8) {
        codeDisplay.style.display = "block";
        return;
      }
      status.textContent = "Correct. Next.";
      showLevel();
    } else {
      status.textContent = "Incorrect, you now have to restart as you got it WRONG.";
      level = 1;
      showLevel();
    }
  });

}

function setupRebusPuzzle() {
  const form = document.getElementById("rebusForm");
  if (!form) return;

  form.addEventListener("submit", function () {
    return true;
  });
}

function setupConnectionsPuzzle() {
  const grid = document.getElementById("conn-grid");
  const selCount = document.getElementById("sel-count");
  const submitBtn = document.getElementById("submit-group");
  const status = document.getElementById("conn-status");
  const digitsSlot = document.getElementById("digits-slot");
  const form = document.getElementById("connections-form");
  const completeBtn = document.getElementById("complete-btn");
  if (!grid || !selCount || !submitBtn || !status || !digitsSlot || !form) return;

 
  const groups = [
    { ids: ["coffee", "tea", "soda"], digit: "4", pos: 0 },
    { ids: ["guitar", "piano", "drums"], digit: "5", pos: 1 },
    { ids: ["hat", "shirt", "shoe"], digit: "3", pos: 2 },
    { ids: ["sun", "moon", "star"], digit: "1", pos: 3 },
  ];

  let selected = [];
  let locked = new Set();

  
  let spotsForPassword = ["_", "_", "_", "_"];

  
  function renderDigits() {
    digitsSlot.textContent = spotsForPassword.join(" ");
  }

  function updateUI() {
    selCount.textContent = selected.length;
    submitBtn.disabled = (selected.length !== 3);
  }

  Array.from(grid.querySelectorAll(".conn-tile")).forEach((tile) => {
    tile.addEventListener("click", function () {
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
    });
  });

  submitBtn.addEventListener("click", function () {
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
      Array.from(grid.querySelectorAll(".conn-tile")).forEach((tile) => {
        tile.classList.remove("selected");
      });
      selected = [];
      updateUI();
      return;
    }


    found.ids.forEach((id) => {
      locked.add(id);
      const tile = grid.querySelector(`.conn-tile[data-item="${id}"]`);
      if (tile) {
        tile.classList.remove("selected");
        tile.classList.add("locked");
      }
    });

   
    spotsForPassword[found.pos] = found.digit;

    status.textContent = "Correct. Code: " + spotsForPassword.join("");
    selected = [];
    updateUI();
    renderDigits();

    
    if (!spotsForPassword.includes("_")) {
      status.textContent = "Seems like connections was too easy 4 u. DO U REMEMBER THE CODE IT GAVE YOU THOGUGH?";
      completeBtn.style.display = "block";
    }
  });

  updateUI();
  renderDigits();
}