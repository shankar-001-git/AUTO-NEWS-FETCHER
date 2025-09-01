async function fetchLatest() {
  const btn = document.getElementById("fetchBtn");
  const alertBox = document.getElementById("alertBox");
  btn.disabled = true;
  btn.innerText = "Fetching...";

  try {
    const res = await fetch("/fetch-latest/", {
      method: "POST",
      headers: {
        "X-CSRFToken": window.CSRF_TOKEN,
      },
    });

    const data = await res.json();
    const { status, fetched, created, latest } = data;

    if (status === "ok") {
      showAlert(`Fetched ${fetched} items, created ${created} new.`, "success");
      renderLatest(latest);
    } else {
      showAlert("Unexpected response from server.", "warning");
    }
  } catch (err) {
    console.error(err);
    showAlert("Failed to fetch news. Check console/logs.", "danger");
  } finally {
    btn.disabled = false;
    btn.innerText = "Fetch Latest News";
  }
}

function showAlert(message, type) {
  const alertBox = document.getElementById("alertBox");
  alertBox.className = `alert alert-${type}`;
  alertBox.innerText = message;
  alertBox.classList.remove("d-none");
  setTimeout(() => alertBox.classList.add("d-none"), 4000);
}

function renderLatest(items) {
  const container = document.getElementById("newsList");
  container.innerHTML = "";

  items.forEach((a) => {
    const el = document.createElement("a");
    el.href = a.url;
    el.target = "_blank";
    el.rel = "noopener";
    el.className = "list-group-item list-group-item-action flex-column align-items-start";

    el.innerHTML = `
      <div class="d-flex w-100 justify-content-between">
        <h2 class="news-title h6 mb-1">${escapeHtml(a.title)}</h2>
        <small class="text-nowrap">${formatDate(a.published_at)}</small>
      </div>
      <p class="mb-1 small">${escapeHtml((a.summary || "").slice(0, 180))}</p>
      <small class="small-muted">${escapeHtml(a.source)}</small>
    `;
    container.appendChild(el);
  });
}

function escapeHtml(str) {
  return (str || "").replace(/[&<>"']/g, function(m) {
    return ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]);
  });
}

function formatDate(iso) {
  try {
    const d = new Date(iso);
    return d.toLocaleString();
  } catch {
    return "";
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const btn = document.getElementById("fetchBtn");
  btn.addEventListener("click", fetchLatest);
});
