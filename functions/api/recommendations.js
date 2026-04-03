export async function onRequestGet(context) {
  const { env } = context;

  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  };

  // Serve cache if under 4 hours old
  try {
    const cached = await env.FOSTER_FINANCE.get('recommendations_cache');
    if (cached) {
      const parsed = JSON.parse(cached);
      const age = Date.now() - new Date(parsed.generated_at).getTime();
      if (age < 4 * 60 * 60 * 1000) {
        return new Response(cached, { headers });
      }
    }
  } catch(e) {}

  const plaidBase = 'https://production.plaid.com';
  const institutionsRaw = await env.FOSTER_FINANCE.get('connected_institutions');
  if (!institutionsRaw) {
    return new Response(JSON.stringify({ alerts: [], recommendations: [], health_score: 50, health_label: 'Unknown', summary: 'No accounts connected.' }), { headers });
  }

  const institutions = JSON.parse(institutionsRaw);
  let allTransactions = [];
  let allAccounts = [];

  const startDate = new Date(Date.now() - 30 * 86400000).toISOString().split('T')[0];
  const endDate = new Date().toISOString().split('T')[0];

  for (const inst of institutions) {
    try {
      const tokenRaw = await env.FOSTER_FINANCE.get(inst.key);
      if (!tokenRaw) continue;
      const { access_token } = JSON.parse(tokenRaw);

      // Balances
      const balRes = await fetch(`${plaidBase}/accounts/balance/get`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ client_id: env.PLAID_CLIENT_ID, secret: env.PLAID_SECRET, access_token }),
      });
      const balData = await balRes.json();
      if (balData.accounts) {
        for (const a of balData.accounts) allAccounts.push({ ...a, institution: inst.name });
      }

      // Transactions
      const txnRes = await fetch(`${plaidBase}/transactions/get`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          client_id: env.PLAID_CLIENT_ID,
          secret: env.PLAID_SECRET,
          access_token,
          start_date: startDate,
          end_date: endDate,
          options: { count: 100, offset: 0 },
        }),
      });
      const txnData = await txnRes.json();
      if (txnData.transactions) allTransactions.push(...txnData.transactions);
    } catch(e) {
      console.error(`Error fetching ${inst.name}:`, e);
    }
  }

  // Summarize
  const totalCash = allAccounts
    .filter(a => a.type === 'depository')
    .reduce((sum, a) => sum + (a.balances.current || 0), 0);
  const creditDebt = allAccounts
    .filter(a => a.type === 'credit')
    .reduce((sum, a) => sum + (a.balances.current || 0), 0);

  const spending = {};
  const merchants = {};
  for (const txn of allTransactions) {
    if (txn.amount > 0) {
      const cat = txn.personal_finance_category?.primary || txn.category?.[0] || 'Other';
      spending[cat] = (spending[cat] || 0) + txn.amount;
      if (txn.merchant_name) {
        merchants[txn.merchant_name] = (merchants[txn.merchant_name] || 0) + txn.amount;
      }
    }
  }

  const topMerchants = Object.entries(merchants)
    .sort((a, b) => b[1] - a[1]).slice(0, 15)
    .map(([name, amount]) => `${name}: $${amount.toFixed(2)}`).join('\n');

  const topCategories = Object.entries(spending)
    .sort((a, b) => b[1] - a[1])
    .map(([k, v]) => `${k}: $${v.toFixed(2)}`).join('\n');

  // Find Amex charge card - flag if high balance
  const amex = allAccounts.find(a => a.institution === 'American Express' && a.type === 'credit');
  const amexBalance = amex?.balances?.current || 0;

  const prompt = `You are Skippy, Scott Foster's personal AI finance advisor. Analyze real transaction data and return actionable JSON.

ACCOUNTS (${new Date().toLocaleDateString()}):
${allAccounts.map(a => `${a.institution} ${a.name} (${a.type}): $${a.balances.current?.toFixed(2)}`).join('\n')}

Total cash: $${totalCash.toFixed(2)}
Total credit owed: $${creditDebt.toFixed(2)}

TOP SPENDING CATEGORIES (last 30 days):
${topCategories}

TOP MERCHANTS (last 30 days):
${topMerchants}

KNOWN CONTEXT:
- Amex Platinum is a CHARGE CARD — full balance due every cycle, no carrying. Current: $${amexBalance.toFixed(2)}
- Verizon ~$230/mo — T-Mobile switch planned (~$75/mo savings)
- Monthly subscriptions ~$620/mo known burn
- GCP billing: RESOLVED
- PayPal Credit: RESOLVED and closed
- Chase savings $29k is healthy emergency fund

Return ONLY valid JSON, no markdown:
{
  "alerts": [
    {"level": "critical|warning|info", "title": "short title", "message": "specific actionable message with real dollar amounts"}
  ],
  "recommendations": [
    {"priority": 1, "title": "title", "detail": "specific actionable detail with real numbers", "savings": "$X/mo or $X one-time"}
  ],
  "health_score": 0-100,
  "health_label": "Excellent|Good|Fair|Poor",
  "summary": "2 sentence plain-english summary using real numbers from data"
}

Rules: Max 3 alerts. Max 5 recommendations. Only flag REAL issues from actual data. Never mention GCP or PayPal Credit — those are resolved. Be Skippy — direct, specific, occasionally sardonic.`;

  const claudeRes = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'x-api-key': env.ANTHROPIC_API_KEY,
      'anthropic-version': '2023-06-01',
    },
    body: JSON.stringify({
      model: 'claude-haiku-4-5-20251001',
      max_tokens: 1024,
      messages: [{ role: 'user', content: prompt }],
    }),
  });

  const claudeData = await claudeRes.json();
  const rawText = claudeData.content?.[0]?.text || '{}';

  let parsed;
  try {
    parsed = JSON.parse(rawText.replace(/```json\n?|\n?```/g, '').trim());
  } catch(e) {
    parsed = {
      alerts: [{ level: 'info', title: 'Analysis Ready', message: 'Financial data loaded. ' + allTransactions.length + ' transactions analyzed.' }],
      recommendations: [],
      health_score: 75,
      health_label: 'Good',
      summary: `Cash position $${totalCash.toFixed(0)}, credit owed $${creditDebt.toFixed(0)}.`
    };
  }

  const result = {
    ...parsed,
    generated_at: new Date().toISOString(),
    snapshot: {
      total_cash: totalCash,
      credit_debt: creditDebt,
      transactions_analyzed: allTransactions.length,
    }
  };

  await env.FOSTER_FINANCE.put('recommendations_cache', JSON.stringify(result), { expirationTtl: 14400 });
  return new Response(JSON.stringify(result), { headers });
}

export async function onRequestOptions() {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    },
  });
}
