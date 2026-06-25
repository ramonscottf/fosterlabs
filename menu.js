/* Foster Labs — Floating Pill Menu (wicko pill, ported from hiresbigh, namespaced #fl-pill) */
(function () {
  if (document.getElementById('fl-pill')) return;

  /* ---- Pages shown in the menu. Edit this list to add/remove. ---- */
  var PAGES = [
    { href: '/',            label: 'Home' },
    { href: '/summershows', label: 'Summer Shows' },
    { href: '/mower',       label: 'Robot Mower' },
    { href: '/math',        label: 'Math Quiz' },
    { href: '/spelling',    label: 'Spelling' },
    { href: '/gin',         label: 'Vicious Gin' }
    /* Held back from the public menu — uncomment to surface:
    { href: '/warroom',    label: 'War Room' },     // covert Hires — keep private
    { href: '/finance',    label: 'Finance' },
    { href: '/health',     label: 'Health' },
    { href: '/intern',     label: 'Intern' },
    { href: '/command',    label: 'Command' },
    { href: '/notes',      label: 'Notes' },
    { href: '/todo.html',  label: 'Tasks' },
    { href: '/gala-items', label: 'Gala Items' },
    { href: '/help-setup', label: 'Helpline' },
    { href: '/jack.html',  label: 'Jack' },
    */
  ];

  var css = `
  #fl-pill{position:fixed;top:18px;left:50%;transform:translate(-50%,0);z-index:99999;
    width:calc(100% - 36px);max-width:940px;background:rgba(253,246,236,.92);
    backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-radius:50px;
    border:1px solid rgba(180,160,130,.18);box-shadow:0 8px 32px rgba(60,45,25,.16);
    transition:top .4s ease,box-shadow .4s ease,background .4s ease;
    animation:flPillDown .7s cubic-bezier(.2,.8,.2,1) both;
    font-family:system-ui,-apple-system,"Segoe UI",sans-serif}
  @keyframes flPillDown{from{opacity:0;transform:translate(-50%,-16px)}to{opacity:1;transform:translate(-50%,0)}}
  #fl-pill.scrolled{top:10px;background:rgba(253,246,236,.98);box-shadow:0 12px 40px rgba(60,45,25,.22)}
  #fl-pill .fl-inner{display:flex;align-items:center;justify-content:space-between;padding:9px 12px 9px 18px}
  #fl-pill .fl-brand{display:flex;align-items:center;gap:10px;text-decoration:none}
  #fl-pill .fl-brand-icon{height:32px;width:32px;flex-shrink:0}
  #fl-pill .fl-brand-icon img{height:100%;width:100%;object-fit:contain;border-radius:8px}
  #fl-pill .fl-brand-tx{display:flex;flex-direction:column;line-height:1.05}
  #fl-pill .fl-brand-main{font-family:Georgia,"Times New Roman",serif;font-weight:700;
    font-size:16px;color:#2b2b2b;letter-spacing:-.2px}
  #fl-pill .fl-brand-sub{font-size:8.5px;font-weight:600;letter-spacing:2px;
    text-transform:uppercase;color:rgba(43,43,43,.42);margin-top:1px}
  #fl-pill .fl-links{display:flex;gap:24px;align-items:center;list-style:none;margin:0;padding:0}
  #fl-pill .fl-links a{font-size:12px;font-weight:600;color:rgba(43,43,43,.62);letter-spacing:.6px;
    text-transform:uppercase;text-decoration:none;position:relative;transition:color .25s;white-space:nowrap}
  #fl-pill .fl-links a::after{content:'';position:absolute;bottom:-4px;left:0;width:0;height:2px;
    background:#c0392b;transition:width .25s;border-radius:1px}
  #fl-pill .fl-links a:hover,#fl-pill .fl-links a.active{color:#1b1b1b}
  #fl-pill .fl-links a:hover::after,#fl-pill .fl-links a.active::after{width:100%}
  #fl-pill .fl-toggle{display:none;background:none;border:none;cursor:pointer;padding:8px;position:relative;z-index:2}
  #fl-pill .fl-toggle span{display:block;width:22px;height:2px;background:#2b2b2b;margin:5px 0;
    transition:all .3s;border-radius:2px}
  #fl-pill .fl-toggle.open span:nth-child(1){transform:rotate(45deg) translate(5px,5px)}
  #fl-pill .fl-toggle.open span:nth-child(2){opacity:0}
  #fl-pill .fl-toggle.open span:nth-child(3){transform:rotate(-45deg) translate(5px,-5px)}
  @media(max-width:820px){
    #fl-pill{width:calc(100% - 24px);border-radius:16px;overflow:visible}
    #fl-pill .fl-inner{padding:8px 10px 8px 14px}
    #fl-pill .fl-toggle{display:block}
    #fl-pill .fl-links{position:absolute;top:calc(100% + 10px);left:0;right:0;flex-direction:column;
      align-items:stretch;gap:0;background:rgba(253,246,236,.99);backdrop-filter:blur(20px);
      -webkit-backdrop-filter:blur(20px);border-radius:18px;border:1px solid rgba(180,160,130,.2);
      box-shadow:0 16px 44px rgba(60,45,25,.2);padding:8px;opacity:0;visibility:hidden;
      transform:translateY(-8px);transition:opacity .25s,transform .25s,visibility .25s;max-height:72vh;overflow:auto}
    #fl-pill .fl-links.open{opacity:1;visibility:visible;transform:translateY(0)}
    #fl-pill .fl-links li{border-bottom:1px solid rgba(180,160,130,.12)}
    #fl-pill .fl-links li:last-child{border-bottom:none}
    #fl-pill .fl-links a{display:block;padding:13px 16px;font-size:13px}
    #fl-pill .fl-links a::after{display:none}
    #fl-pill .fl-links a.active{color:#c0392b}
  }
  @media(prefers-reduced-motion:reduce){#fl-pill{animation:none}#fl-pill *{transition:none !important}}
  `;

  var style = document.createElement('style');
  style.textContent = css;
  document.head.appendChild(style);

  function norm(p){ p = p.replace(/index\.html$/, '').replace(/\/+$/, ''); return p === '' ? '/' : p; }
  var cur = norm(location.pathname);

  var lis = PAGES.map(function (p) {
    var active = norm(p.href) === cur ? ' class="active"' : '';
    return '<li><a href="' + p.href + '"' + active + '>' + p.label + '</a></li>';
  }).join('');

  var nav = document.createElement('nav');
  nav.id = 'fl-pill';
  nav.setAttribute('aria-label', 'Site');
  nav.innerHTML =
    '<div class="fl-inner">' +
      '<a class="fl-brand" href="/">' +
        '<span class="fl-brand-icon"><img src="/logo-mark.png" alt="Foster Labs"></span>' +
        '<span class="fl-brand-tx"><span class="fl-brand-main">Foster Labs</span>' +
        '<span class="fl-brand-sub">Skippy</span></span>' +
      '</a>' +
      '<ul class="fl-links" id="fl-links">' + lis + '</ul>' +
      '<button class="fl-toggle" id="fl-toggle" aria-label="Toggle menu" aria-expanded="false">' +
        '<span></span><span></span><span></span></button>' +
    '</div>';

  function mount(){
    document.body.appendChild(nav);
    // clear the floating pill on pages that start their content at the very top
    try {
      var cs = getComputedStyle(document.body);
      if (parseFloat(cs.paddingTop) < 76) document.body.style.paddingTop = '84px';
    } catch (e) {}
    document.documentElement.style.scrollPaddingTop = '92px';

    var toggle = document.getElementById('fl-toggle');
    var links = document.getElementById('fl-links');
    function open(){ toggle.classList.add('open'); links.classList.add('open'); toggle.setAttribute('aria-expanded','true'); }
    function close(){ toggle.classList.remove('open'); links.classList.remove('open'); toggle.setAttribute('aria-expanded','false'); }
    toggle.addEventListener('click', function (e) { e.stopPropagation(); links.classList.contains('open') ? close() : open(); });
    document.addEventListener('click', function (e) {
      if (links.classList.contains('open') && !links.contains(e.target) && !toggle.contains(e.target)) close();
    });
    links.querySelectorAll('a').forEach(function (a) { a.addEventListener('click', close); });
    window.addEventListener('scroll', function () { nav.classList.toggle('scrolled', window.scrollY > 60); }, { passive: true });
  }

  if (document.body) mount();
  else document.addEventListener('DOMContentLoaded', mount);
})();
