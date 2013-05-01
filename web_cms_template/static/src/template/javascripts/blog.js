get_articles = function(page, categ, author) {
    // Get posts via ajax
    jQuery.ajax({ url: "internal/get_posts",
                type: "GET",
                data: { page:page, categ: categ, author:author} }).done(function(data) {
        // Replace entries div content with the data obtained from ajax call
        $("#entries").html(data);
        })
    };

get_categories = function () {
    jQuery.ajax("internal/get_categories").done(function(data){
        // Append pager after blog entries
        $("#categories").append(data);
        })
}
