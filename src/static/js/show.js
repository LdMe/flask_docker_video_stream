$(function(){
	$("#recordedButton").addClass("btn-dark")
	$("#homeButton").removeClass("btn-dark")
	let elementsQuantity =  $('.recordedVideo').length
	let showQuantity = 10
	function showBySteps() {
		let counter = 0
		$(".recordedVideo").each(() => {
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