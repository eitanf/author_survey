Qualtrics.SurveyEngine.addOnReady(function()
{
	jQuery("#" + this.questionId).change(function(){
		var choice=jQuery("#QID79").find(":selected").text();
		console.log(choice);
		if(choice == "Other") {
			jQuery("#QID81").slideDown()
			jQuery("#QID81Separator").slideDown()
			Qualtrics.SurveyEngine.isOther = true;
		} else if(choice !== null) {
			jQuery("#QID81").slideUp()
			jQuery("#QID81Separator").slideUp()
			Qualtrics.SurveyEngine.isOther = false;
		}
	});
});
