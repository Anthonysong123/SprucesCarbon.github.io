(function () {
  "use strict";

  var PUBLIC_EMAIL_DOMAINS = [
    "gmail.com",
    "googlemail.com",
    "yahoo.com",
    "yahoo.co.uk",
    "hotmail.com",
    "outlook.com",
    "live.com",
    "msn.com",
    "icloud.com",
    "me.com",
    "mac.com",
    "aol.com",
    "proton.me",
    "protonmail.com",
    "qq.com",
    "163.com",
    "126.com",
    "sina.com",
    "sohu.com",
    "foxmail.com",
    "ymail.com",
    "mail.com",
  ];

  function isCorporateEmail(value) {
    var parts = value.trim().toLowerCase().split("@");
    if (parts.length !== 2 || !parts[0] || !parts[1]) return false;
    return PUBLIC_EMAIL_DOMAINS.indexOf(parts[1]) === -1;
  }

  function showFormError(form, message) {
    var err = form.querySelector(".form-error");
    if (err) {
      err.textContent = message;
      err.classList.add("is-visible");
    }
  }

  function clearFormError(form) {
    var err = form.querySelector(".form-error");
    if (err) err.classList.remove("is-visible");
  }

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
      link.addEventListener("click", function (e) {
        if (link.hasAttribute("data-nav-portal")) {
          e.preventDefault();
          window.alert(
            "System Upgrading / Access Restricted to Authorized Auditors Only"
          );
          return;
        }
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
      var name = form.querySelector('[name="name"]');
      var email = form.querySelector('[name="email"]');
      var org = form.querySelector('[name="organisation"]');
      var linkedin = form.querySelector('[name="linkedin"]');
      var consent = form.querySelector('[name="consent"]');

      if (!name.value.trim() || !org.value.trim() || !email.value.trim() || !linkedin.value.trim() || !consent.checked) {
        showFormError(
          form,
          "Please complete all required fields and accept the privacy notice."
        );
        return;
      }

      if (!isCorporateEmail(email.value)) {
        showFormError(form, "Please use your official corporate email address.");
        return;
      }

      clearFormError(form);

      var type = form.querySelector('[name="enquiry"]');
      var msg = form.querySelector('[name="message"]');
      var subject = "ESG/D-MRV technical presentation request";
      var body = [
        "Name: " + name.value.trim(),
        "Company: " + org.value.trim(),
        "Email: " + email.value.trim(),
        "LinkedIn: " + linkedin.value.trim(),
        "Enquiry type: " + (type ? type.value : ""),
        "",
        msg ? msg.value.trim() : "",
      ].join("\n");

      window.location.href =
        "mailto:Info@sprucesglobal.com?subject=" +
        encodeURIComponent(subject) +
        "&body=" +
        encodeURIComponent(body);
    });
  }
})();
