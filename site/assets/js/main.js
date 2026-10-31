// Asdale Dynamics, LLC - AI Password Manager Guide
// Simple interactivity for the static HTML site

document.addEventListener('DOMContentLoaded', function() {
  // Print button
  const printBtn = document.getElementById('print-btn');
  if (printBtn) {
    printBtn.addEventListener('click', function() {
      window.print();
    });
  }

  // Checklist persistence (localStorage)
  const checkboxes = document.querySelectorAll('.checklist-item input[type="checkbox"]');
  checkboxes.forEach(function(cb) {
    const key = 'checklist-' + cb.id;
    const saved = localStorage.getItem(key);
    if (saved === 'true') {
      cb.checked = true;
    }
    cb.addEventListener('change', function() {
      localStorage.setItem(key, cb.checked);
    });
  });
});