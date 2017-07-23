$(function(){
    $('#search').keyup(function() {
        $.ajax({
            type: 'POST',
            url: '/comics/search_comics',
            data: {
                'search' : $('#search').val(),
                'csrfmiddlewaretoken' : jQuery("[name=csrfmiddlewaretoken]").val()
            },
            success: searchSuccess,
            dataType: 'html'
        });
    });

    $('.browse_page').click(function(){
        $.ajax({
            type: 'POST',
            url: '/comics/browse_comics',
            data: {
                'page' : $(this).text(),
                'csrfmiddlewaretoken' : jQuery("[name=csrfmiddlewaretoken]").val()
            },
            success: browseSuccess,
            dataType: 'html'
        })
    });

    $('[name=review_button]').click(function(){
        $('.add_review').show();
        $(this).hide();
    })
    
    $('[name=show_comments]').click(function(){
        if($(this).text() == "Show Comments") {
            $(this).siblings('.comment').css('display', 'block');
            $(this).text("Hide Comments");
        }else{
            $(this).siblings('.comment').css('display', 'none');
            $(this).text("Show Comments");
        }
    })

    $('.review').on('click', '[name=comment_button]', function(){
        $(this).siblings('.add_comment').show();
        $(this).hide();
    })

    $('.add_sub_select').on("change", function() {
        $(this).after(
            "<div><a id='add_more_subs' href='#'>Add more titles</a></div>"
        );
        $(this).off("change");
    })

    $('.add_subs').on("click", "#add_more_subs", function(){
        $(this).before("<div id='more_subs'></div>")
        $.ajax({
            type: 'POST',
            url: '/comics/sub_form_expansion',
            data: {
                'csrfmiddlewaretoken' : jQuery("[name=csrfmiddlewaretoken]").val()
            },
            success: subFormExpansion,
            dataType: 'html'
        });
    })
});

function searchSuccess(data, textStatus, jqXHR){
    $('#comic_list').html(data);
}
function browseSuccess(data, textStatus, jqXHR){
    $('#comic_list').html(data);
}
function subFormExpansion(data, textStatus, jqXHR){
    $('#more_subs:last-of-type').html(data);
}
