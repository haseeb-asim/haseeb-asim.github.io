(function () {
  var dialog = document.querySelector("#viewer");
  var title = document.querySelector("#viewer-title");
  var kind = document.querySelector("#viewer-kind");
  var summary = document.querySelector("#viewer-summary");
  var count = document.querySelector("#viewer-count");
  var screens = document.querySelector("#viewer-screens");
  var cards = Array.prototype.slice.call(document.querySelectorAll(".concept"));
  var index = 0;

  if (!dialog || !cards.length) return;

  function openAt(next) {
    index = (next + cards.length) % cards.length;
    var card = cards[index];
    var template = document.getElementById("tpl-" + card.getAttribute("data-concept"));
    if (!template) return;

    title.textContent = card.querySelector(".concept-name").textContent;
    kind.textContent = card.querySelector(".concept-kind").textContent;
    summary.textContent = card.querySelector(".concept-summary").textContent.trim();
    count.textContent = index + 1 + " of " + cards.length;
    screens.replaceChildren(template.content.cloneNode(true));
    dialog.scrollTop = 0;

    if (!dialog.open) dialog.showModal();
  }

  cards.forEach(function (card, cardIndex) {
    card.addEventListener("click", function () {
      openAt(cardIndex);
    });
  });

  document.querySelector("#viewer-close").addEventListener("click", function () {
    dialog.close();
  });

  document.querySelector("#viewer-prev").addEventListener("click", function () {
    openAt(index - 1);
  });

  document.querySelector("#viewer-next").addEventListener("click", function () {
    openAt(index + 1);
  });

  dialog.addEventListener("click", function (event) {
    if (event.target === dialog) dialog.close();
  });
})();
