Qualtrics.SurveyEngine.addOnReady(function()
{	
	jQuery("#" + this.questionId).change(function(event){
		loop = "${lm://CurrentLoopNumber}";
		var cat=jQuery("#" + loop + "_QID2").find(":selected").text();
		var choice = parseInt(cat);
		qId = 18; //value of textbox
		if(choice == 0){ //is 0 so hide and prefill, set trigger to true
			jQuery("#" + loop + "_QID" + qId).slideUp();
			jQuery("#" + loop + "_QID" + qId + "Separator").slideUp(function() {
				jQuery("#" + loop + "_QID18 input").val("NA");
			});
			Qualtrics.SurveyEngine.zeroConfs = true;
		} else if(typeof choice !== 'undefined'){//if it was set as NA rest, show it and set trigger to false
			if(	jQuery("#" + loop + "_QID18 input").val() == "NA"){
				jQuery("#" + loop + "_QID18 input").val("");
			}
			jQuery("#" + loop + "_QID" + qId).slideDown();
			jQuery("#" + loop + "_QID" + qId + "Separator").slideDown();
			Qualtrics.SurveyEngine.zeroConfs = false; 
		}
	});
	
});
