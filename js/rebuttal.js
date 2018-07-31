Qualtrics.SurveyEngine.addOnload(function()
{
	this.questionclick = function(event,element){
		if(this.getSelectedChoices()[0] == 2) {
			jQuery("#" + loop + "_QID20").hide();
			jQuery("#" + loop + "_QID20Separator").hide();
			jQuery("#" + loop + "_QID21").hide();
			jQuery("#" + loop + "_QID21Separator").hide();
		}
		if(this.getSelectedChoices()[0] == 1) {
			if(Qualtrics.SurveyEngine.onHelp) {
				jQuery("#" + loop + "_QID20").show();
				jQuery("#" + loop + "_QID20Separator").show();
			} 
			if(Qualtrics.SurveyEngine.onHelp == false){
				jQuery("#" + loop + "_QID21").show();
				jQuery("#" + loop + "_QID21Separator").show();
			}
		}
	}
});

Qualtrics.SurveyEngine.addOnReady(function()
{
	on = "${lm://Field/2}";
	loop = "${lm://CurrentLoopNumber}";
	dat = Qualtrics.SurveyEngine.rebuttal;
	if( (dat[on][0] != loop) && (dat[on][1] == 1 || dat[on][1] == 2)) { //if set then set it to the value it was before and hide only if not the same loop
		this.setChoiceValue(dat[on][1], true);
		jQuery("#" + this.questionId).hide();
		jQuery("#" + this.questionId + "Separator").hide();
		if(dat[on][1] == 2) { //then we will hide it if already set to no, if yes we hide and show
			jQuery("#" + loop + "_QID57").hide();
			jQuery("#" + loop + "_QID57" + "Separator").hide();
			jQuery("#" + loop + "_QID46").hide();
			jQuery("#" + loop + "_QID46" + "Separator").hide();
			jQuery("#" + loop + "_QID4").hide();
			jQuery("#" + loop + "_QID4" + "Separator").hide();
			jQuery("#" + loop + "_QID5").hide();
			jQuery("#" + loop + "_QID5" + "Separator").hide();
			jQuery("#" + loop + "_QID20").hide();
			jQuery("#" + loop + "_QID20Separator").hide();
			jQuery("#" + loop + "_QID21").hide();
			jQuery("#" + loop + "_QID21Separator").hide();
		}
	}
});

Qualtrics.SurveyEngine.addOnUnload(function()
{
	//push answer 
	answer = this.getSelectedChoices()[0];
	loop = "${lm://CurrentLoopNumber}";
	if(Qualtrics.SurveyEngine.rebuttal["${lm://Field/2}"] == null || Qualtrics.SurveyEngine.rebuttal["${lm://Field/2}"][0] == loop ) { //in case we set it again by mistake
		Qualtrics.SurveyEngine.rebuttal["${lm://Field/2}"] = [loop, answer];
	}
	console.log(Qualtrics.SurveyEngine.rebuttal);
});
