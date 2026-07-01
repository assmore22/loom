import { makeReader, write, connectWallet, activeAccount, balanceOf, short, fmtErr }
  from "./shared/genlayer-lite.js";

const CONTRACT = "0x5fcB086587Ac6741Dd0dec5AEeDfcda1460c6Da5";
const { read } = makeReader(CONTRACT);
const $ = (id) => document.getElementById(id);
const esc = (s) => (s || "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

let account = null, strands = [], linesByStrand = {}, selected = null;

const AV = ["#5b53e0", "#e0533f", "#178f7f", "#d99a1c", "#9b51e0", "#2e8b57", "#e0518a", "#3d7de0"];
const avatarColor = (addr) => AV[(parseInt((addr || "0x0").slice(2, 8), 16) || 0) % AV.length];
const initials = (addr) => (addr || "0x").slice(2, 4).toUpperCase();

function toast(msg, kind = "", title = "loom") {
  const el = document.createElement("div"); el.className = "toast " + kind;
  el.innerHTML = `<span class="tt">${title}</span>`; el.appendChild(document.createTextNode(msg));
  $("log").appendChild(el); setTimeout(() => el.remove(), kind === "err" ? 15000 : 5000);
}

/* ---- load ---- */
async function load() {
  const sc = Number(await read("get_strand_count"));
  const lc = Number(await read("get_line_count"));
  const ss = [];
  for (let i = 0; i < sc; i++) ss.push({ id: i, ...(await read("get_strand", [i])) });
  const lns = [];
  for (let i = 0; i < lc; i++) lns.push(await read("get_line", [i]));
  strands = ss;
  linesByStrand = {};
  lns.forEach((l) => { (linesByStrand[l.strand_id] ||= []).push(l); });
  if (selected === null && strands.length) selected = strands[strands.length - 1].id;
  renderSidebar();
  renderThread();
}

/* ---- sidebar ---- */
function renderSidebar() {
  const list = $("strandList");
  if (!strands.length) { list.innerHTML = `<div class="side-empty">No strands yet.<br>Start the first one.</div>`; return; }
  list.innerHTML = strands.slice().reverse().map((s) => {
    const sealed = s.status === 1;
    return `<button class="scard ${s.id === selected ? "on" : ""}" data-s="${s.id}">
      <div class="scard-premise">${esc(s.premise)}</div>
      <div class="scard-meta"><span class="sbadge ${sealed ? "sb-sealed" : "sb-open"}">${sealed ? "Sealed" : "Open"}</span>
        <span><i class="ph-bold ph-needle"></i> ${s.line_count} lines</span><span><i class="ph-bold ph-users"></i> ${s.weaver_count}</span></div>
    </button>`;
  }).join("");
  list.querySelectorAll(".scard").forEach((c) => c.onclick = () => { selected = Number(c.dataset.s); renderSidebar(); renderThread(); });
}

/* ---- thread ---- */
function renderThread() {
  const th = $("thread");
  if (selected === null) { th.innerHTML = `<div class="thread-empty">Select a strand to read it.</div>`; return; }
  const s = strands.find((x) => x.id === selected);
  const lines = linesByStrand[selected] || [];
  const sealed = s.status === 1;
  const winnerIdx = s.won ? s.winner_line : -1;

  const bubbles = lines.map((l) => {
    const crowned = sealed && l.idx === winnerIdx;
    return `<div class="line ${crowned ? "crowned" : ""}">
      <div class="avatar" style="background:${avatarColor(l.author)}">${initials(l.author)}</div>
      <div class="lbubble">${crowned ? `<span class="crown"><i class="ph-fill ph-crown-simple"></i> crowned</span>` : ""}
        <div class="lauthor">${short(l.author)}</div><div class="ltext">${esc(l.text)}</div></div>
    </div>`;
  }).join("");

  const verdict = sealed ? `<div class="verdict"><div class="vh"><i class="ph-fill ph-crown-simple"></i> Validator verdict</div>
    <div class="vt">${esc(s.critique || "The crowned line was chosen as the strongest continuation.")}</div></div>` : "";

  const foot = sealed
    ? `<div class="sealed-foot">This strand is sealed. The validators have crowned their line.</div>`
    : `<div class="composer">
         <textarea id="lineInput" maxlength="280" placeholder="Weave the next line…" rows="1"></textarea>
         <button class="comp-send" id="weaveBtn" title="Weave"><i class="ph-bold ph-arrow-up"></i></button>
       </div><div class="comp-meta" id="lineMeta">Up to 280 characters · anyone can weave</div>`;

  th.innerHTML = `
    <div class="th-head">
      <div class="th-premise">${esc(s.premise)}</div>
      <div class="th-sub"><span class="sbadge ${sealed ? "sb-sealed" : "sb-open"}">${sealed ? "Sealed" : "Open"}</span>
        <span class="dot"></span><span>${s.line_count} lines</span><span class="dot"></span><span>${s.weaver_count} weavers</span>
        <span class="th-actions">${!sealed && lines.length >= 2 ? `<button class="btn outline sm" id="sealBtn"><i class="ph-bold ph-seal-check"></i> Seal & judge</button>` : ""}</span>
      </div>
    </div>
    <div class="stream" id="stream">
      <div class="premise-pill">${esc(s.premise)}</div>
      ${bubbles || `<div class="thread-empty" style="margin:30px auto">No lines yet - weave the first.</div>`}
      ${verdict}
    </div>
    ${foot}`;

  const stream = $("stream"); if (stream) stream.scrollTop = stream.scrollHeight;
  if ($("weaveBtn")) {
    const ta = $("lineInput");
    ta.oninput = () => { ta.style.height = "auto"; ta.style.height = Math.min(ta.scrollHeight, 140) + "px"; $("lineMeta").textContent = `${ta.value.length} / 280 · anyone can weave`; };
    ta.onkeydown = (e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); doWeave(); } };
    $("weaveBtn").onclick = doWeave;
  }
  if ($("sealBtn")) $("sealBtn").onclick = doSeal;
}

