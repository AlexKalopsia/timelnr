$(document).ready(function () {
  //HIDE ELEMENTS ON LOAD
  //$('#entry-add').hide();
  //$('.entry-status').find('p').hide();

  //REVEAL/HIDE NON-CANON
  $("#button-canon").click(function (event) {
    $(this).text(function (i, text) {
      return text === "Show everything"
        ? "Hide uncertain canon"
        : "Show everything";
    });
    $(".mgspo-group").slideToggle(250);
    $(".d-md-block.mgspo-label").slideToggle(250);
    //$('.mgr').slideToggle(250);
  });

  //REVEAL/HIDE MGSV
  $("#button-mgsv").click(function (event) {
    console.log("HIDEEE");
    $(this).text(function (i, text) {
      return text === "Show MGSV" ? "Hide MGSV" : "Show MGSV";
    });
    $(".mgsv-group").slideToggle(250);
    //$('.mgr').slideToggle(250);
  });

  /**
   * Check a href for an anchor. If exists, and in document, scroll to it.
   * If href argument ommited, assumes context (this) is HTML Element,
   * which will be the case when invoked by jQuery after an event
   */
  function scroll_if_anchor(href) {
    href = typeof href == "string" ? href : $(this).attr("href");

    var fromTop = 50;

    // If our Href points to a valid, non-empty anchor, and is on the same page (e.g. #foo)
    // Legacy jQuery and IE7 may have issues: http://stackoverflow.com/q/1593174
    if (href.indexOf("#") == 0) {
      var $target = $(href);

      // Older browser without pushState might flicker here, as they momentarily
      // jump to the wrong position (IE < 10)
      if ($target.length) {
        $("html, body").animate({ scrollTop: $target.offset().top - fromTop });
        if (history && "pushState" in history) {
          history.pushState(
            {},
            document.title,
            window.location.pathname + href
          );
          return false;
        }
      }
    }
  }

  // When our page loads, check to see if it contains and anchor
  scroll_if_anchor(window.location.hash);

  // Intercept all anchor clicks
  $("body").on("click", "a", scroll_if_anchor);
});
