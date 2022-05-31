$(document).ready(function(){

    $("input:checkbox[name=substitute_selected_data]:checked").each(function(){
    yourArray.push($(this).val());
});

});