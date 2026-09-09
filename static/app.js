let activeCat = "All";
let showTop10 = false;

const feedEl = document.getElementById("feed");
const controlsEl = document.getElementById("controls");
const top10Btn = document.getElementById("top10Btn");
const heroGrid = document.getElementById("heroGrid");
const modalBackdrop = document.getElementById("modalBackdrop");
const modalBody = document.getElementById("modalBody");
const modalClose = document.getElementById("modalClose");

controlsEl.querySelectorAll(".chip[data-cat]").forEach(btn => {
  btn.addEventListener("click", () => {
    activeCat = btn.dataset.cat;
    controlsEl.querySelectorAll(".chip[data-cat]").forEach(b => b.classList.remove("active"));
    btn.classList.add("active");
    loadStories();
  });
});

top10Btn.addEventListener("click", () => {
  showTop10 = !showTop10;
  top10Btn.classList.toggle("active", showTop10);
  loadStories();
});

async function loadStories() {
  const params = new URLSearchParams({ category: activeCat, top10: showTop10 });
  const res = await fetch(`/api/stories?${params.toString()}`);
  const stories = await res.json();
  renderFeed(stories);
  renderTicker(stories);
}

function renderTicker(all) {
  const ticker = document.getElementById("tickerText");
  const top = [...all].sort((a, b) => a.rank - b.rank).slice(0, 8);
  ticker.textContent = top.map(s => s.title).join("   \u2605   ");
}

function renderFeed(stories) {
  feedEl.className = "feed" + (showTop10 ? " showrank" : "");

  if (stories.length === 0) {
    feedEl.innerHTML = '<div class="empty">No stories in this category right now.</div>';
    return;
  }

  const today = new Date().toLocaleDateString("en-US", { month: "short", day: "numeric" });

  feedEl.innerHTML = stories.map(s => `
    <article class="story" data-id="${s.id}">
      ${showTop10 ? `<span class="rank">${s.rank}</span>` : ""}
      <div class="meta"><span class="cat ${s.category.toLowerCase()}">${s.category}</span> \u00b7 ${today}</div>
      <h2>${s.title}</h2>
      <p>${s.summary}</p>
      <div class="src">Source: ${s.source}</div>
      <div class="readmore">Read full story →</div>
    </article>
  `).join("");

  feedEl.querySelectorAll(".story").forEach(card => {
    card.addEventListener("click", () => openStory(card.dataset.id));
  });
}

async function openStory(id) {
  const res = await fetch(`/api/story/${id}`);
  if (!res.ok) return;
  const s = await res.json();

  modalBody.innerHTML = `
    <span class="cat ${s.category.toLowerCase()}">${s.category}</span>
    <h2>${s.title}</h2>
    <p>${s.summary}</p>
    <div class="src">Source: ${s.source}</div>
    <a class="readlink" href="${s.url}" target="_blank" rel="noopener">Read full story on ${s.source} ↗</a>
  `;
  modalBackdrop.classList.add("open");
}

function closeModal() {
  modalBackdrop.classList.remove("open");
}
modalClose.addEventListener("click", closeModal);
modalBackdrop.addEventListener("click", e => {
  if (e.target === modalBackdrop) closeModal();
});
document.addEventListener("keydown", e => {
  if (e.key === "Escape") closeModal();
});

heroGrid.querySelectorAll(".hero-story").forEach(card => {
  card.addEventListener("click", () => openStory(card.dataset.id));
});

loadStories();
