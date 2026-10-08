import { verify } from "./_captcha.js";
import { addEntry, listEntries } from "./_store.js";

const clean = (s, max) =>
  String(s ?? "")
    .replace(/[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]/g, "")
    .replace(/\r\n?/g, "\n")
    .trim()
    .slice(0, max);

export default async function handler(req, res) {
  try {
    if (req.method === "GET") {
      res.setHeader("Cache-Control", "public, s-maxage=30, stale-while-revalidate=300");
      return res.status(200).json({ entries: await listEntries() });
    }
    if (req.method !== "POST") {
      res.setHeader("Allow", "GET, POST");
      return res.status(405).json({ error: "Method not allowed." });
    }

    const body = typeof req.body === "string" ? JSON.parse(req.body || "{}") : req.body || {};
    const name = clean(body.name, 40);
    const message = clean(body.message, 1000);
    if (!name || !message) return res.status(400).json({ error: "Please fill in your name and a message." });

    const check = verify(body.token, body.code);
    if (!check.ok) {
      const msg = check.reason === "expired"
        ? "That code has expired. Here is a new one."
        : "The code you entered doesn't match the image. Please try again.";
      return res.status(400).json({ error: msg, newCode: true });
    }

    const entry = { name, message, date: new Date().toISOString() };
    // Hidden field that people never see; bots fill it in. Pretend it worked.
    if (body.homepage) return res.status(200).json({ entry });

    try {
      await addEntry(check.nonce, entry);
    } catch (err) {
      if (/duplicate|already exists/i.test(String(err && err.message))) {
        return res.status(400).json({ error: "That code was already used. Here is a new one.", newCode: true });
      }
      throw err;
    }
    return res.status(201).json({ entry });
  } catch (err) {
    console.error(err);
    return res.status(503).json({ error: "The guestbook is not available right now." });
  }
}