/* ---- actions ---- */
async function doWeave() {
  const ta = $("lineInput"); const text = ta.value.trim();
  if (!text) return toast("Write a line first.", "err");
  const btn = $("weaveBtn"); btn.disabled = true; btn.innerHTML = '<span class="spinner"></span>';
  try { await ensureWallet(); await write(CONTRACT, "weave", [selected, text]); ta.value = ""; await load(); }
  catch (e) { toast(fmtErr(e), "err"); btn.disabled = false; btn.innerHTML = '<i class="ph-bold ph-arrow-up"></i>'; }
}
async function doSeal() {
  if (!confirm("Seal this strand? Validators read every line and crown the best one. This is final and calls a real LLM.")) return;
  const btn = $("sealBtn"); btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> validators reading…';
  try { await ensureWallet(); toast("Validators judging the strand…", "", "seal"); await write(CONTRACT, "seal", [selected]); toast("Sealed - a line was crowned.", "ok"); await load(); }
  catch (e) { toast(fmtErr(e), "err"); if (btn) { btn.disabled = false; btn.innerHTML = "Seal & judge"; } }
}
async function doStart() {
  const ta = $("premiseInput"); const premise = ta.value.trim();
  if (!premise) return toast("Set a premise first.", "err");
  const btn = $("startStrand"); btn.disabled = true; btn.innerHTML = '<span class="spinner"></span> starting';
  try { await ensureWallet(); await write(CONTRACT, "start_strand", [premise]); ta.value = ""; $("newComposer").hidden = true; selected = null; await load(); selected = strands.length ? strands[strands.length - 1].id : null; renderSidebar(); renderThread(); toast("Strand started.", "ok"); }
  catch (e) { toast(fmtErr(e), "err"); btn.disabled = false; btn.innerHTML = "Start strand"; }
}

/* ---- new-strand toggle ---- */
$("newToggle").onclick = () => { const c = $("newComposer"); c.hidden = !c.hidden; if (!c.hidden) $("premiseInput").focus(); };
$("premiseInput").addEventListener("input", (e) => { $("premiseCount").textContent = `${e.target.value.length} / 200`; });
$("startStrand").onclick = doStart;

/* ---- wallet ---- */
async function refreshWallet() {
  account = await activeAccount();
  const slot = $("walletslot");
  if (account) { let b = 0n; try { b = await balanceOf(account); } catch (_) {} slot.innerHTML = `<span class="btn ghost" style="cursor:default"><i class="ph-fill ph-circle" style="color:var(--green);font-size:8px"></i> ${short(account)}</span>`; }
  else { slot.innerHTML = `<button class="btn ghost" id="connectBtn"><i class="ph-bold ph-wallet"></i> Connect</button>`; $("connectBtn").onclick = doConnect; }
}
async function doConnect() { try { account = await connectWallet(); toast("Connected on Bradbury.", "ok"); await refreshWallet(); } catch (e) { toast(fmtErr(e), "err"); } }
async function ensureWallet() { if (!account) account = await connectWallet(); await refreshWallet(); }

const _cb = $("connectBtn"); if (_cb) _cb.onclick = doConnect;
if (window.ethereum) window.ethereum.on?.("accountsChanged", refreshWallet);

(async () => {
  await refreshWallet();
  try { await load(); } catch (e) { $("strandList").innerHTML = `<div class="side-empty">Could not reach the chain.<br>${fmtErr(e)}</div>`; }
})();
