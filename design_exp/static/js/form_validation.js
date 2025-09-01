$(document).ready(function () {
  var $nextButton = $(".otree-btn-next");

  function checkFormCompletion() {
    var isFormValid = true;
    $('form input[type="radio"]').each(function () {
      var name = $(this).attr("name");
      if ($('input[name="' + name + '"]:checked').length == 0) {
        isFormValid = false;
        return false; // Break out of the loop
      }
    });

    return isFormValid;
  }

  $nextButton.on("click", function (e) {
    if (!checkFormCompletion()) {
      e.preventDefault();
      alert("To continue, please assess all the statements.");
    }
  });
});

document.addEventListener("DOMContentLoaded", function () {
  var radios = document.querySelectorAll('input[type="radio"]');
  radios.forEach(function (radio) {
    radio.checked = false;
  });
});
