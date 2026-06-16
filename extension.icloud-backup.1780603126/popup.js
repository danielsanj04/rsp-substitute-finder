const API_BASE_URL = "http://127.0.0.1:8000";
const FALLBACK_API_BASE_URL = "http://127.0.0.1:8011";

const form = document.querySelector("#searchForm");
const input = document.querySelector("#partInput");
const button = document.querySelector("#searchButton");
const message = document.querySelector("#message");
const results = document.querySelector("#results");

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const query = input.value.trim();
  if (!query) {
    showMessage("Enter a part number, manufacturer, or product details first.", "error");
    input.focus();
    return;
  }

  setLoading(true);
  showMessage("Searching approved sources...", "info");
  results.classList.add("hidden");

  try {
    const data = await searchPart(query);
    renderResults(data);
    hideMessage();
  } catch (error) {
    showMessage(
      "Could not reach the local PartMatch API. Make sure the backend is running, then try again.",
      "error"
    );
    console.error(error);
  } finally {
    setLoading(false);
  }
});

async function searchPart(query) {
  const payload = buildSearchPayload(query);

  try {
    return await postSearch(`${API_BASE_URL}/api/v1/search`, payload);
  } catch (primaryError) {
    console.warn("Primary API failed, trying fallback preview server", primaryError);
    return postSearch(`${FALLBACK_API_BASE_URL}/api/v1/search`, payload);
  }
}

async function postSearch(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!response.ok) {
    throw new Error(`Search failed with HTTP ${response.status}`);
  }

  return response.json();
}

function buildSearchPayload(query) {
  const likelyPartNumber = query.split(/\s+/)[0];

  return {
    part_number: likelyPartNumber,
    product_details: query,
  };
}

function renderResults(data) {
  const substitute = data.substitutes?.[0];
  const hasMatch = data.recommendation_status === "matches_found" && substitute;

  results.innerHTML = `
    <div class="badge ${hasMatch ? "success" : "warning"}">
      ${hasMatch ? "● Approved match found" : "● No approved match yet"}
    </div>
    ${renderOriginalPart(data.original_part)}
    ${hasMatch ? renderSubstitute(substitute) : ""}
    ${hasMatch ? renderComparison(data.comparison_table || []) : ""}
    ${renderCustomerResponse(data.customer_ready_response)}
  `;

  results.classList.remove("hidden");
}

function renderOriginalPart(originalPart) {
  const title = [originalPart.manufacturer, originalPart.part_number].filter(Boolean).join(" ");

  return `
    <section class="card">
      <p class="card-title">Original Part</p>
      <p class="part-title">${escapeHtml(title || "Unknown part")}</p>
      <p class="meta">${escapeHtml(originalPart.description || "No description available yet.")}</p>
    </section>
  `;
}

function renderSubstitute(substitute) {
  const title = [substitute.manufacturer, substitute.part_number].filter(Boolean).join(" ");

  return `
    <section class="card">
      <p class="card-title">Best Approved Substitute</p>
      <p class="part-title">${escapeHtml(title)}</p>
      <p class="meta">Vendor: <strong>${escapeHtml(substitute.vendor)}</strong> · ${escapeHtml(substitute.condition)} · ${escapeHtml(substitute.stock_status || "Stock unknown")}</p>
      <div class="match-row">
        <div class="pill">
          <strong>Match</strong>
          <span class="match-percent">${substitute.match_percent}%</span>
        </div>
        <div class="pill">
          <strong>Vendor Check</strong>
          Approved source
        </div>
      </div>
      <a class="link-button" href="${substitute.product_link}" target="_blank" rel="noreferrer">Open vendor link →</a>
    </section>
  `;
}

function renderComparison(rows) {
  if (!rows.length) return "";

  const visibleRows = rows.slice(0, 5).map((row) => {
    const icon = row.match ? "✅" : "⚠️";
    return `
      <div class="spec-row">
        ${icon} <strong>${escapeHtml(row.specification)}</strong>: ${escapeHtml(row.original_value || "—")} → ${escapeHtml(row.substitute_value || "—")}
      </div>
    `;
  }).join("");

  return `
    <section class="card">
      <p class="card-title">Key Spec Comparison</p>
      ${visibleRows}
    </section>
  `;
}

function renderCustomerResponse(response) {
  return `
    <section class="card response">
      <p class="card-title">Customer-ready response</p>
      <p class="meta">${escapeHtml(response || "No customer-ready response generated yet.")}</p>
    </section>
  `;
}

function setLoading(isLoading) {
  button.disabled = isLoading;
  button.textContent = isLoading ? "Searching..." : "Find approved match";
}

function showMessage(text, type) {
  message.textContent = text;
  message.className = `message ${type}`;
}

function hideMessage() {
  message.className = "message hidden";
  message.textContent = "";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}
