QUnit.test( "errors should be hidden on input", function( assert ) {
	SuperLists.initialize();
	$('input[name="text"]').trigger('keypress');
	assert.equal($('.has-error').is(':visible'), false)
});

QUnit.test( "errors aren't hidden if there is no keypress", function( assert ) {
	SuperLists.initialize();
	assert.equal($('.has-error').is(':visible'), true)
});
