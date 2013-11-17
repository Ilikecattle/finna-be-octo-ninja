$(document).ready(function() {
	$('.description').toggleClass('hide');
	$(".tease_btn").on('click', function() {
		$(this).prev('.description').toggleClass('hide');
	});
});
