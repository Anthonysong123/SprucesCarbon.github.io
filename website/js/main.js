(function () {
  "use strict";

  var page = document.body.getAttribute("data-page");
  if (page) {
    document.querySelectorAll('.site-nav a[data-nav="' + page + '"]').forEach(function (a) {
      a.classList.add("is-active");
    });
  }

  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".site-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var open = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });

    nav.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        nav.classList.remove("is-open");
        toggle.setAttribute("aria-expanded", "false");
      });
    });
  }

  document.querySelectorAll(".figure img").forEach(function (img) {
    function markPlaceholder() {
      var figure = img.closest(".figure");
      if (figure) figure.classList.add("has-placeholder");
    }
    if (img.complete && img.naturalWidth === 0) markPlaceholder();
    img.addEventListener("error", markPlaceholder);
  });

  var form = document.getElementById("contact-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var err = form.querySelector(".form-error");
      var name = form.querySelector('[name="name"]');
      var email = form.querySelector('[name="email"]');
      var consent = form.querySelector('[name="consent"]');

      if (!name.value.trim() || !email.value.trim() || !consent.checked) {
        if (err) {
          err.textContent =
            "Please enter your name and email, and accept the privacy notice.";
          err.classList.add("is-visible");
        }
        return;
      }
      if (err) err.classList.remove("is-visible");

      var type = form.querySelector('[name="enquiry"]');
      var org = form.querySelector('[name="organisation"]');
      var msg = form.querySelector('[name="message"]');
      var subject =
        "Spruces enquiry: " + (type ? type.value : "General");
      var body = [
        "Name: " + name.value.trim(),
        "Organisation: " + (org ? org.value.trim() : ""),
        "Email: " + email.value.trim(),
        "Enquiry type: " + (type ? type.value : ""),
        "",
        (msg ? msg.value.trim() : ""),
      ].join("\n");

      window.location.href =
        "mailto:Info@sprucesglobal.com?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(body);
    });
  }
})();
