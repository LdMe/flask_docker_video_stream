$(function(){
	$("#recordedButton").addClass("btn-dark")
	$("#homeButton").removeClass("btn-dark")
	let elementsQuantity =  $('.recorded-video').length
	let showQuantity = 10
	function showBySteps() {
		console.log("showing")
		console.log(showQuantity)
		$(".recorded-video").each(function(index) {
			if(index >=  showQuantity){
				console.log(index)
				$(this).hide()
			}
			else {
				$(this).show()
			}
		})
	}
	$("#showMore").click(()=>{
		showQuantity += 10
		console.log(showQuantity)
		showBySteps()
	})
	showBySteps()
})