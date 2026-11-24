/* BiZ Media — Billetterie (paiement MonCash / NatCash vérifié manuellement) */
(function () {
  'use strict';
  var SUPABASE_URL = 'https://sljzkbcpkecpvvpzskxa.supabase.co';
  var SUPABASE_KEY = 'sb_publishable_SSQwmuNgdfpoK-RJdBD0pw_TWgG-uA4';
  var BIZ_WHATSAPP = '50949012257';

  var sb = window.supabase.createClient(SUPABASE_URL, SUPABASE_KEY);
  var body = document.body;
  var ROOT = body.getAttribute('data-root') || '';
  var LANG = (document.documentElement.lang || 'fr').slice(0, 2);
  var EN = LANG === 'en';

  var L = {
    fr: {
      loading: 'Chargement…', noEvents: 'Aucun événement en vente pour le moment.', buy: 'Acheter un billet',
      seatsLeft: function (n) { return n > 0 ? n + ' place' + (n > 1 ? 's' : '') + ' restante' + (n > 1 ? 's' : '') : 'Complet'; },
      chooseType: 'Type de billet', qty: 'Nombre de billets', total: 'Total à payer',
      payTitle: 'Comment payer', payStep1: function (amt, m, num) { return 'Envoyez ' + amt + ' par ' + m + ' au ' + num + '.'; },
      payStep2: 'Notez le numéro de transaction reçu par SMS.', payStep3: 'Remplissez le formulaire ci-dessous. Nous vérifions votre paiement et vous envoyons vos billets sur WhatsApp.',
      name: 'Nom complet', phone: 'Numéro WhatsApp', method: 'Paiement envoyé par', ref: 'Numéro de transaction', proof: 'Capture d’écran du paiement (facultatif)',
      submit: 'Envoyer ma commande', sending: 'Envoi en cours…', notFound: 'Événement introuvable.', back: '← Tous les événements',
      errGeneric: 'Une erreur est survenue. Réessayez ou écrivez-nous sur WhatsApp.', soldOut: 'Complet',
      orderPending: 'Commande reçue — paiement en cours de vérification',
      orderPendingText: 'Nous vérifions votre paiement. Vos billets apparaîtront sur cette page et vous seront envoyés sur WhatsApp. Gardez ce lien.',
      orderPaid: 'Paiement confirmé — voici vos billets', orderRejected: 'Commande refusée', reason: 'Motif : ',
      contact: 'Écrire à BiZ sur WhatsApp', refresh: 'Actualiser', openTicket: 'Ouvrir le billet', orderNotFound: 'Commande introuvable.',
      ticketUsed: 'Billet déjà utilisé le ', ticketValid: 'Billet valide — présentez ce QR code à l’entrée', ticketNotFound: 'Billet introuvable.',
      holder: 'Titulaire', type: 'Type', date: 'Date', venue: 'Lieu', code: 'Code', amount: 'Montant',
      waOrder: function (o) { return 'Bonjour BiZ Media, je viens de commander ' + o + '. Merci de vérifier mon paiement.'; },
      htg: ' HTG'
    },
    en: {
      loading: 'Loading…', noEvents: 'No events on sale right now.', buy: 'Buy a ticket',
      seatsLeft: function (n) { return n > 0 ? n + ' seat' + (n > 1 ? 's' : '') + ' left' : 'Sold out'; },
      chooseType: 'Ticket type', qty: 'Number of tickets', total: 'Total to pay',
      payTitle: 'How to pay', payStep1: function (amt, m, num) { return 'Send ' + amt + ' via ' + m + ' to ' + num + '.'; },
      payStep2: 'Note the transaction number you receive by SMS.', payStep3: 'Fill in the form below. We check your payment and send your tickets on WhatsApp.',
      name: 'Full name', phone: 'WhatsApp number', method: 'Payment sent with', ref: 'Transaction number', proof: 'Payment screenshot (optional)',
      submit: 'Send my order', sending: 'Sending…', notFound: 'Event not found.', back: '← All events',
      errGeneric: 'Something went wrong. Try again or message us on WhatsApp.', soldOut: 'Sold out',
      orderPending: 'Order received — payment being checked',
      orderPendingText: 'We are checking your payment. Your tickets will appear on this page and be sent to you on WhatsApp. Keep this link.',
      orderPaid: 'Payment confirmed — here are your tickets', orderRejected: 'Order declined', reason: 'Reason: ',
      contact: 'Message BiZ on WhatsApp', refresh: 'Refresh', openTicket: 'Open ticket', orderNotFound: 'Order not found.',
      ticketUsed: 'Ticket already used on ', ticketValid: 'Valid ticket — show this QR code at the door', ticketNotFound: 'Ticket not found.',
      holder: 'Holder', type: 'Type', date: 'Date', venue: 'Venue', code: 'Code', amount: 'Amount',
      waOrder: function (o) { return 'Hello BiZ Media, I just ordered ' + o + '. Please check my payment.'; },
      htg: ' HTG'
    }
  }[EN ? 'en' : 'fr'];

  /* ---------- utilitaires ---------- */
  function $(sel, el) { return (el || document).querySelector(sel); }
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
  function money(n) { return new Intl.NumberFormat(EN ? 'en-US' : 'fr-FR').format(n) + L.htg; }
  function when(d) {
    return new Intl.DateTimeFormat(EN ? 'en-US' : 'fr-FR', { dateStyle: 'full', timeStyle: 'short', timeZone: 'America/Port-au-Prince' }).format(new Date(d));
  }
  function param(n) { return new URLSearchParams(location.search).get(n); }
  function url(path) { return new URL(ROOT + path, location.href).href; }
  function waLink(phone, text) { return 'https://wa.me/' + phone + '?text=' + encodeURIComponent(text); }
  function normPhone(p) { var d = String(p || '').replace(/\D/g, ''); if (d.length === 8) d = '509' + d; return d; }
  function qr(text, size) {
    var q = window.qrcode(0, 'M'); q.addData(text); q.make();
    var wrap = h('div', { class: 'qr', role: 'img', 'aria-label': 'QR code' });
    wrap.innerHTML = q.createSvgTag({ cellSize: Math.max(2, Math.floor(size / (q.getModuleCount() + 8))), margin: 4, scalable: true });
    return wrap;
  }
  function msg(el, text, kind) { el.replaceChildren(h('p', { class: 'note ' + (kind || ''), text: text })); }
  function errText(e) { var m = (e && (e.message || e.error_description)) || ''; return /places|Quantité|introuvable|invalide|seats/i.test(m) ? m : L.errGeneric; }

  /* ---------- Liste + achat ---------- */
  async function pageShop() {
    var app = $('#app'); msg(app, L.loading);
    var slug = param('e');
    var q = sb.from('events').select('id, slug, title, description, venue, starts_at, payment_number, payment_methods, ticket_types(id, name, description, price_htg, sort)').eq('is_published', true).order('starts_at');
    var res = slug ? await q.eq('slug', slug) : await q;
    if (res.error) return msg(app, L.errGeneric, 'err');
    if (!slug) {
      if (!res.data.length) return msg(app, L.noEvents);
      app.replaceChildren(h('div', { class: 'ev-list' }, res.data.map(function (ev) {
        var min = Math.min.apply(null, ev.ticket_types.map(function (t) { return t.price_htg; }));
        return h('article', { class: 'ev-card' }, [
          h('span', { class: 'eyebrow', text: when(ev.starts_at) }),
          h('h2', { text: ev.title }), h('p', { class: 'lead', text: ev.venue || '' }),
          h('p', { class: 'ev-price', text: (EN ? 'From ' : 'À partir de ') + money(min) }),
          h('a', { class: 'btn btn-gold', href: '?e=' + encodeURIComponent(ev.slug), text: L.buy })
        ]);
      })));
      return;
    }
    var ev = res.data[0];
    if (!ev) return msg(app, L.notFound, 'err');
    document.title = ev.title + ' — BiZ Media';
    var av = await sb.rpc('event_availability', { p_slug: ev.slug });
    var left = {}; (av.data || []).forEach(function (r) { left[r.ticket_type_id] = r.seats_left; });
    var types = ev.ticket_types.slice().sort(function (a, b) { return a.sort - b.sort; });
    var methods = ev.payment_methods.split(/\s*,\s*/);

    var totalEl = h('b', { class: 'total' });
    var step1 = h('li');
    var qty = h('select', { name: 'qty', id: 'qty' }, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(function (n) { return h('option', { value: n, text: String(n) }); }));
    var typeBox = h('div', { class: 'tt-list', role: 'radiogroup', 'aria-label': L.chooseType }, types.map(function (t, i) {
      var n = left[t.id] || 0;
      return h('label', { class: 'tt' + (n <= 0 ? ' tt-out' : '') }, [
        h('input', { type: 'radio', name: 'tt', value: t.id, 'data-price': t.price_htg, checked: i === 0 && n > 0, disabled: n <= 0 }),
        h('span', { class: 'tt-main' }, [h('b', { text: t.name }), h('small', { text: t.description || '' })]),
        h('span', { class: 'tt-side' }, [h('b', { text: money(t.price_htg) }), h('small', { text: L.seatsLeft(n) })])
      ]);
    }));
    if (!$('input[name=tt]:checked', typeBox)) { var first = $('input[name=tt]:not([disabled])', typeBox); if (first) first.checked = true; }
    function update() {
      var sel = $('input[name=tt]:checked', typeBox);
      var amt = sel ? Number(sel.getAttribute('data-price')) * Number(qty.value) : 0;
      totalEl.textContent = money(amt);
      step1.textContent = L.payStep1(money(amt), methods.join(' / '), ev.payment_number);
    }
    typeBox.addEventListener('change', update); qty.addEventListener('change', update);

    var status = h('div', { 'aria-live': 'polite' });
    var form = h('form', { class: 'buy-form' }, [
      h('div', { class: 'row' }, [
        h('label', null, [L.name, h('input', { name: 'name', required: true, autocomplete: 'name', minlength: 2, maxlength: 120 })]),
        h('label', null, [L.phone, h('input', { name: 'phone', type: 'tel', required: true, autocomplete: 'tel', placeholder: '+509', minlength: 8, maxlength: 20 })])
      ]),
      h('div', { class: 'row' }, [
        h('label', null, [L.method, h('select', { name: 'method' }, methods.map(function (m) { return h('option', { value: m, text: m }); }))]),
        h('label', null, [L.ref, h('input', { name: 'ref', required: true, maxlength: 80 })])
      ]),
      h('label', null, [L.proof, h('input', { name: 'proof', type: 'file', accept: 'image/*' })]),
      h('button', { class: 'btn btn-gold', type: 'submit', text: L.submit }), status
    ]);
    form.addEventListener('submit', async function (e) {
      e.preventDefault();
      var btn = $('button', form); btn.disabled = true; btn.textContent = L.sending;
      try {
        var sel = $('input[name=tt]:checked', typeBox); if (!sel) throw new Error(L.soldOut);
        var proofPath = null, file = form.proof.files[0];
        if (file) {
          if (file.size > 5 * 1024 * 1024) throw new Error('Image > 5 Mo');
          var ext = (file.name.split('.').pop() || 'jpg').toLowerCase().replace(/[^a-z0-9]/g, '').slice(0, 5) || 'jpg';
          proofPath = crypto.randomUUID() + '/preuve.' + ext;
          var up = await sb.storage.from('proofs').upload(proofPath, file, { contentType: file.type || 'image/jpeg' });
          if (up.error) throw up.error;
        }
        var r = await sb.rpc('create_order', {
          p_ticket_type: sel.value, p_quantity: Number(qty.value), p_name: form.name.value, p_phone: form.phone.value,
          p_method: form.method.value, p_ref: form.ref.value, p_proof_path: proofPath
        });
        if (r.error) throw r.error;
        location.href = url((EN ? 'en/tickets/order/' : 'billetterie/commande/') + '?t=' + r.data);
      } catch (err) {
        msg(status, errText(err), 'err'); btn.disabled = false; btn.textContent = L.submit;
      }
    });

    update();
    app.replaceChildren(
      h('a', { class: 'dark-link back', href: './', text: L.back }),
      h('div', { class: 'shop' }, [
        h('div', { class: 'shop-info' }, [
          h('span', { class: 'eyebrow', text: when(ev.starts_at) }),
          h('h1', { class: 'ev-title', text: ev.title }),
          h('p', { class: 'lead', text: ev.venue || '' }),
          ev.description ? h('p', { text: ev.description }) : null
        ]),
        h('div', { class: 'shop-buy' }, [
          h('h2', { text: L.chooseType }), typeBox,
          h('label', { class: 'qty' }, [L.qty, qty]),
          h('p', { class: 'total-line' }, [L.total + ' : ', totalEl]),
          h('div', { class: 'pay' }, [h('h3', { text: L.payTitle }), h('ol', null, [step1, h('li', { text: L.payStep2 }), h('li', { text: L.payStep3 })])]),
          form
        ])
      ])
    );
  }

  /* ---------- Suivi de commande ---------- */
  async function pageOrder() {
    var app = $('#app'); msg(app, L.loading);
    var t = param('t');
    var r = t ? await sb.rpc('get_order', { p_token: t }) : { data: null };
    var o = r.data;
    if (!o) return msg(app, L.orderNotFound, 'err');
    var label = o.quantity + ' × ' + o.ticket_type + ' — ' + o.event.title;
    var kids = [
      h('span', { class: 'eyebrow', text: o.event.title }),
      h('h1', { class: 'ev-title', text: o.status === 'paid' ? L.orderPaid : o.status === 'rejected' ? L.orderRejected : L.orderPending }),
      h('dl', { class: 'meta' }, [
        h('div', null, [h('dt', { text: L.holder }), h('dd', { text: o.buyer_name })]),
        h('div', null, [h('dt', { text: L.type }), h('dd', { text: o.quantity + ' × ' + o.ticket_type })]),
        h('div', null, [h('dt', { text: L.amount }), h('dd', { text: money(o.amount_htg) })]),
        h('div', null, [h('dt', { text: L.date }), h('dd', { text: when(o.event.starts_at) })])
      ])
    ];
    if (o.status === 'pending') {
      kids.push(h('p', { class: 'lead', text: L.orderPendingText }));
      kids.push(h('div', { class: 'actions' }, [
        h('a', { class: 'btn btn-gold', href: waLink(BIZ_WHATSAPP, L.waOrder(label) + '\n' + location.href), target: '_blank', rel: 'noopener', text: L.contact }),
        h('button', { class: 'btn btn-navy', type: 'button', onclick: function () { location.reload(); }, text: L.refresh })
      ]));
    } else if (o.status === 'rejected') {
      if (o.reject_reason) kids.push(h('p', { class: 'lead', text: L.reason + o.reject_reason }));
      kids.push(h('a', { class: 'btn btn-gold', href: waLink(BIZ_WHATSAPP, L.waOrder(label)), target: '_blank', rel: 'noopener', text: L.contact }));
    } else {
      kids.push(h('div', { class: 'tk-grid' }, o.tickets.map(function (code) {
        var link = url((EN ? 'en/ticket/' : 'billet/') + '?c=' + code);
        return h('a', { class: 'tk-mini', href: link }, [qr(link, 160), h('b', { text: code }), h('span', { text: L.openTicket + ' →' })]);
      })));
    }
    app.replaceChildren(h('div', { class: 'panel' }, kids));
  }

  /* ---------- Billet ---------- */
  async function pageTicket() {
    var app = $('#app'); msg(app, L.loading);
    var c = (param('c') || '').toUpperCase();
    var r = c ? await sb.rpc('get_ticket', { p_code: c }) : { data: null };
    var t = r.data;
    if (!t) return msg(app, L.ticketNotFound, 'err');
    app.replaceChildren(h('article', { class: 'ticket' }, [
      h('div', { class: 'tk-head' }, [
        h('span', { class: 'biz sm', 'aria-hidden': 'true' }, [h('span', { text: 'B' }), h('span', { class: 'i' }, [h('span', { class: 'dot' }), h('span', { class: 'stem' })]), h('span', { text: 'Z' })]),
        h('span', { class: 'tk-type', text: t.ticket_type })
      ]),
      h('h1', { text: t.event.title }),
      h('dl', { class: 'meta' }, [
        h('div', null, [h('dt', { text: L.date }), h('dd', { text: when(t.event.starts_at) })]),
        h('div', null, [h('dt', { text: L.venue }), h('dd', { text: t.event.venue || '' })]),
        h('div', null, [h('dt', { text: L.holder }), h('dd', { text: t.holder })])
      ]),
      qr(location.href, 260),
      h('p', { class: 'tk-code' }, [L.code + ' : ', h('b', { text: t.code })]),
      h('p', { class: 'tk-state ' + (t.checked_in_at ? 'used' : 'ok'), text: t.checked_in_at ? L.ticketUsed + when(t.checked_in_at) : L.ticketValid })
    ]));
  }

  var page = body.getAttribute('data-page');
  ({ shop: pageShop, order: pageOrder, ticket: pageTicket }[page] || function () {})();
})();
