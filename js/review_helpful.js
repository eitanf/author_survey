Qualtrics.SurveyEngine.addOnReady(function()
{
	/*Place your JavaScript here to run when the page is fully displayed*/
	this.questionclick = function(event,element){
		val = this.getSelectedChoices()[0];
		loopon = "${lm://CurrentLoopNumber}"
		if(val == 1) {
			jQuery("#" + loopon + "_QID20").show();
			jQuery("#" + loopon + "_QID20Separator").show()
			jQuery("#" + loopon + "_QID21").hide();
			jQuery("#" + loopon +"_QID21Separator").hide()
		} else if(val == 2){
			jQuery("#" + loopon + "_QID20").hide();
			jQuery("#" + loopon + "_QID20Separator").hide()
			jQuery("#" + loopon + "_QID21").show();
			jQuery("#" + loopon + "_QID21Separator").show()
		}

	};

});
