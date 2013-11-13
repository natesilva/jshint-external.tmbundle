/* global Zepto, document, EJS, context, ejsTemplate */

Zepto(document).ready(function($) {
  var html = new EJS({text: ejsTemplate}).render(context);
  $('#content').html(html);
});
