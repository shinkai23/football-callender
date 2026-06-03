const WEEKDAYS = ["日", "月", "火", "水", "木", "金", "土"];

/** @param {Date} date */
export function toDateKey(date) {
  const y = date.getFullYear();
  const m = String(date.getMonth() + 1).padStart(2, "0");
  const d = String(date.getDate()).padStart(2, "0");
  return `${y}-${m}-${d}`;
}

/** @param {string} iso */
export function parseKickoff(iso) {
  return new Date(iso);
}

/**
 * @param {Array<{ kickoff_at: string }>} matches
 * @returns {Map<string, typeof matches>}
 */
export function groupMatchesByDate(matches) {
  const map = new Map();
  for (const match of matches) {
    const key = toDateKey(parseKickoff(match.kickoff_at));
    if (!map.has(key)) {
      map.set(key, []);
    }
    map.get(key).push(match);
  }
  for (const list of map.values()) {
    list.sort(
      (a, b) =>
        parseKickoff(a.kickoff_at).getTime() - parseKickoff(b.kickoff_at).getTime(),
    );
  }
  return map;
}

/**
 * @param {number} year
 * @param {number} month 0-indexed
 */
export function buildMonthGrid(year, month) {
  const first = new Date(year, month, 1);
  const startOffset = first.getDay();
  const daysInMonth = new Date(year, month + 1, 0).getDate();

  const cells = [];
  for (let i = 0; i < startOffset; i++) {
    cells.push(null);
  }
  for (let day = 1; day <= daysInMonth; day++) {
    cells.push(new Date(year, month, day));
  }
  while (cells.length % 7 !== 0) {
    cells.push(null);
  }
  return cells;
}

export function formatMonthLabel(year, month) {
  return `${year}年${month + 1}月`;
}

export { WEEKDAYS };
