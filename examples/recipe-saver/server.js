const http = require('http');
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, 'public');
const DATA_FILE = process.env.DATA_FILE
  ? path.resolve(process.env.DATA_FILE)
  : path.join(__dirname, 'recipes.json');

function readRecipes() {
  try {
    return JSON.parse(fs.readFileSync(DATA_FILE, 'utf8'));
  } catch {
    return [];
  }
}

function writeRecipes(recipes) {
  fs.writeFileSync(DATA_FILE, JSON.stringify(recipes, null, 2));
}

function send(res, status, body, type = 'application/json') {
  res.writeHead(status, { 'Content-Type': type });
  res.end(body);
}

function sendJson(res, status, value) {
  send(res, status, JSON.stringify(value));
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', chunk => { data += chunk; });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host}`);

  if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/index.html')) {
    return send(res, 200, fs.readFileSync(path.join(PUBLIC_DIR, 'index.html')), 'text/html');
  }

  const staticMatch = url.pathname.match(/^\/public\/(.+)$/);
  if (req.method === 'GET' && staticMatch) {
    const filePath = path.join(PUBLIC_DIR, staticMatch[1]);
    if (!filePath.startsWith(PUBLIC_DIR + path.sep) || !fs.existsSync(filePath)) {
      return sendJson(res, 404, { error: 'Not found' });
    }
    const types = { '.css': 'text/css', '.js': 'text/javascript' };
    const type = types[path.extname(filePath)] || 'text/plain';
    return send(res, 200, fs.readFileSync(filePath), type);
  }

  if (req.method === 'GET' && url.pathname === '/api/recipes') {
    const q = (url.searchParams.get('q') || '').toLowerCase();
    const recipes = readRecipes().filter(r =>
      !q ||
      r.title.toLowerCase().includes(q) ||
      r.ingredients.toLowerCase().includes(q)
    );
    return sendJson(res, 200, recipes);
  }

  if (req.method === 'POST' && url.pathname === '/api/recipes') {
    const raw = await readBody(req);
    let body;
    try {
      body = JSON.parse(raw || '{}');
    } catch {
      return sendJson(res, 400, { error: 'That did not look like a recipe. Please try again.' });
    }
    if (typeof body.title !== 'string' || !body.title.trim()) {
      return sendJson(res, 400, { error: 'Please give your recipe a title.' });
    }
    const recipe = {
      id: crypto.randomUUID(),
      title: body.title.trim(),
      ingredients: String(body.ingredients || '').trim(),
      steps: String(body.steps || '').trim(),
      created_at: new Date().toISOString()
    };
    const recipes = readRecipes();
    recipes.push(recipe);
    writeRecipes(recipes);
    return sendJson(res, 201, recipe);
  }

  sendJson(res, 404, { error: 'Not found' });
});

server.listen(PORT, () => {
  console.log(`Recipe Saver running at http://localhost:${PORT}`);
});
