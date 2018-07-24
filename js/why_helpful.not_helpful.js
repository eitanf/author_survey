Qualtrics.SurveyEngine.addOnReady(function()
{
	/*Place your JavaScript here to run when the page is fully displayed*/
	jQuery("#"+this.questionId).hide();
	jQuery("#"+this.questionId + "Separator").hide();
});
