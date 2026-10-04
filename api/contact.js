const ALLOWED_ORIGIN = process.env.SITE_ORIGIN || 'https://nicksc1cc.github.io';
const WINDOW_MS = 60_000;
const MAX_REQUESTS = 5;
const requests = new Map();

function corsHeaders(origin) {
  const allowed = origin === ALLOWED_ORIGIN ? origin : ALLOWED_ORIGIN;
  return {
    'Access-Control-Allow-Origin': allowed,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    Vary: 'Origin'
  };
}

function json(res, status, payload, origin) {
  Object.entries(corsHeaders(origin)).forEach(([key, value]) => res.setHeader(key, value));
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.status(status).json(payload);
}

function clean(value, max) {
  return String(value || '').replace(/[<>]/g, '').trim().slice(0, max);
}

function isEmail(value) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

module.exports = async function handler(req, res) {
  const origin = req.headers.origin || ALLOWED_ORIGIN;
  if (req.method === 'OPTIONS') return json(res, 204, {}, origin);
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed.' }, origin);
  if (!process.env.ATTIO_API_TOKEN) return json(res, 503, { error: 'The contact service is not configured yet.' }, origin);

  const ip = String(req.headers['x-forwarded-for'] || req.socket?.remoteAddress || 'unknown').split(',')[0].trim();
  const now = Date.now();
  const recent = (requests.get(ip) || []).filter((time) => now - time < WINDOW_MS);
  if (recent.length >= MAX_REQUESTS) return json(res, 429, { error: 'Please wait a moment before trying again.' }, origin);
  recent.push(now);
  requests.set(ip, recent);

  const body = req.body || {};
  if (clean(body.website, 100)) return json(res, 200, { success: true }, origin);

  const name = clean(body.name, 120);
  const email = clean(body.email, 254).toLowerCase();
  const company = clean(body.company, 200);
  const message = clean(body.message, 5000);
  const requestAudit = body.request_audit === true || body.request_audit === 'yes';

  if (!name || !email || !message) return json(res, 400, { error: 'Name, email and message are required.' }, origin);
  if (!isEmail(email)) return json(res, 400, { error: 'Please enter a valid email address.' }, origin);
  if (message.length < 10) return json(res, 400, { error: 'Please add a little more detail to your message.' }, origin);

  const headers = {
    Authorization: `Bearer ${process.env.ATTIO_API_TOKEN}`,
    'Content-Type': 'application/json'
  };
  const personResponse = await fetch('https://api.attio.com/v2/objects/people/records?matching_attribute=email_addresses', {
    method: 'PUT',
    headers,
    body: JSON.stringify({ data: { values: {
      email_addresses: [{ email_address: email }],
      name: [{ full_name: name }]
    } } })
  });

  if (!personResponse.ok) return json(res, 502, { error: 'We could not save your message. Please email hello@inflexion.co instead.' }, origin);
  const person = await personResponse.json();
  const recordId = person?.data?.id?.record_id;

  if (recordId) {
    const note = [
      `Contact form message`,
      `Company: ${company || 'Not provided'}`,
      `Request an AI visibility audit: ${requestAudit ? 'Yes' : 'No'}`,
      '',
      message
    ].join('\n');
    const noteResponse = await fetch('https://api.attio.com/v2/notes', {
      method: 'POST',
      headers,
      body: JSON.stringify({ data: {
        parent_object: 'people',
        parent_record_id: recordId,
        title: requestAudit ? 'Website enquiry — audit requested' : 'Website enquiry',
        format: 'plaintext',
        content: note
      } })
    });
    if (!noteResponse.ok) return json(res, 502, { error: 'Your contact was saved, but the message note could not be attached.' }, origin);
  }

  return json(res, 200, { success: true }, origin);
};
