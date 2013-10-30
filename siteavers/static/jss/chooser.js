$(document).ready(function(){
    $('.countries').change(function(){
	var name =$(this).attr('name') 
	var sel = $(this).find('option:selected').val()
	var lang = $('input[name=lang]').val()
	switch(name){
	    case 'co_from':
	    $.get('/points/ajx/cities/',{
		'sel':sel,
		'lang':lang
	    
	    },
		  function(data){
		      json_data  = $.parseJSON(data)
		      $('#ci_from option[value!=""]').remove()
		      $.each(json_data,function(){
			  var option = '<option value="'+this['value']+'">'+this['nazva']+'</option>'
			  $('#ci_from').append(option)
		      })
		  })
	    break;

	    case 'co_to':
	    $.get('/points/ajx/cities/',{
		'sel':sel,
		'lang':lang
	    
	    },
		  function(data){
		      json_data  = $.parseJSON(data)
		      $('#ci_to option[value!=""]').remove()
		      $.each(json_data,function(){
			  var option = '<option value="'+this['value']+'">'+this['nazva']+'</option>'
			  $('#ci_to').append(option)
		      })
		  })
	    break;
	}
    })
})
