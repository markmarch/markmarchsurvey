$('.dropdown input').bind('click', function (e) {
  e.stopPropagation()
});

$('.modal-footer .cancel').bind('click', function(e) {
  $('#modal-from-dom').modal('hide');
});