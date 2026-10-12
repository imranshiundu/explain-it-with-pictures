const form = document.querySelector('#recipe-form');
const list = document.querySelector('#recipe-list');
const search = document.querySelector('#search');
const message = document.querySelector('#form-message');

function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = value;
  return div.innerHTML;
}

async function loadRecipes(query = '') {
  const response = await fetch(`/api/recipes?q=${encodeURIComponent(query)}`);
  const recipes = await response.json();
  list.innerHTML = recipes.map(r => `
    <li>
      <strong>${escapeHtml(r.title)}</strong>
      ${r.ingredients ? `<p>${escapeHtml(r.ingredients)}</p>` : ''}
      ${r.steps ? `<p>${escapeHtml(r.steps)}</p>` : ''}
    </li>
  `).join('');
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  message.textContent = '';
  const response = await fetch('/api/recipes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(Object.fromEntries(new FormData(form)))
  });
  if (!response.ok) {
    const error = await response.json();
    message.textContent = error.error;
    return;
  }
  form.reset();
  message.textContent = 'Saved!';
  loadRecipes(search.value);
});

search.addEventListener('input', () => loadRecipes(search.value));

loadRecipes();
