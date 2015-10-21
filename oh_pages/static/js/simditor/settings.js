$(function() {
  var editor = new Simditor({
    textarea: $('#id_content'),
    defaultImage:'/s/img/avatar.png',
    toolbar: [
      'title',
      'bold',
      'italic',
      'underline',
      'strikethrough',
      'color',
      'ol',
      'ul',
      'blockquote',
      'code',
      'table',
      'link',
      'image',
      'indent',
      'outdent',
      'alignment'
    ]
  });
});