Qualtrics.SurveyEngine.addOnReady(function()
{
	this.questionclick = function(event, element){
		val = this.getSelectedChoices()[0];
		on = "${lm://CurrentLoopNumber}"
		qNums = [34, 53, 49, 61, 50, 54, 64, 63, 66, 65, 68, 67] //Sequential number id's
		chosen = 0;
		if(val == "121") { //0
			chosen = 0;
		} else if(val == "122") { //1
			chosen = 1;
		} else if(val == "123") { //2
			chosen = 2; 
		} else if(val == "124") { //3
			chosen = 3;
		} else if(val == "125") { //4
			chosen = 4;
		} else if(val == "126") { //5
			chosen = 5;
		} else if(val == "127") { //6
			chosen = 6;
		}
		
		//Now loop through everything.... using jquery slide them down
		for (var i = 0; i < chosen*2; i += 2) { //loops through each question pair
			var q1 = qNums[i];
			var q2 = qNums[i+1];
			jQuery("#" + on + "_QID" + q1).slideDown()
			jQuery("#" + on + "_QID" + q1 + "Separator").slideDown()
			jQuery("#" + on + "_QID" + q2).slideDown()
			jQuery("#" + on + "_QID" + q2 + "Separator").slideDown()
		}
		
		//Then hide the others... just to be safe
		for(var i = chosen* 2; i <= qNums.length; i+=2){
			var q1 = qNums[i];
			var q2 = qNums[i+1];
			jQuery("#" + on + "_QID" + q1).slideUp()
			jQuery("#" + on + "_QID" + q1 + "Separator").slideUp()
			jQuery("#" + on + "_QID" + q2).slideUp()
			jQuery("#" + on + "_QID" + q2 + "Separator").slideUp()

		}
	}
});
