$(function(){
	$("#homeButton").addClass("btn-dark")
	$("input[type='range']").each( function(){
		console.log("name")
		let name = $(this).attr("name")

		$("input[type='number'][name='"+name+"_value']").val($(this).val())
	})
	$("input[type='range']").on("change", function(){
		let name = $(this).attr("name")
		$("input[type='number'][name='"+name+"_value']").val($(this).val())
	})
	$("input[type='number']").on("change", function(){
		let name = $(this).attr("name").replace("_value","")
		let max= parseInt($("input[type='range'][name='"+name+"']").attr("max"))
		let min= parseInt($("input[type='range'][name='"+name+"']").attr("min"))
		let value = parseInt($(this).val())
		if(value > max){
			value = max;
		}
		else if(value < min){
			value = min;
		}
		$(this).val(value);
		$("input[type='range'][name='"+name+"']").val(value)
	})
	$("input[type='number']").on("keypress", function(event){
		$(this).val($(this).val().replace(/[^\d].+/, ""));
		if ((event.which < 48 || event.which > 57)) {
			event.preventDefault();
		}
	})
	$("#showWriters").click(function(){
		$(this).toggleClass("show");
		if($(this).hasClass("show")){
			showWriters();
		}
		else{
			hideWriters()
		}
	});
	
	$("#writerForm").ajaxForm(function(){
		$('#modal').modal('toggle');
	})
	$(".dropdown-item").on("click",function(event){

	})
	function showWriters(){
		getWriters();
		interval =setInterval( 
			function(){
				getWriters();
				$("#writerTable td").on("hover")
			},1000);

	}
	function getWriters(){
		$.ajax({url: "/active", 
			success: function(result){

				$("#writers").empty()
				$("#showWriters").text("hide writers");
				$("#showWriters").removeClass("btn-success");
				$("#showWriters").addClass("btn-danger");
				console.log(result)
				if(Object.entries(result).length === 0){
					$("#writers").append("<p> No writers active</p>");
					return;
				}
				$("#writers").append("<table class='table table-sm table-hover' id='writerTable'>\
					<thead>\
					<tr>\
					<th>id</th>\
					<th>duration</th>\
					<th>fps</th>\
					<th>speed</th>\
					<th>remaining time</th>\
					</tr>\
					</thead>\
					<tbody></tbody>\
					</table>")
				for (id in result){
					let element = result[id]
					let progress = (element.remainingTime / element.realRecordingDuration) * 100
					$("#writerTable tbody").append("\
						<tr>\
						<td>"+element.id+"</td>\
						<td>"+element.outputSeconds+"s</td>\
						<td>"+element.fps+"</td>\
						<td>x"+element.speed+"</td>\
						<td id='progress"+id+"'>\
						<div class='progress' >\
						<div  id='progress-bar"+id+"' class='progress-bar progress-bar-striped progress-bar-animated \
						' role='progressbar' style='width: "+progress+"%;' aria-valuenow='"+progress+"' aria-valuemin='0' aria-valuemax='100'>"+parseInt(element.remainingTime)+"</div>\
						</div>\
						</td>\
						</tr>");
					if (element.paused == true) {
						$("#progress-bar"+id).addClass("bg-warning")
					}
				}
				$("[id*='progress']").on("click",function(){
					let id = $(this).attr("id").replace("progress","");

					togglePauseWriter(id);
				});



			}
		});
	}
	function togglePauseWriter(id){
		$.ajax({url: "/pause/"+id, 
			success: function(result){

			}
		});
	}
	function createWriter(id){

	}
	function hideWriters(){
		$("#writers").empty()

		$("#showWriters").removeClass("btn-danger");
		$("#showWriters").addClass("btn-success");
		$("#showWriters").text( "show writers");
		clearInterval(interval);
	}

})