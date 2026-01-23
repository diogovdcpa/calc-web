const userApi = "/api/user-assets";
const adminApi = "/api/admin-assets";

const form = document.getElementById("user-form");
const submitBtn = document.getElementById("user-submit-btn");
const cancelBtn = document.getElementById("user-cancel-btn");
const statusMsg = document.getElementById("user-status-msg");
const formTitle = document.getElementById("user-form-title");
const totalLabel = document.getElementById("user-total-label");
const adminLabel = document.getElementById("admin-total-label");
const calcBtn = document.getElementById("calc-btn");
const exportBtn = document.getElementById("export-btn");
const calcStatus = document.getElementById("calc-status");
const rowsBody = document.getElementById("user-asset-rows");
const emptyState = document.getElementById("user-empty-state");

const reportRows = document.getElementById("report-rows");
const reportEmpty = document.getElementById("report-empty");
const reportMissing = document.getElementById("report-missing");
const reportTotalBytes = document.getElementById("report-total-bytes");
const reportMb = document.getElementById("report-mb");
const reportGb = document.getElementById("report-gb");
const reportTb = document.getElementById("report-tb");

const fields = {
    nome: document.getElementById("user-asset-nome"),
    usuarios: document.getElementById("user-usuarios"),
};

let editingId = null;
let currentUserAssets = [];
let currentAdminAssets = [];
let lastReport = null;

function setStatus(message, isError = false) {
    statusMsg.textContent = message;
    statusMsg.classList.toggle("text-rose-600", isError);
    statusMsg.classList.toggle("text-emerald-900", !isError);
}

function setCalcStatus(message, isError = false) {
    calcStatus.textContent = message;
    calcStatus.classList.toggle("text-rose-600", isError);
    calcStatus.classList.toggle("text-emerald-900", !isError);
}

function resetForm() {
    form.reset();
    editingId = null;
    submitBtn.textContent = "Salvar ativo";
    formTitle.textContent = "Novo ativo";
    setStatus("");
}

function formatNumber(value, digits = 2) {
    return Number(value).toLocaleString("pt-BR", {
        minimumFractionDigits: digits,
        maximumFractionDigits: digits,
    });
}

function normalizeName(value) {
    return value.trim().toLowerCase();
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
    if (!Number.isFinite(parsed) || parsed < 0) {
        throw new Error(`Campo ${label} deve ser >= 0.`);
    }
    return parsed;
}

function aggregateUserAssets(items) {
    const merged = new Map();
    items.forEach((asset) => {
        const key = normalizeName(asset.nome);
        if (!merged.has(key)) {
            merged.set(key, { nome: asset.nome, usuarios: 0 });
        }
        const entry = merged.get(key);
        entry.usuarios += Number(asset.usuarios) || 0;
    });
    return Array.from(merged.values());
}

function buildPdf(report) {
    const jspdf = window.jspdf;
    if (!jspdf || !jspdf.jsPDF) {
        setCalcStatus("PDF indisponivel. Recarregue a pagina.", true);
        return;
    }

    const doc = new jspdf.jsPDF({ unit: "pt", format: "a4" });
    const left = 40;
    let y = 48;

    doc.setFont("helvetica", "bold");
    doc.setFontSize(16);
    doc.text("Relatorio de consumo mensal", left, y);
    y += 22;

    doc.setFont("helvetica", "normal");
    doc.setFontSize(10);
    doc.text(`Gerado em: ${new Date().toLocaleString("pt-BR")}`, left, y);
    y += 18;

    doc.setFont("helvetica", "bold");
    doc.text("Totais", left, y);
    y += 14;

    doc.setFont("helvetica", "normal");
    doc.text(`Bytes: ${formatNumber(report.totalBytes, 0)}`, left, y);
    y += 14;
    doc.text(`MB: ${formatNumber(report.totalBytes / 1024 ** 2, 2)}`, left, y);
    y += 14;
    doc.text(`GB: ${formatNumber(report.totalBytes / 1024 ** 3, 2)}`, left, y);
    y += 14;
    doc.text(`TB: ${formatNumber(report.totalBytes / 1024 ** 4, 2)}`, left, y);
    y += 20;

    doc.setFont("helvetica", "bold");
    doc.text("Detalhes por ativo", left, y);
    y += 16;

    doc.setFont("helvetica", "normal");
    report.items.forEach((item) => {
        const line = `${item.nome} | Usuarios: ${formatNumber(item.usuarios, 2)} | Evento: ${formatNumber(
            item.consumoEvento,
            2
        )} | Logs/dia: ${formatNumber(item.logsDia, 0)} | Mensal GB: ${formatNumber(
            item.mensalGb,
            2
        )}`;
        doc.text(line, left, y);
        y += 14;
        if (y > 760) {
            doc.addPage();
            y = 48;
        }
    });

    if (report.missing.length) {
        if (y > 720) {
            doc.addPage();
            y = 48;
        }
        y += 6;
        doc.setFont("helvetica", "bold");
        doc.text("Sem match no admin", left, y);
        y += 14;
        doc.setFont("helvetica", "normal");
        doc.text(report.missing.join(", "), left, y);
    }

    doc.save("relatorio-consumo.pdf");
}

