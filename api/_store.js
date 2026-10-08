// Guestbook storage: one public JSON blob per entry in Vercel Blob.
// Entries hold only what the page shows (name, message, date).
const PREFIX = "guestbook/";
const memory = [];

function useBlob() {
  if (process.env.BLOB_READ_WRITE_TOKEN) return true;
  if (process.env.VERCEL_ENV) throw new Error("BLOB_READ_WRITE_TOKEN is not set");
  return false; // local development: keep entries in memory
}

export async function addEntry(nonce, entry) {
  if (!useBlob()) {
    if (memory.some((e) => e.nonce === nonce)) throw new Error("duplicate");
    memory.push({ nonce, ...entry });
    return;
  }
  const { put } = await import("@vercel/blob");
  // The captcha nonce alone names the blob, so a solved captcha can't be used twice.
  await put(`${PREFIX}${nonce}.json`, JSON.stringify(entry), {
    access: "public",
    contentType: "application/json",
    addRandomSuffix: false,
    allowOverwrite: false,
  });
}

export async function listEntries(limit = 200) {
  if (!useBlob()) return memory.map(({ nonce, ...e }) => e);
  const { list } = await import("@vercel/blob");
  const { blobs } = await list({ prefix: PREFIX, limit: 1000 });
  const recent = blobs.sort((a, b) => new Date(b.uploadedAt) - new Date(a.uploadedAt)).slice(0, limit);
  const entries = await Promise.all(
    recent.map(async (b) => {
      try {
        const r = await fetch(b.url);
        return r.ok ? await r.json() : null;
      } catch {
        return null;
      }
    }),
  );
  return entries.filter(Boolean);
}
