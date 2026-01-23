const apiBase = "/api/admin-assets";

const form = document.getElementById("admin-form");
const submitBtn = document.getElementById("admin-submit-btn");
const cancelBtn = document.getElementById("admin-cancel-btn");
const statusMsg = document.getElementById("admin-status-msg");
const formTitle = document.getElementById("admin-form-title");
const totalLabel = document.getElementById("admin-total-label");
const rowsBody = document.getElementById("admin-asset-rows");
const emptyState = document.getElementById("admin-empty-state");

const fields = {
    nome: document.getElementById("admin-asset-nome"),
    eventsize1: document.getElementById("eventsize1"),
    eventsize2: document.getElementById("eventsize2"),
    eventsize3: document.getElementById("eventsize3"),
    logs_por_dia: document.getElementById("logs-por-dia"),
};

let editingId = null;
let currentAssets = [];

function setStatus(message, isError = false) {
    statusMsg.textContent = message;
    statusMsg.classList.toggle("text-rose-600", isError);
    statusMsg.classList.toggle("text-emerald-900", !isError);
}

function resetForm() {
    form.reset();
    editingId = null;
    submitBtn.textContent = "Salvar ativo";
    formTitle.textContent = "Novo ativo";
    setStatus("");
}

function renderRows(items) {
    rowsBody.innerHTML = "";
    if (!items.length) {
        emptyState.classList.remove("hidden");
        return;
    }
    emptyState.classList.add("hidden");

    items.forEach((asset) => {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.className = "px-6 py-4";
        nameCell.textContent = asset.nome;
        row.appendChild(nameCell);

        const ev1Cell = document.createElement("td");
        ev1Cell.className = "px-6 py-4";
        ev1Cell.textContent = asset.eventsize1;
        row.appendChild(ev1Cell);

        const ev2Cell = document.createElement("td");
        ev2Cell.className = "px-6 py-4";
        ev2Cell.textContent = asset.eventsize2;
        row.appendChild(ev2Cell);

        const ev3Cell = document.createElement("td");
        ev3Cell.className = "px-6 py-4";
        ev3Cell.textContent = asset.eventsize3;
        row.appendChild(ev3Cell);

        const logsCell = document.createElement("td");
        logsCell.className = "px-6 py-4";
        logsCell.textContent = asset.logs_por_dia;
        row.appendChild(logsCell);

        const actionsCell = document.createElement("td");
        actionsCell.className = "px-6 py-4";
        const actionsWrap = document.createElement("div");
        actionsWrap.className = "flex flex-wrap gap-2";

        const editBtn = document.createElement("button");
        editBtn.type = "button";
        editBtn.className = "btn btn-ghost btn-xs text-xs";
        editBtn.textContent = "Editar";
        editBtn.addEventListener("click", () => startEdit(asset));

        const deleteBtn = document.createElement("button");
        deleteBtn.type = "button";
        deleteBtn.className = "btn btn-ghost btn-xs text-xs";
        deleteBtn.textContent = "Excluir";
        deleteBtn.addEventListener("click", () => deleteAsset(asset.id));

        actionsWrap.appendChild(editBtn);
        actionsWrap.appendChild(deleteBtn);
        actionsCell.appendChild(actionsWrap);
        row.appendChild(actionsCell);

        rowsBody.appendChild(row);
    });
}

function startEdit(asset) {
    editingId = asset.id;
    fields.nome.value = asset.nome;
    fields.eventsize1.value = asset.eventsize1;
    fields.eventsize2.value = asset.eventsize2;
    fields.eventsize3.value = asset.eventsize3;
    fields.logs_por_dia.value = asset.logs_por_dia;
    submitBtn.textContent = "Atualizar ativo";
    formTitle.textContent = "Editar ativo";
    setStatus(`Editando ativo #${asset.id}`);
}

function readNumber(value, label) {
    const parsed = Number(value);
    if (!Number.isFinite(parsed) || parsed < 0) {
        throw new Error(`Campo ${label} deve ser >= 0.`);
    }
    return parsed;
}

async function loadAssets() {
    setStatus("Carregando ativos...");
    try {
        const response = await fetch(apiBase);
        const payload = await response.json();
        if (!response.ok) {
            throw new Error(payload.error || "Falha ao carregar ativos.");
        }
        currentAssets = payload.data || [];
        renderRows(currentAssets);
        totalLabel.textContent = `Total: ${payload.total || 0}`;
        setStatus("");
    } catch (error) {
        setStatus(error.message, true);
    }
}

async function deleteAsset(assetId) {
    const confirmDelete = window.confirm("Confirma excluir este ativo?");
    if (!confirmDelete) {
        return;
    }
    try {
        const response = await fetch(`${apiBase}/${assetId}`, { method: "DELETE" });
        const payload = await response.json();
        if (!response.ok) {
            throw new Error(payload.error || "Erro ao excluir.");
        }
        await loadAssets();
        resetForm();
    } catch (error) {
        setStatus(error.message, true);
    }
}

form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const nome = fields.nome.value.trim();
    if (!nome) {
        setStatus("Nome do ativo obrigatorio.", true);
        return;
    }

    let payload;
    try {
        payload = {
            nome,
            eventsize1: readNumber(fields.eventsize1.value, "eventsize1"),
            eventsize2: readNumber(fields.eventsize2.value, "eventsize2"),
            eventsize3: readNumber(fields.eventsize3.value, "eventsize3"),
            logs_por_dia: readNumber(fields.logs_por_dia.value, "logs_por_dia"),
        };
    } catch (error) {
        setStatus(error.message, true);
        return;
    }

    const isEditing = editingId !== null;
    const url = isEditing ? `${apiBase}/${editingId}` : apiBase;
    const method = isEditing ? "PUT" : "POST";

    try {
        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
        });
        const result = await response.json();
        if (!response.ok) {
            throw new Error(result.error || "Erro ao salvar.");
        }
        await loadAssets();
        resetForm();
    } catch (error) {
        setStatus(error.message, true);
    }
});

cancelBtn.addEventListener("click", resetForm);

loadAssets();
