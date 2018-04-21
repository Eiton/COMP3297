function downloadImage(pk) {    
    $.ajax({
            type: "GET",
            url:'/download/'+pk, 
        })
        .done(function(response) {
            $('#image_'+pk).replaceWith(response);
        });
}
function like(pk) {
    $.ajax({
            type: "GET",
            url:'/like/'+pk, 
        })
        .done(function(response) {
            $('#image_'+pk).replaceWith(response);
        });
}