$(function(){
	$("#recordedButton").addClass("btn-dark")
	$("#homeButton").removeClass("btn-dark")
	let elementsQuantity =  $('.recorded-video').length
	let showQuantity = 10
	function showBySteps() {
		let counter = 0
		$(".recorded-video").each(() => {
			if(counter <  showQuantity){
				$(this).hide()
			}
			else {
				$(this).show()
			}
			counter++
		})
	}
	$("#showMore").click(()=>{
		showQuantity += 10
		showBySteps()
	})
	showBySteps()
})