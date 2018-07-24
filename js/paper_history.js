Qualtrics.SurveyEngine.addOnload(function()
{
	/*Place your JavaScript here to run when the page loads*/
	document.getElementById("1_QID1Separator").outerHTML = "";

});

Qualtrics.SurveyEngine.addOnReady(function()
{
	/*Place your JavaScript here to run when the page is fully displayed*/
	onLoop = "${lm://CurrentLoopNumber}"
	totalLoop = "${lm://TotalLoops}"
	total = (parseInt(totalLoop) * 3) + 1
	on = (parseInt(onLoop)*3) - 2
	div = Math.floor((on/ total) * 100)
	fill = document.getElementsByClassName("ProgressBarFill")[0]
	fill.style = "width: " + div + "%"
});
