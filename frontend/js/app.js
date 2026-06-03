import { fetchMatches, fetchTeams } from "./api.js";
import {
  WEEKDAYS,
  buildMonthGrid,
  formatMonthLabel,
  groupMatchesByDate,
  parseKickoff,
  toDateKey,
} from "./calendar.js";

const state = {
  teams: [],
  allMatches: [],
  filteredMatches: [],
  matchesByDate: new Map(),
  selectedTeamId: "",
  viewYear: new Date().getFullYear(),
  viewMonth: new Date().getMonth(),
  selectedDateKey: null,
};

const els = {
  teamFilter: document.getElementById("team-filter"),
  calendarTitle: document.getElementById("calendar-title"),
  calendarGrid: document.getElementById("calendar-grid"),
  prevMonth: document.getElementById("prev-month"),
  nextMonth: document.getElementById("next-month"),
  matchList: document.getElementById("match-list"),
  listHeading: document.getElementById("list-heading"),
  status: document.getElementById("status"),
  modal: document.getElementById("match-modal"),
  modalBody: document.getElementById("modal-body"),
  modalClose: document.getElementById("modal-close"),
};

function setStatus(message, isError = false) {
  els.status.textContent = message;
  els.status.className = isError ? "status status--error" : "status";
}

function applyTeamFilter() {
  const teamId = state.selectedTeamId;
  if (!teamId) {
    state.filteredMatches = [...state.allMatches];
  } else {
    const id = Number(teamId);
    state.filteredMatches = state.allMatches.filter(
      (m) => m.home_team.id === id || m.away_team.id === id,
    );
  }
  state.matchesByDate = groupMatchesByDate(state.filteredMatches);
}

/** 試合がある月をカレンダーの初期表示にする */
function setCalendarToFirstMatchMonth() {
  if (state.filteredMatches.length === 0) {
    return;
  }
  const sorted = [...state.filteredMatches].sort(
    (a, b) =>
      parseKickoff(a.kickoff_at).getTime() - parseKickoff(b.kickoff_at).getTime(),
  );
  const first = parseKickoff(sorted[0].kickoff_at);
  state.viewYear = first.getFullYear();
  state.viewMonth = first.getMonth();
}

function populateTeamFilter() {
  els.teamFilter.innerHTML = '<option value="">すべてのチーム</option>';
  const sorted = [...state.teams].sort((a, b) =>
    a.name.localeCompare(b.name, "ja"),
  );
  for (const team of sorted) {
    const opt = document.createElement("option");
    opt.value = String(team.id);
    opt.textContent = team.name;
    els.teamFilter.appendChild(opt);
  }
}

function renderCalendar() {
  els.calendarTitle.textContent = formatMonthLabel(
    state.viewYear,
    state.viewMonth,
  );
  els.calendarGrid.innerHTML = "";

  for (const label of WEEKDAYS) {
    const head = document.createElement("div");
    head.className = "calendar__weekday";
    head.textContent = label;
    els.calendarGrid.appendChild(head);
  }

  const cells = buildMonthGrid(state.viewYear, state.viewMonth);
  const todayKey = toDateKey(new Date());

  for (const date of cells) {
    const cell = document.createElement("button");
    cell.type = "button";
    cell.className = "calendar__day";
    cell.disabled = !date;

    if (!date) {
      cell.classList.add("calendar__day--empty");
      els.calendarGrid.appendChild(cell);
      continue;
    }

    const key = toDateKey(date);
    const count = state.matchesByDate.get(key)?.length ?? 0;
    const dayNum = date.getDate();

    cell.innerHTML = `<span class="calendar__day-num">${dayNum}</span>`;
    if (count > 0) {
      const badge = document.createElement("span");
      badge.className = "calendar__badge";
      badge.textContent = String(count);
      cell.appendChild(badge);
    }

    if (key === todayKey) {
      cell.classList.add("calendar__day--today");
    }
    if (key === state.selectedDateKey) {
      cell.classList.add("calendar__day--selected");
    }
    if (count === 0) {
      cell.classList.add("calendar__day--no-match");
    }

    cell.addEventListener("click", () => {
      state.selectedDateKey = key;
      renderCalendar();
      renderMatchList();
    });

    els.calendarGrid.appendChild(cell);
  }
}

