/**
 * bing_img_api
 * @author izuzi@foxmail.com
 *
 * Copyright (c) 2018, http://o-k.la
 */
(function() {
    img_list = new Array();
    
    window.load_bing_img = function (element){
    	jQuery.ajax({  
            type : "GET",
            dataType:"jsonp",
            jsonp: "callback", 
            url : "http://okla.applinzi.com/lab/bing_img_api.php",
            data : {
                "format":"js",
                "idx":0,
                "n":3
            },
            success : function(result) {
                if(result){
                    images = result.images;
                    for(i=0; i<images.length; i++){
                        full_url = "https://cn.bing.com" + images[i].url;
                        img_list.push(full_url);
                    }
                    
                    set_img(element);
                }
            },
            error : function() {
                alert("error");
            }
        });   
    };
    
    function get_random(n){
        if(n <= 0) return 0;
        
        min = 0;
        max = n - 1;
        return Math.floor(Math.random()*(max-min+1)+min);
    };
    
    function set_img(element){
        if(img_list.length == 0) return;
        
        rdm = get_random(img_list.length);
        url = img_list[rdm];
        //alert(url);               
        jQuery(element).css("background-image","url("+ url +")");
        //alert(jQuery(element).css("background-image"));
    };
})();