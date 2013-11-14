/* global Zepto, document, EJS, context, ejsTemplate, TextMate */

Zepto(document).ready(function($) {
  // (try to) close the report window when the user presses ESCape
  $(document).keydown(function(e) {
    if (e.keyCode === 27) {
      e.preventDefault();
      var cmd = '"tell application \\"System Events\\" ' +
        'to keystroke \\"w\\" using command down"';
      TextMate.system('osascript -e ' + cmd, function(){});
    }
  });

  // render the template and inject it into the page
  var html = new EJS({text: ejsTemplate}).render(context);
  $('#content').html(html);
});
