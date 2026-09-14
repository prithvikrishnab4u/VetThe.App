async function loadApps() {
  const res = await fetch('/data/apps.json');
  const apps = await res.json();

  const container = document.getElementById('apps-container');
  const filters = document.getElementById('apps-filters');

  // Build category filter
  const cats = Array.from(new Set(apps.map(a=>a.category).filter(Boolean))).sort();
  const catSelect = document.createElement('select');
  const allOpt = document.createElement('option'); allOpt.value=''; allOpt.text='All categories'; catSelect.appendChild(allOpt);
  cats.forEach(c=>{ const o=document.createElement('option'); o.value=c; o.text=c; catSelect.appendChild(o); });
  filters.appendChild(catSelect);

  const table = document.createElement('table');
  table.className = 'apps-table';
  const thead = document.createElement('thead');
  thead.innerHTML = '<tr><th></th><th>Name</th><th>Category</th><th>SSO</th><th>SCIM</th><th>MFA</th><th>Compliance</th><th>Last Verified</th></tr>';
  table.appendChild(thead);
  const tbody = document.createElement('tbody');
  table.appendChild(tbody);

  function renderRows(filterCat) {
    tbody.innerHTML='';
    const visible = apps.filter(a => !filterCat || a.category === filterCat);
    visible.forEach(a=>{
      const tr = document.createElement('tr');
      const id = a._id || a.name;
      tr.innerHTML = `
        <td><input type="checkbox" class="cmp" data-id="${id}"></td>
        <td><strong>${a.name||id}</strong></td>
        <td>${a.category||''}</td>
        <td>${(a.sso && a.sso.protocols)? a.sso.protocols.join(', '): (a.sso && a.sso.supported? 'Yes':'No')}</td>
        <td>${a.scim && a.scim.supported? a.scim.supported : 'No'}</td>
        <td>${(a.mfa && a.mfa.types)? a.mfa.types.join(', '): (a.mfa && a.mfa.supported? 'Yes':'No')}</td>
        <td>${(a.compliance && a.compliance.soc2? 'SOC2 ':'') + (a.compliance && a.compliance.iso27001? 'ISO27001':'')}</td>
        <td>${(a.meta && a.meta.last_verified) || ''}</td>
      `;
      tbody.appendChild(tr);
    });
  }

  catSelect.addEventListener('change', ()=> renderRows(catSelect.value));
  renderRows('');

  container.appendChild(filters);
  container.appendChild(table);

  // Compare button
  const btn = document.createElement('button'); btn.textContent='Compare selected'; btn.style.marginTop='8px';
  container.appendChild(btn);

  btn.addEventListener('click', ()=>{
    const checked = Array.from(document.querySelectorAll('.cmp:checked')).map(i=>i.dataset.id);
    if(checked.length < 2) { alert('Select at least two apps to compare'); return; }
    const sel = apps.filter(a=> checked.includes((a._id||a.name)));
    showComparison(sel);
  });

  function showComparison(list) {
    let cmp = document.getElementById('compare-area');
    if(!cmp){ cmp = document.createElement('div'); cmp.id='compare-area'; cmp.style.marginTop='16px'; container.appendChild(cmp); }
    cmp.innerHTML='';
    const fields = ['name','category','sso.protocols','scim.supported','mfa.types','compliance.soc2','compliance.iso27001','meta.last_verified'];
    const table = document.createElement('table'); table.className='compare-table';
    const thead = document.createElement('thead');
    thead.innerHTML = '<tr><th>Field</th>' + list.map(a=>`<th>${a.name}</th>`).join('') + '</tr>';
    table.appendChild(thead);
    const tbody = document.createElement('tbody');
    fields.forEach(f=>{
      const tr = document.createElement('tr');
      const label = f.replace('.', ' › ');
      const tds = list.map(a=>{
        const parts = f.split('.');
        let v = a;
        for(const p of parts){ v = v && v[p]; }
        if(Array.isArray(v)) v = v.join(', ');
        return `<td>${v||''}</td>`;
      }).join('');
      tr.innerHTML = `<td><strong>${label}</strong></td>` + tds;
      tbody.appendChild(tr);
    });
    table.appendChild(tbody);
    cmp.appendChild(table);
  }
}

document.addEventListener('DOMContentLoaded', loadApps);
