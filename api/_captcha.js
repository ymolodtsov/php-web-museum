// Server-side captcha: renders a distorted 2006-style PNG and signs the answer
// into a stateless token, so the answer never reaches the page.
import crypto from "node:crypto";
import zlib from "node:zlib";

// Look-alikes (B/8, G/6, S/5, Z/2, U/V/Y, O/0, I/1/J, K/H) are left out.
const CHARS = "ACDEFHLMNPRTWX3479";
const TTL_MS = 15 * 60 * 1000;
export const MIN_FILL_MS = 3000;

const GLYPHS = {
  A: [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
  B: ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
  C: [".###.", "#...#", "#....", "#....", "#....", "#...#", ".###."],
  D: ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
  E: ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
  F: ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
  G: [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".####"],
  H: ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
  J: ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
  K: ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
  L: ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
  M: ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
  N: ["#...#", "#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#"],
  P: ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
  Q: [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
  R: ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
  S: [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
  T: ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
  U: ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
  V: ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
  W: ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "#.#.#", ".#.#."],
  X: ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
  Y: ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
  Z: ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
  2: [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
  3: ["#####", "...#.", "..#..", "...#.", "....#", "#...#", ".###."],
  4: ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
  5: ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
  6: ["..##.", ".#...", "#....", "####.", "#...#", "#...#", ".###."],
  7: ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
  8: [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
  9: [".###.", "#...#", "#...#", ".####", "....#", "...#.", ".##.."],
};

function secret() {
  const s = process.env.GUESTBOOK_SECRET;
  if (s) return s;
  if (process.env.VERCEL_ENV) throw new Error("GUESTBOOK_SECRET is not set");
  return "local-dev-secret";
}

function sign(nonce, issued, answer) {
  return crypto.createHmac("sha256", secret()).update(`${nonce}.${issued}.${answer}`).digest("base64url");
}

export function newChallenge() {
  let answer = "";
  for (let i = 0; i < 5; i++) answer += CHARS[crypto.randomInt(CHARS.length)];
  const nonce = crypto.randomBytes(12).toString("base64url");
  const issued = Date.now();
  return { answer, token: `${nonce}.${issued}.${sign(nonce, issued, answer)}` };
}

// Returns the nonce if the answer matches an unexpired, untampered token.
export function verify(token, answer, now = Date.now()) {
  const parts = String(token || "").split(".");
  if (parts.length !== 3) return { ok: false, reason: "bad-token" };
  const [nonce, issuedStr, sig] = parts;
  const issued = Number(issuedStr);
  if (!Number.isFinite(issued) || now - issued > TTL_MS) return { ok: false, reason: "expired" };
  const expected = Buffer.from(sign(nonce, issued, String(answer || "").trim().toUpperCase()));
  const given = Buffer.from(sig);
  if (expected.length !== given.length || !crypto.timingSafeEqual(expected, given)) return { ok: false, reason: "wrong" };
  if (now - issued < MIN_FILL_MS) return { ok: false, reason: "too-fast" };
  return { ok: true, nonce };
}

// --- PNG rendering -----------------------------------------------------------

const W = 150, H = 44;
const rnd = (a, b) => a + Math.random() * (b - a);

const CRC_TABLE = Array.from({ length: 256 }, (_, n) => {
  let c = n;
  for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
  return c >>> 0;
});
function crc32(buf) {
  let c = 0xffffffff;
  for (const b of buf) c = CRC_TABLE[(c ^ b) & 0xff] ^ (c >>> 8);
  return (c ^ 0xffffffff) >>> 0;
}
function chunk(type, data) {
  const len = Buffer.alloc(4);
  len.writeUInt32BE(data.length);
  const td = Buffer.concat([Buffer.from(type, "ascii"), data]);
  const crc = Buffer.alloc(4);
  crc.writeUInt32BE(crc32(td));
  return Buffer.concat([len, td, crc]);
}

export function renderPng(answer) {
  const px = Buffer.alloc(W * H * 3);
  const set = (x, y, [r, g, b]) => {
    if (x < 0 || y < 0 || x >= W || y >= H) return;
    const i = (y * W + x) * 3;
    px[i] = r; px[i + 1] = g; px[i + 2] = b;
  };
  // gradient background + speckle
  for (let y = 0; y < H; y++)
    for (let x = 0; x < W; x++) {
      const t = (x / W + y / H) / 2;
      set(x, y, [228 - 27 * t, 232 - 23 * t, 238 - 18 * t].map(Math.round));
    }
  for (let n = 0; n < 160; n++) set(Math.floor(rnd(0, W)), Math.floor(rnd(0, H)), [35 + rnd(0, 60), 70 + rnd(0, 40), 108 + rnd(0, 40)].map(Math.round));

  const faint = [[120, 146, 176], [140, 128, 110], [128, 140, 160]];
  const curve = (ink) => {
    const y0 = rnd(10, H - 10), a = rnd(3, 7), f = rnd(0.02, 0.045), p = rnd(0, 6);
    for (let x = 0; x < W; x++) set(x, Math.round(y0 + a * Math.sin(x * f + p)), ink);
  };
  curve(faint[0]);
  curve(faint[1]);

  const inks = [[35, 70, 108], [49, 90, 137], [74, 58, 40], [47, 47, 47]];
  const phase = rnd(0, Math.PI * 2), amp = rnd(0.8, 1.8), freq = rnd(0.06, 0.1);
  [...answer].forEach((ch, i) => {
    const glyph = GLYPHS[ch];
    const ink = inks[i % inks.length];
    const cx = 17 + i * 29 + rnd(-1.5, 1.5), cy = H / 2 + rnd(-1.5, 1.5);
    const s = rnd(4.4, 4.8), th = rnd(-0.17, 0.17), sh = rnd(-0.12, 0.12);
    const cos = Math.cos(-th), sin = Math.sin(-th);
    for (let y = 0; y < H; y++)
      for (let x = Math.floor(cx - 18); x < cx + 18; x++) {
        const wy = y - amp * Math.sin(x * freq + phase);
        const dx = x - cx, dy = wy - cy;
        const rx = dx * cos - dy * sin, ry = dx * sin + dy * cos;
        const gx = (rx - sh * ry) / s + 2.5, gy = ry / s + 3.5;
        if (gx < 0 || gy < 0 || gx >= 5 || gy >= 7) continue;
        if (glyph[Math.floor(gy)][Math.floor(gx)] === "#") set(x, y, ink);
      }
  });
  curve(faint[2]);

  const raw = Buffer.alloc((W * 3 + 1) * H);
  for (let y = 0; y < H; y++) {
    raw[y * (W * 3 + 1)] = 0;
    px.copy(raw, y * (W * 3 + 1) + 1, y * W * 3, (y + 1) * W * 3);
  }
  const ihdr = Buffer.alloc(13);
  ihdr.writeUInt32BE(W, 0);
  ihdr.writeUInt32BE(H, 4);
  ihdr[8] = 8; ihdr[9] = 2; ihdr[10] = 0; ihdr[11] = 0; ihdr[12] = 0;
  return Buffer.concat([
    Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]),
    chunk("IHDR", ihdr),
    chunk("IDAT", zlib.deflateSync(raw)),
    chunk("IEND", Buffer.alloc(0)),
  ]);
}
