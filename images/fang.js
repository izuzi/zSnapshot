jQuery(document).ready(function(){
    jQuery("#choose_fang_btn").click(function(){
        max_error = jQuery("#max_error").val();
        totle_area = jQuery("#totle_area").val();
        house_num = jQuery("#house_num").val();
        max_area = 180;
        min_area = 0;
        fang(max_error, totle_area, house_num, max_area, min_area);
    });
});

function fang(max_error, totle_area, house_num, max_area, min_area)
{
    jQuery("#err_1").html(""); jQuery("#err_2").html(""); jQuery("#err_3").html("");
    if(!max_error)
    {
        jQuery("#err_1").html("[x] é”™è¯¯ï¼Œè¯·é‡æ–°å¡«å†™[è¯¯å·®]");
        return;
    }
    if(!totle_area)
    {
        jQuery("#err_2").html("[x] é”™è¯¯ï¼Œè¯·é‡æ–°å¡«å†™[é¢ç§¯]");
        return;
    }
    if(!house_num)
    {
        jQuery("#err_3").html("[x] é”™è¯¯ï¼Œè¯·é‡æ–°å¡«å†™[å¥—æ•°]");
        return;
    }
    jQuery("#find_fang_btn").attr('disabled',"true");
    jQuery("#result_div").html("[!] æ­£åœ¨è®¡ç®—ä¸­ï¼Œè¯·ç¨åŽ");
    jQuery.ajax({  
        type : "GET",
        dataType:"jsonp",
        jsonp: "callback", 
        url : "http://izuzi.cn/zlab/fang/fang.php",
        data : {  
            "max_error" : max_error,
            "totle_area" : totle_area,
            "house_num" : house_num,
            "max_area" : max_area,
            "min_area" : min_area
        },
        success : function(result) {
            if(result.length>0){
                jQuery("#result_div").html("");
                jQuery("#result_div").append("<hr /><div id='result_count'>å…±è®¡ "+result.length+" ç§æ–¹æ¡ˆ</div><hr />"); 
                head="";
                head+="<span class='field_fang_error'>è¯¯å·®</span>";
                for(i=0;i<house_num;i++)
                {
                    head+="<span class='field_fang_type'>ç¬¬"+(i+1)+"å¥—</span>"
                }
                jQuery("#result_div").append(head);
                jQuery("#result_div").append("#div class='fang_item_clear'>#/div>".replace(/#/g,"<"));
                for(i=0;i< result.length;i++)
                {
                    res="";
                    fang_error=result[i]["err"];
                    fang_type=result[i]["type"];
                    res+="<span class='field_fang_error'>"+fang_error+"</span>";
                    for(j=0;j<fang_type.length;j++)
                    {
                        fang_type_area = fang_type[j]["area"];
                        fang_type_pos = fang_type[j]["pos"];
                        res+="<span class='field_fang_type'>";
                        res+=fang_type_area;
                        res+="<br>"
                        for(k=0;k<fang_type_pos.length;k++)
                        {
                            res+="[";
                            res+=fang_type_pos[k];
                            res+="]";
                        }
                        res+="</span>";
                    }
                    jQuery("#result_div").append("<span class='fang_item'>"+res+"</span>");
                    jQuery("#result_div").append("#div class='fang_item_clear'>#/div>".replace(/#/g,"<"));
                }
                jQuery("#result_div").append("<hr /><div id='result_count'>å…±è®¡ "+result.length+" ç§æ–¹æ¡ˆ</div><hr />");                                     
            }
            else{
                jQuery("#result_div").html("[?] æŠ±æ­‰ï¼Œæ²¡æœ‰åˆé€‚çš„ç»„åˆæ–¹æ¡ˆï¼");
            }
            jQuery("#find_fang_btn").attr('disabled',"false");
        },
        error : function() {
            jQuery("#find_fang_btn").attr('disabled',"false");
            jQuery("#result_div").html("[x] ç³»ç»Ÿæ•…éšœï¼Œè¯·é‡è¯•");
        }
    }); 
}