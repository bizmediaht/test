/* BiZ Insider — Administration de la billetterie : validation des paiements et pointage */
(function () {
  'use strict';
  var SUPABASE_URL = 'https://sljzkbcpkecpvvpzskxa.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_SSQwmuNgdfpoK-RJdBD0pw_TWgG-uA4';
  var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  var ROOT = document.body.getAttribute('data-root') || '';
  var PAGE = document.body.getAttribute('data-page');

  function $(s, el) { return (el || document).querySelector(s); }
  function h(tag, attrs, kids) {
    var el = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === 'text') el.textContent = attrs[k];
      else if (k.slice(0, 2) === 'on') el.addEventListener(k.slice(2), attrs[k]);
      else if (attrs[k] !== null && attrs[k] !== undefined && attrs[k] !== false) el.setAttribute(k, attrs[k] === true ? '' : attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) el.appendChild(typeof c === 'string' ? document.createTextNode(c) : c); });
    return el;
  }
  function money(n) { return new Intl.NumberFormat('fr-FR').format(n) + ' HTG'; }
  function when(d) { return new Intl.DateTimeFormat('fr-FR', { dateStyle: 'medium', timeStyle: 'short', timeZone: 'America/Port-au-Prince' }).format(new Date(d)); }
  function url(path) { return new URL(ROOT + path, location.href).href; }
  function normPhone(p) { var d = String(p || '').replace(/\D/g, ''); if (d.length === 8) d = '509' + d; return d; }
  function ticketsMessage(o, codes) {
    return 'Bonjour ' + o.buyer_name + ', votre paiement est confirmé ✅\n' +
      'Voici vos billets pour ' + o.events.title + ' (' + when(o.events.starts_at) + ') :\n' +
      codes.map(function (c) { return url('billet/?c=' + c); }).join('\n') +
      '\nPrésentez le QR code à l’entrée. — BiZ Insider';
  }
  var app = $('#app');
  var ACCESS = null;

  /* ---------- Connexion ---------- */
  async function requireAdmin() {
    var s = await sb.auth.getSession();
    if (!s.data.session) { loginView(); return false; }
    var a = await sb.rpc('my_access');
    ACCESS = a.data || { orgs: [] };
    if (!(ACCESS.superadmin || ACCESS.orgs.length)) {
      app.replaceChildren(h('div', { class: 'panel' }, [
        h('h1', { class: 'ev-title', text: 'Compte non autorisé' }),
        h('p', { class: 'lead', text: 'Le compte ' + s.data.session.user.email + ' n’est pas encore administrateur. Demandez à BiZ Insider de l’ajouter.' }),
        h('button', { class: 'btn btn-navy', type: 'button', onclick: logout, text: 'Se déconnecter' })
      ]));
      return false;
    }
    $('#who').replaceChildren(
      ACCESS.superadmin ? h('a', { class: 'linkbtn', href: ROOT + 'admin/participants/', text: 'Base nationale' }) : '',
      ACCESS.superadmin ? ' · ' : '',
      s.data.session.user.email + ' · ', h('button', { class: 'linkbtn', type: 'button', onclick: logout, text: 'Déconnexion' }));
    return true;
  }
  async function logout() { await sb.auth.signOut(); location.reload(); }
  function loginView() {
    var st = h('p', { 'aria-live': 'polite' });
    var f = h('form', { class: 'panel login' }, [
      h('h1', { class: 'ev-title', text: 'Espace billetterie' }),
      h('label', null, ['E-mail', h('input', { name: 'email', type: 'email', required: true, autocomplete: 'username' })]),
      h('label', null, ['Mot de passe', h('input', { name: 'pw', type: 'password', required: true, minlength: 8, autocomplete: 'current-password' })]),
      h('div', { class: 'actions' }, [
        h('button', { class: 'btn btn-navy', type: 'submit', text: 'Se connecter' }),
        h('button', { class: 'btn btn-ghost-dark', type: 'button', text: 'Créer le compte', onclick: async function () {
          if (!f.reportValidity()) return;
          var r = await sb.auth.signUp({ email: f.email.value, password: f.pw.value });
          st.textContent = r.error ? r.error.message : 'Compte créé. Confirmez votre e-mail avec le lien reçu, puis demandez à être ajouté comme administrateur.';
        } })
      ]), st
    ]);
    f.addEventListener('submit', async function (e) {
      e.preventDefault();
      var r = await sb.auth.signInWithPassword({ email: f.email.value, password: f.pw.value });
      if (r.error) { st.textContent = r.error.message === 'Email not confirmed' ? 'Confirmez d’abord votre e-mail (lien reçu par e-mail).' : 'E-mail ou mot de passe incorrect.'; return; }
      location.reload();
    });
    app.replaceChildren(f);
  }

  /* ---------- Tableau de bord ---------- */
  var state = { event: null, status: 'pending' };
  async function dashboard() {
    if (!(await requireAdmin())) return;
    var evq = sb.from('events').select('id, title, starts_at, slug, org_id, organizations(name)').order('starts_at', { ascending: false });
    if (!ACCESS.superadmin) evq = evq.in('org_id', ACCESS.orgs.map(function (o) { return o.id; }));
    var evs = await evq;
    if (evs.error || !evs.data.length) { app.replaceChildren(h('p', { class: 'note', text: 'Aucun événement.' })); return; }
    state.event = state.event || evs.data[0].id;
    var sel = h('select', { 'aria-label': 'Événement', onchange: function () { state.event = sel.value; render(); } },
      evs.data.map(function (e) { return h('option', { value: e.id, selected: e.id === state.event, text: (e.organizations ? e.organizations.name + ' · ' : '') + e.title + ' — ' + when(e.starts_at) }); }));
    var tabs = h('div', { class: 'tabs', role: 'tablist' }, [['pending', 'À vérifier'], ['paid', 'Payées'], ['rejected', 'Refusées'], ['people', 'Participants'], ['profile', 'Profil']].map(function (t) {
      return h('button', { type: 'button', role: 'tab', 'aria-selected': String(state.status === t[0]), 'data-s': t[0], text: t[1], onclick: function () { state.status = t[0]; render(); } });
    }));
    var stats = h('div', { class: 'adm-stats' }); var list = h('div', { class: 'orders' });
    var csvBtn = h('button', { class: 'btn btn-ghost-dark', type: 'button', text: 'Exporter (CSV)', onclick: function () { exportCsv(); } });
    app.replaceChildren(h('div', { class: 'adm-bar' }, [sel, h('div', { class: 'actions' }, [csvBtn, h('a', { class: 'btn btn-gold', href: 'scan/', text: 'Scanner les billets' })])]), stats, tabs, list);
    var cache = { orders: [], byOrder: {}, questions: [] };
    cacheRef = function () { return cache; };

    async function render() {
      tabs.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-selected', String(b.getAttribute('data-s') === state.status)); });
      list.replaceChildren(h('p', { class: 'note', text: 'Chargement…' }));
      var all = await sb.from('orders').select('id, status, quantity, amount_htg, buyer_name, buyer_phone, buyer_email, consent_biz, answers, payment_method, payment_ref, proof_path, reject_reason, created_at, ticket_type_id, ticket_types(name, questions), events(title, starts_at, questions)').eq('event_id', state.event).order('created_at', { ascending: false });
      var tk = await sb.from('tickets').select('order_id, code, checked_in_at').eq('event_id', state.event);
      if (all.error) { list.replaceChildren(h('p', { class: 'note err', text: all.error.message })); return; }
      var byOrder = {}; (tk.data || []).forEach(function (t) { (byOrder[t.order_id] = byOrder[t.order_id] || []).push(t); });
      var paid = all.data.filter(function (o) { return o.status === 'paid'; });
      var sold = paid.reduce(function (s, o) { return s + o.quantity; }, 0);
      var cash = paid.reduce(function (s, o) { return s + o.amount_htg; }, 0);
      var pend = all.data.filter(function (o) { return o.status === 'pending'; }).length;
      var inn = (tk.data || []).filter(function (t) { return t.checked_in_at; }).length;
      stats.replaceChildren.apply(stats, [['Billets émis', sold], ['Encaissé', money(cash)], ['À vérifier', pend], ['Entrées pointées', inn + ' / ' + sold]].map(function (s) {
        return h('div', null, [h('b', { text: String(s[1]) }), h('span', { text: s[0] })]);
      }));
      cache.orders = all.data; cache.byOrder = byOrder; cache.questions = questionsOf(all.data);
      if (state.status === 'people') return peopleView(list, cache);
      if (state.status === 'profile') return profileView(list, cache);
      var rows = all.data.filter(function (o) { return o.status === state.status; });
      if (!rows.length) { list.replaceChildren(h('p', { class: 'note', text: 'Aucune commande ici.' })); return; }
      list.replaceChildren.apply(list, rows.map(function (o) { return orderCard(o, byOrder[o.id] || [], render); }));
    }
    render();
  }

  /* ---------- CRM : participants, profil, export ---------- */
  function questionsOf(orders) {
    var seen = {}, out = [];
    orders.forEach(function (o) {
      var qs = (o.ticket_types && o.ticket_types.questions) || (o.events && o.events.questions) || [];
      qs.forEach(function (q) { if (!seen[q.id]) { seen[q.id] = 1; out.push(q); } });
    });
    return out;
  }
  function confirmed(c) { return c.orders.filter(function (o) { return o.status === 'paid'; }); }
  function present(c, o) { return (c.byOrder[o.id] || []).some(function (t) { return t.checked_in_at; }); }

  function peopleView(list, c) {
    var rows = confirmed(c);
    var search = h('input', { type: 'search', placeholder: 'Rechercher un nom, un téléphone, une réponse…', 'aria-label': 'Rechercher' });
    var typeSel = h('select', { 'aria-label': 'Type de billet' }, [h('option', { value: '', text: 'Tous les billets' })].concat(
      Array.from(new Set(rows.map(function (o) { return o.ticket_types.name; }))).map(function (n) { return h('option', { value: n, text: n }); })));
    var count = h('p', { class: 'note' });
    var wrap = h('div', { class: 'tbl-wrap' });
    function draw() {
      var term = search.value.trim().toLowerCase(), ty = typeSel.value;
      var f = rows.filter(function (o) {
        if (ty && o.ticket_types.name !== ty) return false;
        if (!term) return true;
        return [o.buyer_name, o.buyer_phone, o.buyer_email || ''].concat(Object.values(o.answers || {})).join(' ').toLowerCase().indexOf(term) >= 0;
      });
      count.textContent = f.length + ' participant(s) · ' + f.filter(function (o) { return present(c, o); }).length + ' présent(s) le jour J';
      var qs = c.questions;
      wrap.replaceChildren(h('table', { class: 'crm' }, [
        h('thead', null, [h('tr', null, ['Nom', 'Téléphone', 'Billet'].concat(qs.map(function (q) { return q.label; }), ['Présent', 'Contact BiZ']).map(function (t) { return h('th', { text: t }); }))]),
        h('tbody', null, f.map(function (o) {
          return h('tr', null, [o.buyer_name, o.buyer_phone, o.quantity + ' × ' + o.ticket_types.name].concat(
            qs.map(function (q) { return (o.answers || {})[q.id] || ''; }), [present(c, o) ? '✓' : '', o.consent_biz ? 'oui' : 'non']
          ).map(function (v) { return h('td', { text: String(v) }); }));
        }))
      ]));
    }
    search.addEventListener('input', draw); typeSel.addEventListener('change', draw);
    list.replaceChildren(h('div', { class: 'adm-bar' }, [search, typeSel]), count, wrap);
    draw();
  }

  function profileView(list, c) {
    var rows = confirmed(c);
    var groups = {};
    rows.forEach(function (o) { var n = o.ticket_types.name; (groups[n] = groups[n] || { qs: (o.ticket_types.questions || (o.events && o.events.questions) || []), rows: [] }).rows.push(o); });
    var names = Object.keys(groups);
    if (!names.length) { list.replaceChildren(h('p', { class: 'note', text: 'Pas encore de participants confirmés.' })); return; }
    list.replaceChildren.apply(list, names.map(function (name) {
      var g = groups[name];
      var cards = g.qs.filter(function (q) { return q.type === 'select'; }).map(function (q) {
        var who = g.rows.filter(function (o) { return (o.answers || {})[q.id]; });
        if (!who.length) return null;
        var counts = {}; who.forEach(function (o) { var v = o.answers[q.id]; counts[v] = (counts[v] || 0) + 1; });
        var items = Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; });
        return h('section', { class: 'prof-card' }, [
          h('h3', { text: q.label }), h('p', { class: 'note', text: who.length + ' réponse(s)' }),
          h('div', { class: 'hbars' }, items.map(function (k) {
            var pc = Math.round(100 * counts[k] / who.length);
            return h('div', { class: 'hb sm light' }, [h('span', { class: 'hb-l', text: k }),
              h('span', { class: 'hb-track' }, [h('span', { class: 'hb-fill', style: 'width:' + pc + '%' })]),
              h('b', { class: 'hb-v', text: counts[k] + ' · ' + pc + ' %' })]);
          }))
        ]);
      }).filter(Boolean);
      return h('div', { class: 'prof-group' }, [h('h2', { class: 'prof-title', text: name + ' — ' + g.rows.length + ' inscrit(s)' }),
        cards.length ? h('div', { class: 'prof-grid' }, cards) : h('p', { class: 'note', text: 'Pas de questions à choix pour ce billet.' })]);
    }));
  }

  function exportCsv() {
    var c = cacheRef(); if (!c) return;
    var qs = c.questions;
    var head = ['Nom', 'Téléphone', 'E-mail', 'Billet', 'Quantité', 'Montant HTG', 'Statut', 'Paiement', 'Référence', 'Date'].concat(qs.map(function (q) { return q.label; }), ['Présent', 'Accepte contact BiZ']);
    var lines = [head].concat(c.orders.map(function (o) {
      return [o.buyer_name, o.buyer_phone, o.buyer_email || '', o.ticket_types.name, o.quantity, o.amount_htg, o.status, o.payment_method, o.payment_ref || '', o.created_at]
        .concat(qs.map(function (q) { return (o.answers || {})[q.id] || ''; }), [present(c, o) ? 'oui' : 'non', o.consent_biz ? 'oui' : 'non']);
    }));
    var csv = '\ufeff' + lines.map(function (r) { return r.map(function (v) { v = String(v == null ? '' : v); return /[";\n,]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v; }).join(';'); }).join('\r\n');
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv;charset=utf-8' }));
    a.download = 'participants-' + new Date().toISOString().slice(0, 10) + '.csv';
    document.body.appendChild(a); a.click(); a.remove();
  }
  var cacheRef = function () { return null; };

  function orderCard(o, tickets, refresh) {
    var phone = normPhone(o.buyer_phone);
    var out = h('div', { class: 'oc-actions' });
    var card = h('article', { class: 'oc oc-' + o.status }, [
      h('div', { class: 'oc-main' }, [
        h('b', { class: 'oc-name', text: o.buyer_name }),
        h('span', { text: o.quantity + ' × ' + o.ticket_types.name + ' · ' + money(o.amount_htg) }),
        h('span', { class: 'oc-pay' }, [o.payment_method + ' · Réf. ', h('b', { text: o.payment_ref || '—' })]),
        h('span', { class: 'oc-meta', text: o.buyer_phone + ' · ' + when(o.created_at) }),
        o.reject_reason ? h('span', { class: 'oc-meta', text: 'Motif : ' + o.reject_reason }) : null,
        tickets.length ? h('span', { class: 'oc-meta', text: 'Billets : ' + tickets.map(function (t) { return t.code + (t.checked_in_at ? ' ✓' : ''); }).join(', ') }) : null
      ]), out
    ]);
    if (o.proof_path) out.appendChild(h('button', { class: 'btn btn-ghost-dark', type: 'button', text: 'Voir la preuve', onclick: async function () {
      var s = await sb.storage.from('proofs').createSignedUrl(o.proof_path, 300);
      if (s.data) window.open(s.data.signedUrl, '_blank', 'noopener');
    } }));
    function sendBtn(codes) {
      return h('a', { class: 'btn btn-wa', target: '_blank', rel: 'noopener', href: 'https://wa.me/' + phone + '?text=' + encodeURIComponent(ticketsMessage(o, codes)), text: 'Envoyer les billets sur WhatsApp' });
    }
    if (o.status === 'pending') {
      out.appendChild(h('button', { class: 'btn btn-gold', type: 'button', text: 'Paiement reçu ✓', onclick: async function (e) {
        e.target.disabled = true;
        var r = await sb.rpc('approve_order', { p_order: o.id });
        if (r.error) { alert(r.error.message); e.target.disabled = false; return; }
        out.replaceChildren(sendBtn(r.data.tickets));
        card.className = 'oc oc-paid';
      } }));
      out.appendChild(h('button', { class: 'btn btn-ghost-dark', type: 'button', text: 'Refuser', onclick: async function () {
        var why = prompt('Motif du refus (visible par le client) :', 'Paiement introuvable');
        if (why === null) return;
        var r = await sb.rpc('reject_order', { p_order: o.id, p_reason: why });
        if (r.error) alert(r.error.message); else refresh();
      } }));
    } else if (o.status === 'paid') {
      out.appendChild(sendBtn(tickets.map(function (t) { return t.code; })));
    }
    return card;
  }

  /* ---------- Scanner ---------- */
  async function scanner() {
    if (!(await requireAdmin())) return;
    var res = h('div', { class: 'scan-res', 'aria-live': 'assertive' }, [h('p', { text: 'Scannez un billet…' })]);
    var manual = h('form', { class: 'scan-manual' }, [
      h('label', null, ['Code du billet', h('input', { name: 'code', autocomplete: 'off', autocapitalize: 'characters', maxlength: 20 })]),
      h('button', { class: 'btn btn-navy', type: 'submit', text: 'Vérifier' })
    ]);
    manual.addEventListener('submit', function (e) { e.preventDefault(); check(manual.code.value); manual.code.value = ''; });
    app.replaceChildren(h('a', { class: 'dark-link back', href: '../', text: '← Tableau de bord' }), h('div', { id: 'reader' }), res, manual);
    var busy = false, last = '', lastAt = 0;
    async function check(raw) {
      var code = String(raw || '').trim();
      try { var u = new URL(code); code = u.searchParams.get('c') || code; } catch (_) {}
      code = code.toUpperCase();
      if (!code || busy || (code === last && Date.now() - lastAt < 4000)) return;
      busy = true; last = code; lastAt = Date.now();
      var r = await sb.rpc('check_in', { p_code: code });
      busy = false;
      var d = r.data || { result: 'invalid' };
      var map = { ok: ['ok', 'ENTRÉE VALIDÉE'], already: ['warn', 'DÉJÀ UTILISÉ'], invalid: ['bad', 'BILLET INVALIDE'], other_org: ['bad', 'BILLET D’UN AUTRE ORGANISATEUR'] };
      var m = map[d.result] || map.invalid;
      res.className = 'scan-res ' + m[0];
      res.replaceChildren(h('b', { text: m[1] }),
        d.holder ? h('span', { text: d.holder + ' · ' + d.type }) : h('span', { text: code }),
        d.checked_in_at ? h('span', { text: 'Pointé le ' + when(d.checked_in_at) }) : null);
      if (navigator.vibrate) navigator.vibrate(d.result === 'ok' ? 80 : [60, 60, 60]);
    }
    if (window.Html5Qrcode) {
      var cam = new window.Html5Qrcode('reader');
      cam.start({ facingMode: 'environment' }, { fps: 10, qrbox: { width: 240, height: 240 } }, check, function () {})
        .catch(function () { $('#reader').replaceChildren(h('p', { class: 'note', text: 'Caméra indisponible : utilisez la saisie du code ci-dessous.' })); });
    }
  }

  /* ---------- Base nationale (super-admin BiZ) ---------- */
  async function national() {
    if (!(await requireAdmin())) return;
    if (!ACCESS.superadmin) { app.replaceChildren(h('p', { class: 'note err', text: 'Réservé à l’équipe BiZ Insider.' })); return; }
    var st = await sb.rpc('national_stats');
    if (st.error) { app.replaceChildren(h('p', { class: 'note err', text: st.error.message })); return; }
    var d = st.data;
    var search = h('input', { type: 'search', placeholder: 'Nom, téléphone ou ville…', 'aria-label': 'Rechercher' });
    var onlyC = h('input', { type: 'checkbox' });
    var list = h('div', { class: 'orders' });
    app.replaceChildren(
      h('a', { class: 'dark-link back', href: '../', text: '← Tableau de bord' }),
      h('h1', { class: 'ev-title', text: 'Base nationale des participants' }),
      h('div', { class: 'adm-stats' }, [['Personnes', d.people], ['Contactables (consentement BiZ)', d.contactable], ['Venues à 2 événements ou plus', d.multi_event], ['Clients différents', d.multi_org]].map(function (x) {
        return h('div', null, [h('b', { text: String(x[1]) }), h('span', { text: x[0] })]);
      })),
      h('p', { class: 'note', text: 'Par client : ' + d.by_org.map(function (o) { return o.name + ' (' + o.people + ')'; }).join(' · ') }),
      h('div', { class: 'adm-bar' }, [search, h('label', { class: 'consent' }, [onlyC, h('span', { text: 'Seulement les contactables' })])]),
      list);
    async function load() {
      var q = sb.from('people').select('full_name, phone, email, city, consent_biz, first_seen, last_seen, orders(event_id)').order('last_seen', { ascending: false }).limit(200);
      var term = search.value.trim();
      if (term) q = q.or('full_name.ilike.%' + term.replace(/[%,()]/g, '') + '%,phone.ilike.%' + term.replace(/\D/g, '') + '%,city.ilike.%' + term.replace(/[%,()]/g, '') + '%');
      if (onlyC.checked) q = q.eq('consent_biz', true);
      var r = await q;
      if (r.error) { list.replaceChildren(h('p', { class: 'note err', text: r.error.message })); return; }
      if (!r.data.length) { list.replaceChildren(h('p', { class: 'note', text: 'Aucune personne.' })); return; }
      list.replaceChildren.apply(list, r.data.map(function (p) {
        var nEv = new Set((p.orders || []).map(function (o) { return o.event_id; })).size;
        return h('article', { class: 'oc ' + (p.consent_biz ? 'oc-paid' : 'oc-rejected') }, [h('div', { class: 'oc-main' }, [
          h('b', { class: 'oc-name', text: p.full_name }),
          h('span', { text: p.phone + (p.email ? ' · ' + p.email : '') + (p.city ? ' · ' + p.city : '') }),
          h('span', { class: 'oc-meta', text: nEv + ' événement(s) · vu le ' + when(p.last_seen) + ' · ' + (p.consent_biz ? 'contactable' : 'ne pas contacter') })
        ])]);
      }));
    }
    var tmr; search.addEventListener('input', function () { clearTimeout(tmr); tmr = setTimeout(load, 300); });
    onlyC.addEventListener('change', load);
    load();
  }

  ({ admin: dashboard, scan: scanner, people: national }[PAGE] || function () {})();
})();
