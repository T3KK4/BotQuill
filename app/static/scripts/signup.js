/* ==================================================
   SIGNUP PAGE SCRIPT
================================================== */

document.addEventListener("DOMContentLoaded", () => {

  /* --------------------
     Elements
  -------------------- */

  const signupForm = document.querySelector(
    'form[action="/signup"]'
  );

  const password = document.querySelector("#password");
  const confirmPassword = document.querySelector("#confirm-password");
  const submitButton = signupForm?.querySelector('button[type="submit"]');


  /* --------------------
     Password Comparison
  -------------------- */

  function passwordsMatch() {
    return password.value === confirmPassword.value;
  }


  /* --------------------
     Password Validation
  -------------------- */

  function validatePasswords() {

    if (password.value !== confirmPassword.value) {

      confirmPassword.setCustomValidity(
        "Passwords do not match."
      );

      return false;
    }

    confirmPassword.setCustomValidity("");

    return true;
  }


  /* --------------------
     Live Password Check
  -------------------- */

  confirmPassword.addEventListener("input", () => {
    validatePasswords();
  });

  password.addEventListener("input", () => {
    if (confirmPassword.value !== "") {
      validatePasswords();
    }
  });


  /* --------------------
     Submit Animation
  -------------------- */

  signupForm.addEventListener("submit", (event) => {

    /* Validate passwords first */
    if (!validatePasswords()) {
      event.preventDefault();
      confirmPassword.reportValidity();
      return;
    }

    /*
      Prevent multiple clicks while the
      form is being submitted.
    */
    submitButton.disabled = true;

    submitButton.dataset.originalText =
      submitButton.textContent;

    submitButton.textContent = "Creating Account...";

    submitButton.style.opacity = "0.7";
    submitButton.style.cursor = "wait";
  });


  /* --------------------
     Button Hover Animation
  -------------------- */

  submitButton.addEventListener("mouseenter", () => {

    if (!submitButton.disabled) {
      submitButton.style.transform = "translateY(-2px)";
    }

  });


  submitButton.addEventListener("mouseleave", () => {

    if (!submitButton.disabled) {
      submitButton.style.transform = "translateY(0)";
    }

  });

});