$(document).bind('DOMNodeInserted DOMNodeRemoved', function(element){
    if($(this).hasClass('djn-dynamic-form-survey-question')){
        console.log(element.target);
    }

});

if ($('select[name*="question_set"]:not([name*="prefix"])').val() != 'image') {
		$('fieldset[class*="question-images"]').css("display", "none");
}


// Call the below function
waitForElementToDisplay('select[name*="question_set"]:not([name*="prefix"])',function(){console.log('DONE'); add_event_listener()},500,9000);

function waitForElementToDisplay(selector, callback, checkFrequencyInMs, timeoutInMs) {
  var startTimeInMs = Date.now();
  (function loopSearch() {
    if (document.querySelector(selector) != null) {
      callback();
      return;
    }
    else {
      setTimeout(function () {
        if (timeoutInMs && Date.now() - startTimeInMs > timeoutInMs)
          return;
        loopSearch();
      }, checkFrequencyInMs);
    }
  })();
}

function add_event_listener() {
	$('select[name*="question_set"]:not([name*="prefix"])').on('change', function() {
		if ($(this).val() == 'image') {
				$('fieldset[class*="question-images"]').css("display", "block");
		} else {
				$('fieldset[class*="question-images"]').css("display", "none");
		}
	});
}
