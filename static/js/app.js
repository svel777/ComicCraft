const form = document.getElementById("comic-form");
const promptBox = document.getElementById("story_prompt");
const count = document.getElementById("char-count");
const loading = document.getElementById("loading");
const bar = document.getElementById("progress-bar");
const loadingTitle = document.getElementById("loading-title");
const loadingText = document.getElementById("loading-text");

if (promptBox) {
  const updateCount = () => count.textContent = `${promptBox.value.length} / 1000`;
  promptBox.addEventListener("input", updateCount);
  updateCount();

  document.querySelectorAll(".chip").forEach(chip => {
    chip.addEventListener("click", () => {
      promptBox.value = chip.dataset.prompt;
      promptBox.dispatchEvent(new Event("input"));
      promptBox.focus();
    });
  });
}

if (form) {
  form.addEventListener("submit", () => {
    loading.hidden = false;
    document.body.classList.add("is-loading");

    const stages = [
      ["Writing your adventure...", "Gemini is turning your idea into a panel-by-panel story.", 18],
      ["Designing the scenes...", "Building visual prompts with consistent characters and composition.", 38],
      ["Painting panel 1...", "Creating the first comic illustration.", 55],
      ["Painting the comic...", "Generating the remaining illustrations.", 76],
      ["Binding the pages...", "Preparing your finished comic and PDF.", 92]
    ];

    let i = 0;
    const timer = setInterval(() => {
      if (i >= stages.length) return clearInterval(timer);
      loadingTitle.textContent = stages[i][0];
      loadingText.textContent = stages[i][1];
      bar.style.width = `${stages[i][2]}%`;
      i++;
    }, 2200);
  });
}

document.querySelectorAll(".comic-panel").forEach(panel => {
  panel.addEventListener("click", () => panel.classList.toggle("expanded"));
});
