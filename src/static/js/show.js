$(function(){
	$("#recordedButton").addClass("btn-dark")
	$("#homeButton").removeClass("btn-dark")
	let elementsQuantity =  $('.recorded-video').length
	let showQuantity = 10
	function showBySteps() {
		console.log("showing")
		console.log(showQuantity)
		let counter = 0
		$(".recorded-video").each(() => {
			if(counter >=  showQuantity){
				console.log(counter)
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
		console.log(showQuantity)
		showBySteps()
	})
	showBySteps()
})