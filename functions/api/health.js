// Foster Labs — Health API
// Auth: X-Health-Auth header must equal sha256('cjf11307#')
// 5e7e5641da6bdceafb9ec94e6f1074cd98373f407890e23a01db3f3143ac426f

const AUTH_HASH = '5e7e5641da6bdceafb9ec94e6f1074cd98373f407890e23a01db3f3143ac426f';

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, PATCH, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, X-Health-Auth',
};

const json = (data, status = 200) =>
  new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json', ...cors },
  });

async function checkAuth(request) {
  const auth = request.headers.get('X-Health-Auth');
  return auth === AUTH_HASH;
}

export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const action = url.searchParams.get('action');

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: cors });
  }

  if (!(await checkAuth(request))) {
    return json({ error: 'unauthorized' }, 401);
  }

  if (!env.HEALTH_DB) {
    return json({ error: 'D1 not bound' }, 500);
  }

  try {
    // ============ MEDS ============
    if (action === 'meds' && request.method === 'GET') {
      const { results } = await env.HEALTH_DB.prepare(
        'SELECT * FROM meds ORDER BY is_peptide DESC, name ASC'
      ).all();
      return json({ meds: results });
    }

    // ============ VIALS ============
    if (action === 'vials' && request.method === 'GET') {
      const med = url.searchParams.get('med');
      const showAll = url.searchParams.get('all') === '1';
      let query = 'SELECT * FROM vials';
      const conds = [];
      const binds = [];
      if (med) { conds.push('med_name = ?'); binds.push(med); }
      if (!showAll) { conds.push('active = 1'); }
      if (conds.length) query += ' WHERE ' + conds.join(' AND ');
      query += ' ORDER BY reconstituted_at DESC';
      const stmt = env.HEALTH_DB.prepare(query);
      const { results } = binds.length ? await stmt.bind(...binds).all() : await stmt.all();
      return json({ vials: results });
    }

    if (action === 'vial_create' && request.method === 'POST') {
      const body = await request.json();
      const result = await env.HEALTH_DB.prepare(
        `INSERT INTO vials (med_name, vial_mg, bac_water_ml, syringe_total_ml, syringe_total_units, reconstituted_at, notes, active)
         VALUES (?, ?, ?, ?, ?, ?, ?, 1) RETURNING *`
      ).bind(
        body.med_name,
        body.vial_mg,
        body.bac_water_ml,
        body.syringe_total_ml,
        body.syringe_total_units,
        body.reconstituted_at || new Date().toISOString(),
        body.notes || null
      ).first();
      return json({ vial: result });
    }

    if (action === 'vial_archive' && request.method === 'POST') {
      const body = await request.json();
      await env.HEALTH_DB.prepare('UPDATE vials SET active = 0 WHERE id = ?').bind(body.id).run();
      return json({ ok: true });
    }

    if (action === 'vial_delete' && request.method === 'POST') {
      const body = await request.json();
      await env.HEALTH_DB.prepare('DELETE FROM vials WHERE id = ?').bind(body.id).run();
      return json({ ok: true });
    }

    // ============ DOSES ============
    if (action === 'doses' && request.method === 'GET') {
      const med = url.searchParams.get('med');
      const limit = parseInt(url.searchParams.get('limit') || '50');
      let query = `SELECT d.*, v.vial_mg, v.bac_water_ml FROM doses d
                   LEFT JOIN vials v ON d.vial_id = v.id`;
      const binds = [];
      if (med) { query += ' WHERE d.med_name = ?'; binds.push(med); }
      query += ' ORDER BY d.taken_at DESC LIMIT ?';
      binds.push(limit);
      const { results } = await env.HEALTH_DB.prepare(query).bind(...binds).all();
      return json({ doses: results });
    }

    if (action === 'dose_log' && request.method === 'POST') {
      const body = await request.json();
      const result = await env.HEALTH_DB.prepare(
        `INSERT INTO doses (med_name, dose_amount, dose_unit, syringe_units, vial_id, taken_at, notes)
         VALUES (?, ?, ?, ?, ?, ?, ?) RETURNING *`
      ).bind(
        body.med_name,
        body.dose_amount,
        body.dose_unit,
        body.syringe_units || null,
        body.vial_id || null,
        body.taken_at || new Date().toISOString(),
        body.notes || null
      ).first();
      return json({ dose: result });
    }

    if (action === 'dose_delete' && request.method === 'POST') {
      const body = await request.json();
      await env.HEALTH_DB.prepare('DELETE FROM doses WHERE id = ?').bind(body.id).run();
      return json({ ok: true });
    }

    // ============ STATS ============
    if (action === 'stats' && request.method === 'GET') {
      const { results: lastDoses } = await env.HEALTH_DB.prepare(
        `SELECT med_name, MAX(taken_at) as last_taken, COUNT(*) as count_30d
         FROM doses
         WHERE taken_at > datetime('now', '-30 days')
         GROUP BY med_name`
      ).all();
      const { results: activeVials } = await env.HEALTH_DB.prepare(
        `SELECT v.*, COUNT(d.id) as doses_drawn,
         COALESCE(SUM(d.syringe_units), 0) as units_drawn
         FROM vials v
         LEFT JOIN doses d ON d.vial_id = v.id
         WHERE v.active = 1
         GROUP BY v.id`
      ).all();
      return json({ lastDoses, activeVials });
    }

    return json({ error: 'unknown action' }, 400);
  } catch (e) {
    return json({ error: e.message, stack: e.stack }, 500);
  }
}
