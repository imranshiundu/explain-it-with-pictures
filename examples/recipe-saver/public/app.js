const form = document.querySelector('#recipe-form');
const list = document.querySelector('#recipe-list');
const search = document.querySelector('#search');
const message = document.querySelector('#form-message');
const toast = document.querySelector('#toast');
const submitButton = form.querySelector('button[type="submit"]');

let toastTimer = null;

function showToast(text) {
  toast.textContent = text;
  toast.classList.add('show');
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove('show'), 2200);
}

function escapeHtml(value) {
  const div = document.createElement('div');
  div.textContent = value;
  return div.innerHTML;
}

async function loadRecipes(query = '') {
  const response = await fetch(`/api/recipes?q=${encodeURIComponent(query)}`);
  const recipes = await response.json();
  if (recipes.length === 0) {
    const text = query
      ? `No recipes match "${escapeHtml(query)}". Try another word.`
      : 'Your book is empty. Save your first recipe above — it will live here.';
    list.innerHTML = `<li class="empty">${text}</li>`;
    return;
  }
  list.innerHTML = recipes.map((r, i) => `
    <li style="--i:${i}">
      <strong>${escapeHtml(r.title)}</strong>
      ${r.ingredients ? `<p>${escapeHtml(r.ingredients)}</p>` : ''}
      ${r.steps ? `<p>${escapeHtml(r.steps)}</p>` : ''}
    </li>
  `).join('');
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  message.textContent = '';
  message.classList.remove('ok');
  submitButton.disabled = true;
  try {
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
    message.classList.add('ok');
    showToast('Recipe saved');
    loadRecipes(search.value);
  } catch {
    message.textContent = 'The kitchen is not answering. Is the server still running?';
  } finally {
    submitButton.disabled = false;
  }
});

search.addEventListener('input', () => loadRecipes(search.value));

loadRecipes();
