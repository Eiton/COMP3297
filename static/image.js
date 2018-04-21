function downloadImage(pk) {    
    $.ajax({
            type: "GET",
            url:'/uploadImage/download/'+pk, 
        })
        .done(function(response) {
            $('#image_'+pk).replaceWith(response);
        });
}
function like(pk) {
    $.ajax({
            type: "GET",
            url:'/uploadImage/like/'+pk, 
        })
        .done(function(response) {
            $('#image_'+pk).replaceWith(response);
        });
}