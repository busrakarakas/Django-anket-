document.addEventListener('DOMContentLoaded', () => {
  // Oy formu submit
  document.querySelectorAll('.vp-vote-form').forEach(form => {
    form.addEventListener('submit', e => {
      const checked = form.querySelector('input:checked');
      const btn = form.querySelector('[type=submit]');
      if (!checked) {
        e.preventDefault();
        btn.textContent = '⚠️ Bir seçenek seçin!';
        btn.classList.replace('btn-primary','btn-warning');
        setTimeout(() => { btn.innerHTML = '<i class="bi bi-send me-2"></i>Oyumu Gönder'; btn.classList.replace('btn-warning','btn-primary'); }, 2000);
        return;
      }
      btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Gönderiliyor...';
      btn.disabled = true;
    });
  });

  // Mesaj otomatik kapat
  setTimeout(() => {
    document.querySelectorAll('.alert').forEach(a => {
      try { bootstrap.Alert.getOrCreateInstance(a).close(); } catch(e){}
    });
  }, 6000);

  // Sayı animasyonu
  document.querySelectorAll('.vp-stat-num').forEach(el => {
    const target = parseInt(el.textContent) || 0;
    if (target === 0) return;
    let n = 0;
    const step = target / 40;
    const timer = setInterval(() => {
      n = Math.min(n + step, target);
      el.textContent = Math.floor(n);
      if (n >= target) clearInterval(timer);
    }, 25);
  });

  console.log('🗳️ AnketApp Hazır!');
});
