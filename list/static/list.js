window.SuperLists = {};

function initialize() {
	$('input[name="text"]').on('keypress', function() {
		$('.has-error').hide();
	});
}

window.SuperLists.initialize = initialize
