// Minimal vanilla JS to replace Alpine/Tailwind-driven mobile menu behavior
(function(){
  const button = document.querySelector('[data-testid="mobile-menu-button"]');
  const menu = document.getElementById('mobile-menu');
  if(!button || !menu) return;

  function openMenu(){
    button.classList.add('is-open');
    menu.classList.add('open');
    button.setAttribute('aria-expanded','true');
    // prevent body scroll
    document.body.style.overflow = 'hidden';
  }
  function closeMenu(){
    button.classList.remove('is-open');
    menu.classList.remove('open');
    button.setAttribute('aria-expanded','false');
    document.body.style.overflow = '';
  }

  button.addEventListener('click', ()=>{
    const expanded = button.getAttribute('aria-expanded') === 'true';
    if(expanded) closeMenu(); else openMenu();
  });

  // Close menu on escape or clicking outside
  document.addEventListener('keydown', (e)=>{
    if(e.key === 'Escape' && menu.classList.contains('open')) closeMenu();
  });

  document.addEventListener('click', (e)=>{
    if(!menu.classList.contains('open')) return;
    if(e.target.closest('#mobile-menu')) return; // inside menu
    if(e.target.closest('[data-testid="mobile-menu-button"]')) return; // the button
    closeMenu();
  });
})();
