$(function(){
	$("#recordedButton").addClass("btn-dark")
	$("#homeButton").removeClass("btn-dark")
	let elementsQuantity =  $('.recorded-video-card').length
	let showQuantity = 6
	function showBySteps() {
		console.log("showing")
		console.log(showQuantity)
		$(".recorded-video-card").each(function(index) {
			if(index >=  showQuantity){
				$(this).hide()
			}
			else {
				$(this).show()
				$("#video"+index).attr("preload","metadata")
				//$("#video"+index).removeAttr( "preload" )
			}
		})
	}
	$("#showMore").click(()=>{
		showQuantity += 10
		console.log(showQuantity)
		showBySteps()
		if(showQuantity >= elementsQuantity) {
			$("#showMore").hide()
		}
	})
	showBySteps()
})