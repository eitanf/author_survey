Qualtrics.SurveyEngine.addOnReady(function()
{
	loopon = "${lm://CurrentLoopNumber}";
	//handle hidden input - hide it
	label = document.getElementById("QR~"  + loopon + "_QID3~3");
	answer = label.parentElement;
	if(answer.tagName == "LI"){
		answer.style = "display: none;";
	} //if supposed to be set - set it to bypass validation
	if(Qualtrics.SurveyEngine.hiddenQuestion) {
		choices = this.getChoices();
		this.setChoiceValue(choices[2], true);
	}
	
	//handle the is it helpful text
	this.questionclick = function(event,element){
		val = this.getSelectedChoices()[0];
		if(val == 1) {
			if(this.fieldOn == 1){
				jQuery("#" + loopon + "_QID20").show();
				jQuery("#" + loopon + "_QID20Separator").show()
			} else if(this.fieldOn == 2){
				jQuery("#" + loopon + "_QID21").show();
				jQuery("#" + loopon + "_QID21Separator").show()
			}
		}
		if(val == 2) {
			isHelpful = jQuery("#" + loopon + "_QID20").is(":visible"); 
			isNotHelpful = jQuery("#" + loopon + "_QID21").is(":visible"); 
			if(isHelpful){
				jQuery("#" + loopon + "_QID20").hide();
				jQuery("#" + loopon + "_QID20Separator").hide()
				this.fieldOn = 1
			} else if(isNotHelpful){
				jQuery("#" + loopon + "_QID21").hide();
				jQuery("#" + loopon +"_QID21Separator").hide()
				this.fieldOn = 2
			}		
		}
	}

});
