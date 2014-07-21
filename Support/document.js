/* global Zepto, document, EJS, context, ejsTemplate, TextMate */
/* global error_explanations */

Zepto(document).ready(function($) {
  var VERSION = '1.1.0';

  // close the report window when the user presses ESCape
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

  // add links to error/warning codes, when available
  $('.issue-code').each(function(index, item) {
    var issueCode = $(item).text();
    if (error_explanations.hasOwnProperty(issueCode)) {
      var url = error_explanations[issueCode];
      $(item).wrap('<a href="' + url + '" class="open-external">');
    }
  });

  // By default, links will open in the TextMate results window. If
  // the <a> tag has class "open-external" we’ll catch it and open
  // the link in the user’s browser instead.
  $('.open-external').on('click', function(e) {
    e.preventDefault();
    var href = $(this).attr('href');
    if (!href.match(/^http(?:s?)\:\/\/[^\/]/)) {
      // doesn’t look like a normal URL
      return;
    }
    TextMate.system('open "' + encodeURI(href) + '"', null);
  });

  $('.version-number').text('v' + VERSION);

  // parse a version number into semver parts
  var parseVersion = function(ver) {
    return ver.split('.').map(function(part) { return parseInt(part, 10); });
  };

  // return true if target is newer than current
  var newer = function(current, target) {
    var currentParts = parseVersion(current);
    var targetParts = parseVersion(target);
    if (currentParts.length !== 3 || targetParts.length !== 3) { return false; }

    if (targetParts[0] > currentParts[0]) { return true; }
    if (targetParts[0] < currentParts[0]) { return false; }

    if (targetParts[1] > currentParts[1]) { return true; }
    if (targetParts[1] < currentParts[1]) { return false; }

    if (targetParts[2] > currentParts[2]) { return true; }
    if (targetParts[2] < currentParts[2]) { return false; }

    return false;
  };

  $('.update-checker').on('click', function(e) {
    $.getJSON('http://natesilva.github.io/jshint-external.tmbundle/latest.json',
      function(data)
    {
      $('.update-checker').addClass('hidden');
      if (newer(VERSION, data.latest)) {
        $('.update-available').removeClass('hidden');
      } else {
        $('.no-update').removeClass('hidden');
      }
    });
  });
});
