const apiBase = "/api/assets";

const form = document.getElementById("asset-form");
const submitBtn = document.getElementById("submit-btn");
const cancelBtn = document.getElementById("cancel-btn");
const statusMsg = document.getElementById("status-msg");
const formTitle = document.getElementById("form-title");
const totalLabel = document.getElementById("total-label");
const calcBtn = document.getElementById("calc-btn");
const calcResult = document.getElementById("calc-result");
const rowsBody = document.getElementById("asset-rows");
const emptyState = document.getElementById("empty-state");

const fields = {
    nome: document.getElementById("asset-nome"),
    usuarios: document.getElementById("usuarios"),
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

function setCalculationResult(message, isError = false) {
    calcResult.textContent = message;
    calcResult.classList.toggle("text-rose-600", isError);
    calcResult.classList.toggle("text-emerald-900", !isError);
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

        const usersCell = document.createElement("td");
        usersCell.className = "px-6 py-4";
        usersCell.textContent = asset.usuarios;
        row.appendChild(usersCell);

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
    fields.usuarios.value = asset.usuarios;
    submitBtn.textContent = "Atualizar ativo";
    formTitle.textContent = "Editar ativo";
    setStatus(`Editando ativo #${asset.id}`);
}

function readNumber(value, label) {
    const parsed = Number(value);
    if (!Number.isInteger(parsed) || parsed < 0) {
        throw new Error(`Campo ${label} deve ser inteiro >= 0.`);
    }
    return parsed;
}

async function loadAssets() {
    setStatus("Carregando ativos...");
    try {
        const response = await fetch(apiBase);
        const payload = await response.json();
        currentAssets = payload.data || [];
        renderRows(currentAssets);
        totalLabel.textContent = `Total: ${payload.total || 0}`;
        setCalculationResult("");
        setStatus("");
    } catch (error) {
        setStatus("Falha ao carregar ativos.", true);
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
            usuarios: readNumber(fields.usuarios.value, "usuarios"),
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

calcBtn.addEventListener("click", () => {
    if (!currentAssets.length) {
        setCalculationResult("Nenhum ativo para calcular.", true);
        return;
    }
    const totalUsuarios = currentAssets.reduce((acc, asset) => acc + (asset.usuarios || 0), 0);
    setCalculationResult(`Total de usuarios: ${totalUsuarios}`);
});

loadAssets();
