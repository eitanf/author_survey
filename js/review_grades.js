Qualtrics.SurveyEngine.addOnReady(function()
{
	onLoop = "${lm://CurrentLoopNumber}"
	totalLoop = "${lm://TotalLoops}"
	total = (parseInt(totalLoop) * 3) + 1
	on = (parseInt(onLoop)*3) 
	div = Math.floor((on/ total) * 100)
	fill = document.getElementsByClassName("ProgressBarFill")[0]
	fill.style = "width: " + div + "%"
	
	jQuery("#" + this.questionId).hide()
	jQuery("#" + this.questionId + "Separator").hide()
});
