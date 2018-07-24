Qualtrics.SurveyEngine.addOnload(function()
{
	document.getElementById("1_QID46Separator").outerHTML = "";
});

Qualtrics.SurveyEngine.addOnReady(function()
{
	numpapers = parseInt("${e://Field/NumPapers}");
	confs = ["${e://Field/ConferenceName1}","${e://Field/ConferenceName2}","${e://Field/ConferenceName3}",
				 "${e://Field/ConferenceName4}", "${e://Field/ConferenceName5}", "${e://Field/ConferenceName6}",
				  "${e://Field/ConferenceName7}", "${e://Field/ConferenceName8}", "${e://Field/ConferenceName9}",
				  "${e://Field/ConferenceName10}", "${e://Field/ConferenceName11}", "${e://Field/ConferenceName12}",
				  "${e://Field/ConferenceName13}", "${e://Field/ConferenceName14}", "${e://Field/ConferenceName15}"];
	confs = confs.slice(0, numpapers);
	paperOn = "${lm://CurrentLoopNumber}";
	confOn = confs[paperOn-1]
	hit = false;
	//now we loop through what is before it and if the conference was already shown at least once before we set hit to true
	for(i = 0; i < paperOn - 1; i++) {
		if(confs[i] == confOn){
			hit = true;
		}
	}
	//now if it's been shown already, we will not show the rebuttal question, use jquery to hide
	if(hit) {
		//select hidden element to bypass required question
		Qualtrics.SurveyEngine.hiddenQuestion = true;
		qIds = [57, 46, 3]; //ID's of rebuttal questions
		for(i = 0; i < qIds.length; i++) {
			jQuery("#" + paperOn + "_QID" + qIds[i]).hide()
			jQuery("#" + paperOn + "_QID" + qIds[i] + "Separator").hide()
		}
	}
});
