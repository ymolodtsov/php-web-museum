import { newChallenge, renderPng } from "./_captcha.js";

export default function handler(req, res) {
  try {
    const { answer, token } = newChallenge();
    const image = "data:image/png;base64," + renderPng(answer).toString("base64");
    res.setHeader("Cache-Control", "no-store");
    res.status(200).json({ token, image });
  } catch (err) {
    console.error(err);
    res.status(503).json({ error: "The guestbook is not available right now." });
  }
}
