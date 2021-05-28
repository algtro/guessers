/**
	Display data from parameters
 */

function showGuessers(data) {
	const guessers = data['guessers'];
	let guessersText = "";
	let guesserHistory = "";
	let guesserName = "";
	if(typeof guessers === 'object') {
		guessers.forEach(function (guesser) {
			guesserName = guesserIndexToScreenName(guesser['index']);
			guesserHistory = historyListToString(guesser['history']);
			guessersText = `${guessersText}<div><h4>${guesserName}</h4>
                                           Вариант ответа: ${guesser['guess']}<br/>
                                           История ответов: ${guesserHistory}<br/>
                                           Уровень достоверности: ${guesser['confidence']}<div/>`;
		});
		$('#guessers').html(guessersText).show();
	}
}


function guesserIndexToScreenName(indexString) {
	let indexInt = parseInt(indexString);
	if (isNaN(indexInt)) {
		return "Экстрасенс без номера";
	}
	indexInt = indexInt + 1;
	return "Экстрасенс №" + indexInt;
}


function showAnswersHistory(data) {
	const userHistory = data['user_history'];
	const historyString = historyListToString(userHistory);
	if(typeof  userHistory === 'object') {
		$('#answersHistory').text("История загаданных чисел: " + historyString).show()
	}
}


function historyListToString(historyList) {
	const historyString = JSON.stringify(historyList, null, 2);
	const cleanString = historyString.replace("[", "");
	return cleanString.replace("]", "");
}


/**
	Screen states
 */

function stateStart(data) {
	$('#message').show();
	$('#guessers').hide();
	$('#answer').hide();
	showAnswersHistory(data);
	$('#errorAlert').hide();
}


function stateProcess(data) {
	$('#message').hide();
	showGuessers(data);
	$('#answer').show();
	showAnswersHistory(data);
	$('#errorAlert').hide();
}


function stateError(data) {
	$('#message').hide();
	$('#answer').hide();
	$('#answersHistory').hide();
	$('#guessers').hide();
	$('#errorAlert').text(data.error).show();
}


/**
	Event handlers setup
 */

$(document).ready(function() {


	$('#start').on('click', function () {

		$.ajax({
			type : 'GET',
			url : '/start'
		})
			.done(function(data) {
				if (data.error) {
					stateError(data);
				}
				else {
					stateProcess(data);
				}
			});

		event.preventDefault();
	});


	$('form').on('submit', function(event) {

		$.ajax({
			data : {
				answer : $('#answerInput').val()
			},
			type : 'POST',
			url : '/process'
		})
			.done(function(data) {
				if (data.error) {
					stateError(data);
				}
				else {
					stateStart(data);
				}
			});

		event.preventDefault();
	});


});