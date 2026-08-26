const token = () => localStorage.getItem("access_token");
const headers = () => ({
  Authorization: `Bearer ${token()}`,
  "Content-Type": "application/json",
});

async function api(path, options = {}) {
  const res = await fetch(path, {
    ...options,
    headers: { ...headers(), ...(options.headers || {}) },
  });
  if (res.status === 401) {
    localStorage.clear();
    window.location.href = "/";
    return;
  }
  return res;
}

document.getElementById("logout-btn").addEventListener("click", () => {
  localStorage.clear();
  window.location.href = "/";
});

const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("file-input");
let filePickerOpen = false;

dropZone.addEventListener("click", (e) => {
  e.preventDefault();
  if (filePickerOpen) return;
  filePickerOpen = true;
  fileInput.click();
  window.setTimeout(() => {
    filePickerOpen = false;
  }, 500);
});
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});
dropZone.addEventListener("dragleave", () => dropZone.classList.remove("dragover"));
dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  if (e.dataTransfer.files.length) uploadFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener("change", () => {
  filePickerOpen = false;
  if (fileInput.files.length) uploadFile(fileInput.files[0]);
  fileInput.value = "";
});

async function uploadFile(file) {
  const msg = document.getElementById("upload-msg");
  msg.textContent = "Uploading...";
  const form = new FormData();
  form.append("file", file);
  const res = await fetch("/api/files/upload/", {
    method: "POST",
    headers: { Authorization: `Bearer ${token()}` },
    body: form,
  });
  const data = await res.json();
  if (!res.ok) {
    msg.textContent = "Upload failed: " + JSON.stringify(data);
    msg.className = "msg error";
    return;
  }
  msg.textContent = `Uploaded: ${data.original_name}`;
  msg.className = "msg success";
  loadFiles();
}

function badgeClass(status) {
  if (status === "clean") return "clean";
  if (status === "quarantined") return "quarantined";
  return "scanning";
}

function statusLabel(status) {
  if (status === "clean") return "ready";
  return status;
}

function escapeHtml(text) {
  const div = document.createElement("div");
  div.textContent = text;
  return div.innerHTML;
}

async function loadFiles() {
  const res = await api("/api/files/");
  if (!res) return;
  const files = await res.json();
  const list = document.getElementById("files-list");
  if (!files.length) {
    list.innerHTML = "<p>No files yet.</p>";
    return;
  }
  list.innerHTML = files
    .map(
      (f) => `
    <div class="file-row" data-id="${f.id}">
      <div>
        <strong>${escapeHtml(f.original_name)}</strong>
        <span class="badge ${badgeClass(f.status)}">${escapeHtml(statusLabel(f.status))}</span>
        <div class="report-box" id="report-${f.id}"></div>
      </div>
      <div class="file-actions">
        ${f.status === "clean" ? `<button type="button" class="btn-download" data-id="${f.id}" data-name="${escapeHtml(f.original_name)}">Download</button>` : ""}
        ${f.status === "clean" ? `<button type="button" class="secondary btn-report" data-id="${f.id}">View Scan Report</button>` : ""}
        <button type="button" class="danger btn-delete" data-id="${f.id}" data-name="${escapeHtml(f.original_name)}">Delete</button>
      </div>
    </div>`
    )
    .join("");
}

document.getElementById("files-list").addEventListener("click", async (e) => {
  const target = e.target;
  if (target.classList.contains("btn-download")) {
    downloadFile(target.dataset.id, target.dataset.name);
  }
  if (target.classList.contains("btn-report")) {
    loadReport(target.dataset.id);
  }
  if (target.classList.contains("btn-delete")) {
    deleteFile(target.dataset.id, target.dataset.name);
  }
});

async function downloadFile(id, name) {
  const res = await fetch(`/api/files/${id}/download/`, {
    headers: { Authorization: `Bearer ${token()}` },
  });
  if (!res.ok) {
    const data = await res.json();
    alert(data.detail || "Download failed");
    return;
  }
  const blob = await res.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = name || "download";
  a.click();
  URL.revokeObjectURL(url);
}

async function loadReport(id) {
  const res = await api(`/api/scanning/report/${id}/`);
  if (!res) return;
  const data = await res.json();
  const el = document.getElementById(`report-${id}`);
  if (el) el.textContent = data.summary;
}

async function deleteFile(id, name) {
  if (!confirm(`Delete "${name}"? This cannot be undone.`)) return;
  const res = await api(`/api/files/${id}/delete/`, { method: "DELETE" });
  if (!res) return;
  if (!res.ok) {
    let detail = "Delete failed";
    try {
      const data = await res.json();
      detail = data.detail || detail;
    } catch (_) {}
    alert(detail);
    return;
  }
  loadFiles();
}

async function init() {
  if (!token()) {
    window.location.href = "/";
    return;
  }
  const meRes = await api("/api/auth/me/");
  if (!meRes) return;
  const me = await meRes.json();
  document.getElementById("user-info").textContent = `Logged in as ${me.email}`;
  loadFiles();
}

init();
