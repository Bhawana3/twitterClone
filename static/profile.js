$(document).ready(function(){
        $('.delete-tweet').click(function(){
            var element = $(this);
            var user_tweet = $(this).attr('tweet');
            $.ajax({
                url:'/delete_tweet',
                data:{'tid':user_tweet},
                type:'post',
                success:function(response){
                    if(response["message"] === "success"){
                        console.log("tweet deleted successfully!");
                        element.closest('div').remove();
                    }
                    else if(response["message"] === "failure"){
                        console.log("tweet already deleted!");
                    }
                }
            });
        });
    });
    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                $('#upload-image')
                    .attr('src', e.target.result)
                    .width(100)
                    .height(100);
            };

            reader.readAsDataURL(input.files[0]);
        }
    }

    $(document).ready(function(){
        $('.upload').click(function(){
             var form_data = new FormData($('#upload-file')[0])
             console.log(form_data);
             $.ajax({
                 url:'/upload',
                 type:'post',
                 data: form_data,
                 contentType: false,
                 cache: false,
                 processData: false,
                 async: false,
                 success: function(response) {
                    if(response["message"] === "success"){
                        console.log('Success!');
                        $('#show').show();
                        setTimeout(function(){//
                            location.reload(); // then reload the page.(3)
                        });
                     }
                    else{
                        $('#failure').show();
                        }
                 }
             });
        });
    });

$(function($){
        var addToAll = false;
        var gallery = true;
        var titlePosition = 'inside';
        $(addToAll ? 'img' : 'img.fancybox').each(function(){
            var $this = $(this);
            var title = $this.attr('title');
            var src = $this.attr('data-big') || $this.attr('src');
            var a = $('<a href="#" class="fancybox"></a>').attr('href', src).attr('title', title);
            $this.wrap(a);
        });
        if (gallery)
            $('a.fancybox').attr('rel', 'fancyboxgallery');
        $('a.fancybox').fancybox({
            titlePosition: titlePosition
        });
    });
    $.noConflict();