function formatKickoff(iso) {
  return parseKickoff(iso).toLocaleString("ja-JP", {
    timeZone: "Asia/Tokyo",
    month: "numeric",
    day: "numeric",
    weekday: "short",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function teamLine(team) {
  const crest = team.crest
    ? `<img class="team-crest" src="${team.crest}" alt="" width="24" height="24" />`
    : "";
  const tla = team.tla ? ` (${team.tla})` : "";
  return `${crest}<span>${team.name}${tla}</span>`;
}

function renderMatchList() {
  els.matchList.innerHTML = "";

  let matches = state.filteredMatches;
  if (state.selectedDateKey) {
    matches = state.matchesByDate.get(state.selectedDateKey) ?? [];
    const [y, m, d] = state.selectedDateKey.split("-");
    els.listHeading.textContent = `${y}年${Number(m)}月${Number(d)}日の試合`;
  } else {
    els.listHeading.textContent = "すべての試合";
    matches = [...matches].sort(
      (a, b) =>
        parseKickoff(a.kickoff_at).getTime() -
        parseKickoff(b.kickoff_at).getTime(),
    );
  }

  if (matches.length === 0) {
    const empty = document.createElement("p");
    empty.className = "match-list__empty";
    empty.textContent = state.allMatches.length
      ? "この条件に該当する試合はありません。"
      : "試合データがありません。backend で同期スクリプトを実行してください。";
    els.matchList.appendChild(empty);
    return;
  }

  for (const match of matches) {
    const card = document.createElement("article");
    card.className = "match-card";
    card.innerHTML = `
      <div class="match-card__teams">
        <div class="match-card__team">${teamLine(match.home_team)}</div>
        <span class="match-card__vs">vs</span>
        <div class="match-card__team">${teamLine(match.away_team)}</div>
      </div>
      <p class="match-card__meta">${formatKickoff(match.kickoff_at)}</p>
      <p class="match-card__meta">${match.venue} · ${match.stage}</p>
    `;
    card.addEventListener("click", () => openMatchModal(match));
    els.matchList.appendChild(card);
  }
}

function openMatchModal(match) {
  els.modalBody.innerHTML = `
    <h2 class="modal__title">${match.home_team.name} vs ${match.away_team.name}</h2>
    <dl class="modal__dl">
      <dt>日時</dt><dd>${formatKickoff(match.kickoff_at)}</dd>
      <dt>会場</dt><dd>${match.venue}</dd>
      <dt>ステージ</dt><dd>${match.stage}</dd>
      <dt>ホーム</dt><dd>${match.home_team.name}${match.home_team.tla ? ` (${match.home_team.tla})` : ""}</dd>
      <dt>アウェイ</dt><dd>${match.away_team.name}${match.away_team.tla ? ` (${match.away_team.tla})` : ""}</dd>
    </dl>
  `;
  els.modal.classList.remove("hidden");
  els.modal.setAttribute("aria-hidden", "false");
}

function closeMatchModal() {
  els.modal.classList.add("hidden");
  els.modal.setAttribute("aria-hidden", "true");
}

function wireEvents() {
  els.teamFilter.addEventListener("change", () => {
    state.selectedTeamId = els.teamFilter.value;
    state.selectedDateKey = null;
    applyTeamFilter();
    renderCalendar();
    renderMatchList();
  });

  els.prevMonth.addEventListener("click", () => {
    state.viewMonth -= 1;
    if (state.viewMonth < 0) {
      state.viewMonth = 11;
      state.viewYear -= 1;
    }
    renderCalendar();
  });

  els.nextMonth.addEventListener("click", () => {
    state.viewMonth += 1;
    if (state.viewMonth > 11) {
      state.viewMonth = 0;
      state.viewYear += 1;
    }
    renderCalendar();
  });

  els.modalClose.addEventListener("click", closeMatchModal);
  els.modal.addEventListener("click", (e) => {
    if (e.target === els.modal) {
      closeMatchModal();
    }
  });
}

async function init() {
  setStatus("データを読み込み中…");
  wireEvents();

  try {
    const [teams, matches] = await Promise.all([fetchTeams(), fetchMatches()]);
    state.teams = teams;
    state.allMatches = matches;
    populateTeamFilter();
    applyTeamFilter();
    setCalendarToFirstMatchMonth();
    renderCalendar();
    renderMatchList();
    setStatus(
      matches.length
        ? `${matches.length} 件の試合を表示しています。`
        : "試合が0件です。同期スクリプトを実行してください。",
    );
  } catch (err) {
    console.error(err);
    setStatus(
      `${err.message} — バックエンドが起動しているか確認してください（uvicorn）。`,
      true,
    );
  }
}

init();
