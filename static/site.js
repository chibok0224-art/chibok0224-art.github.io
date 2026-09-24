// Client-side filter and sort for long lists. No dependencies.
//   <input data-filter="#list" data-count="#count">  hides [data-search] items that don't match,
//                                                    and [data-group] sections left empty
//   <select data-sort="#list">                         orders children by data-<value>
for (const input of document.querySelectorAll('[data-filter]')) {
  const root = document.querySelector(input.dataset.filter);
  const items = [...root.querySelectorAll('[data-search]')];
  const groups = [...root.querySelectorAll('[data-group]')];
  const count = input.dataset.count && document.querySelector(input.dataset.count);
  const apply = () => {
    const term = input.value.trim().toLowerCase();
    let shown = 0;
    for (const item of items) {
      item.hidden = term !== '' && !item.dataset.search.includes(term);
      if (!item.hidden) shown++;
    }
    for (const g of groups) g.hidden = !g.querySelector('[data-search]:not([hidden])');
    if (count) count.textContent = term ? `${shown} of ${items.length}` : `${items.length}`;
  };
  input.addEventListener('input', apply);
  apply();
}

for (const select of document.querySelectorAll('[data-sort]')) {
  const list = document.querySelector(select.dataset.sort);
  select.addEventListener('change', () => {
    const key = select.value;
    const dir = key === 'price' || key === 'rank' ? 1 : -1;
    [...list.children]
      .sort((a, b) => dir * (a.dataset[key] - b.dataset[key]))
      .forEach((el) => list.appendChild(el));
  });
}