function clearReport() {
    reportRows.innerHTML = "";
    reportEmpty.classList.remove("hidden");
    reportMissing.textContent = "";
    reportTotalBytes.textContent = "0";
    reportMb.textContent = "0";
    reportGb.textContent = "0";
    reportTb.textContent = "0";
    lastReport = null;
}

async function loadAssets() {
    setStatus("Carregando ativos...");
    try {
        const [userResponse, adminResponse] = await Promise.all([
            fetch(userApi),
            fetch(adminApi),
        ]);
        const userPayload = await userResponse.json();
        const adminPayload = await adminResponse.json();
        if (!userResponse.ok) {
            throw new Error(userPayload.error || "Falha ao carregar ativos do usuario.");
        }
        if (!adminResponse.ok) {
            throw new Error(adminPayload.error || "Falha ao carregar ativos do admin.");
        }

        currentUserAssets = userPayload.data || [];
        currentAdminAssets = adminPayload.data || [];

        renderRows(currentUserAssets);
        totalLabel.textContent = `Total: ${userPayload.total || 0}`;
        adminLabel.textContent = `Admin: ${adminPayload.total || 0}`;
        setCalcStatus("");
        clearReport();
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
        const response = await fetch(`${userApi}/${assetId}`, { method: "DELETE" });
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
    const url = isEditing ? `${userApi}/${editingId}` : userApi;
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
    if (!currentUserAssets.length) {
        setCalcStatus("Nenhum ativo do usuario para calcular.", true);
        clearReport();
        return;
    }
    if (!currentAdminAssets.length) {
        setCalcStatus("Nenhum ativo do admin cadastrado.", true);
        clearReport();
        return;
    }

    const adminMap = new Map(
        currentAdminAssets.map((asset) => [normalizeName(asset.nome), asset])
    );
    const missingAssets = [];
    const reportItems = [];

    let totalMensalBytes = 0;

    const mergedUsers = aggregateUserAssets(currentUserAssets);

    mergedUsers.forEach((userAsset) => {
        const adminAsset = adminMap.get(normalizeName(userAsset.nome));
        if (!adminAsset) {
            missingAssets.push(userAsset.nome);
            return;
        }

        const consumoEvento =
            Number(adminAsset.eventsize1) +
            Number(adminAsset.eventsize2) +
            Number(adminAsset.eventsize3);
        const logsDia = Number(adminAsset.logs_por_dia);
        const consumoDiarioPorUsuario = consumoEvento * logsDia;
        const consumoMensalPorUsuario = consumoDiarioPorUsuario * 30;
        const mensalBytes = consumoMensalPorUsuario * Number(userAsset.usuarios);

        totalMensalBytes += mensalBytes;

        reportItems.push({
            nome: userAsset.nome,
            usuarios: userAsset.usuarios,
            consumoEvento,
            logsDia,
            mensalGb: mensalBytes / 1024 ** 3,
        });
    });

    reportRows.innerHTML = "";
    if (!reportItems.length) {
        reportEmpty.classList.remove("hidden");
    } else {
        reportEmpty.classList.add("hidden");
    }

    reportItems.forEach((item) => {
        const row = document.createElement("tr");

        const nameCell = document.createElement("td");
        nameCell.className = "px-6 py-4";
        nameCell.textContent = item.nome;
        row.appendChild(nameCell);

        const usersCell = document.createElement("td");
        usersCell.className = "px-6 py-4";
        usersCell.textContent = formatNumber(item.usuarios, 2);
        row.appendChild(usersCell);

        const mediaCell = document.createElement("td");
        mediaCell.className = "px-6 py-4";
        mediaCell.textContent = formatNumber(item.consumoEvento, 2);
        row.appendChild(mediaCell);

        const logsCell = document.createElement("td");
        logsCell.className = "px-6 py-4";
        logsCell.textContent = formatNumber(item.logsDia, 0);
        row.appendChild(logsCell);

        const mensalCell = document.createElement("td");
        mensalCell.className = "px-6 py-4";
        mensalCell.textContent = formatNumber(item.mensalGb, 2);
        row.appendChild(mensalCell);

        reportRows.appendChild(row);
    });

    reportTotalBytes.textContent = formatNumber(totalMensalBytes, 0);
    reportMb.textContent = formatNumber(totalMensalBytes / 1024 ** 2, 2);
    reportGb.textContent = formatNumber(totalMensalBytes / 1024 ** 3, 2);
    reportTb.textContent = formatNumber(totalMensalBytes / 1024 ** 4, 2);

    if (missingAssets.length) {
        reportMissing.textContent = `Sem match no admin: ${missingAssets.join(", ")}.`;
    } else {
        reportMissing.textContent = "";
    }

    setCalcStatus("Calculo atualizado.");
    lastReport = {
        totalBytes: totalMensalBytes,
        items: reportItems,
        missing: missingAssets,
    };
});

loadAssets();

exportBtn.addEventListener("click", () => {
    if (!lastReport || !lastReport.items.length) {
        setCalcStatus("Calcule antes de exportar.", true);
        return;
    }
    buildPdf(lastReport);
});
