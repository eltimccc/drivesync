document.addEventListener('DOMContentLoaded', function() {
  var navbarToggler = document.querySelector('.navbar-toggler');
  var navbarCollapse = document.querySelector('.navbar-collapse');

  document.addEventListener('click', function(event) {
    if (navbarCollapse.classList.contains('show') && !navbarToggler.contains(event.target) && !navbarCollapse.contains(event.target)) {
      var bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
      if (bsCollapse) {
        bsCollapse.hide();
        navbarToggler.setAttribute('aria-expanded', 'false');
      }
    }
  });

  navbarToggler.addEventListener('click', function(event) {
    var bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
    if (bsCollapse) {
      bsCollapse.toggle();
      var expanded = navbarToggler.getAttribute('aria-expanded') === 'true' || false;
      navbarToggler.setAttribute('aria-expanded', String(!expanded));
    }
  });
});