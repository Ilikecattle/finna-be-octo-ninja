$(document).ready(function() {
	$('.description').toggleClass('hide');
	$(".tease_btn").on('click', function() {
		$(this).prev('.description').toggleClass('hide');
	});
	function checkOffset() {
		if ($('.bottom-buttons').offset().top + $('.bottom-buttons').height() >= $('footer').offset().top - 10) $('.bottom-buttons').css('position', 'relative');
		if ($(document).scrollTop() + window.innerHeight < $('footer').offset().top) $('.bottom-buttons').css('position', 'fixed'); // restore when you scroll up
	}
	$(document).scroll(function() {
		checkOffset();
	});
	checkOffset();
});
