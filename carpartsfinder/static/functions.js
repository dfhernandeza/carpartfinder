
//populate divs from data object matching name and key
function populateText(container, data) {
    $.each(data, function (key, value) {     
        $('[name=' + key + ']', container).text(value);       
    });
}
//populate inputs from data object matching name and key
function populateInput(container, data) {
    $.each(data, function (key, value) {     
        $('[name=' + key + ']', container).val(value);       
    });
}
// returs an array of objects from a collection of html items
function ajaxData(coleccion) {
    var jsonData = {};
    coleccion.each(function (i, item) {        
            var key = $(item).attr('name');           
            jsonData[key] = $(this).val();           
    });

    return (jsonData)
}
// populates a dropdown list from array of objects
function populateSelect(data){
    var html = '';
    $(data).each(function(i, item){
        html = html + `<option value="${item.id}">${item.text}</option>`;
    });
    return html;
}
$(document).on('change','#make',function(){
    var $this = $(this);            
    $.ajax({
        url: "/getModels",
        type: 'POST',
        async: false,
        dataType: 'json',
        data:{
            idmake : $this.val()
        },
        success: function (data) {                    
          $('#model').append(populateSelect(data)).removeAttr('disabled') 
            
        },
    });
});  
$(document).on('change','#model',function(){
    var $this = $(this);            
    $.ajax({
        url: "/getYears",
        type: 'POST',
        async: false,
        dataType: 'json',
        data:{
            idmodel : $this.val()
        },
        success: function (data) {                    
          $('#year').append(populateSelect(data)).removeAttr('disabled')
            
        },
    });
}); 
$(document).ready(function(){
    $('#searchForm').validate({
        errorPlacement: function(error, element){
            return true;
        },
        rules:{
            q: "required"
        }

    });
})