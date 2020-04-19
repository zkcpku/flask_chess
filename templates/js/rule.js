// var bout = false;//是否允许落子
var color = "";//自己落子颜色
function get_color(){
    $.get("/getColor",function(rtnFromSvr){
        color = rtnFromSvr;
    })
}
function try_play(xy){
    var rst = '';
    $.get("/play_chess",{xy:xy},function(rtnFromSvr){
        rst = rtnFromSvr;
    })
    return rst;
}

setInterval("get_color()",1000);

var row = 15;
var col = 15;
var widthAndHeight = 30;//格子宽度高度
var WuZiQi = {
    isEnd:function(xy,chessmanColor){//判断是否结束游戏
        var id = parseInt(xy);
        //竖的计算
        var num = 1;
        num = WuZiQi.shujia(num,id,chessmanColor);
        num = WuZiQi.shujian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("游戏结束！你赢了！");
            }else{
                confirm("游戏结束！你输了！");
            }
            return ;
        }
        num = 1;
        num = WuZiQi.hengjia(num,id,chessmanColor);
        num = WuZiQi.hengjian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("游戏结束！你赢了！");
            }else{
                confirm("游戏结束！你输了！");
            }
            return ;
        }
        num = 1;
        num = WuZiQi.zuoxiejia(num,id,chessmanColor);
        num = WuZiQi.zuoxiejian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("游戏结束！你赢了！");
            }else{
                confirm("游戏结束！你输了！");
            }
            return ;
        }
        num = 1;
        num = WuZiQi.youxiejia(num,id,chessmanColor);
        num = WuZiQi.youxiejian(num,id,chessmanColor);
        if(num>=5){
            if(chessmanColor==color){
                confirm("游戏结束！你赢了！");
            }else{
                confirm("游戏结束！你输了！");
            }
            return ;
        }
    },youxiejia:function(num,id,color){
        var yu = id%row;
        id = id+(row-1);
        if(id<(row*col)&&(id%row)<yu){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.youxiejia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },youxiejian:function(num,id,color){
        var yu = id%row;
        id = id-(row-1);
        if(id>=0&&(id%row)>yu){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.youxiejian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },zuoxiejia:function(num,id,color){
        var yu = id%row;
        id = id+(row+1);
        if(id<(row*col)&&(id%row)>yu){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.zuoxiejia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },zuoxiejian:function(num,id,color){
        var yu = id%row;
        id = id-(row+1);
        if(id>=0&&(id%row)<yu){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.zuoxiejian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    hengjia:function(num,id,color){
        var yu = id%row;
        id = id+1;
        if(id<(row*col)&&(id%row)>yu){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.hengjia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
        
    },
    hengjian:function(num,id,color){
        var yu = id%row;
        id = id-1;
        if(id>=0&(id%row)<yu){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.hengjian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    shujia:function(num,id,color){
        id = id+row;
        if(id<(row*col)){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.shujia(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    shujian:function(num,id,color){
        id = id-row;
        if(id>=0){
            var flag = WuZiQi.checkColor(id,color);
            if(flag){
                num++;
                return WuZiQi.shujian(num,id,color);
            }else{
                return num;
            }
        }else{
            return num;
        }
    },
    checkColor:function(xy,color){
        if($("#"+xy).children("div").hasClass(color)){
            return true;
        }else {
            return false;
        }
    },
    playchess:function(e){
        // console.log(e);
        if(color!=""){
            if($(e).children("div").length>0){
                alert("这里已经有子了！请在其它地方落子！");
                return;
            }
            var try_rst = try_play($(e).attr("id"));
            console.log(try_rst)
            if (try_rst == '1') {
                $("#messageContent").append("系统：已落子!");
                $("#"+$(e).attr("id")).html("<div class=\"chessman "+color+"\"></div>");
                WuZiQi.isEnd($(e).attr("id"),color)
            }
            else if (try_rst == '0') {
                $("#messageContent").append("系统：请等待你的对手落子!");
            }
            else {
                $("#messageContent").append("系统：已断开连接");
            }

        }else{
            $("#messageContent").append("系统：游戏还没有开始!");
            $("#messageContent").append("\n");
            $("#messageContent").scrollTop($("#messageContent")[0].scrollHeight - $("#messageContent").height());
        }
        
    },
    //发送消息
    sendMessage:function(){
      var message = $("#message").val();
      if(message!=""){
          var result = {};
          result.message = message;
          // websocket.send(JSON.stringify(result));
          $("#message").val("");
      }else{
          $("#messageContent").append("系统：请不要发送空信息!");
          $("#messageContent").append("\n");
          $("#messageContent").scrollTop($("#messageContent")[0].scrollHeight - $("#messageContent").height());
      }

  }
};
$(function(){
    //根据棋盘格子数得到棋盘大小
    $("#background").css({width:(row*widthAndHeight)+"px",height:(col*widthAndHeight)+"px"});
    //用canvas画棋盘
    var canvas = document.createElement("canvas");
//    $(canvas).attr({width:((row-1)*widthAndHeight)+"px",height:(col-1)*widthAndHeight+"px"});
//    $(canvas).css({"position":"relative","top":(widthAndHeight/2)+"px","left":(widthAndHeight/2)+"px","z-index":9999});
$(canvas).attr({width:(row*widthAndHeight)+"px",height:col*widthAndHeight+"px"});
$(canvas).css({position:"relative","z-index":9999});
var cot = canvas.getContext("2d");
cot.fillStyle = "#EAC000";
cot.fillRect(0,0,row*widthAndHeight,col*widthAndHeight);
cot.lineWidth = 1;
var offset = widthAndHeight/2;
    for(var i=0;i<row;i++){//面板大小和棋盘一致，但格子线条比棋盘的行列少1
        cot.moveTo((widthAndHeight*i)+offset,0+offset);
        cot.lineTo((widthAndHeight*i)+offset,(col*widthAndHeight)-offset);
    }
    for(var j=0;j<col;j++){
        cot.moveTo(0+offset,(widthAndHeight*j)+offset);
        cot.lineTo((widthAndHeight*row)-offset,(j*widthAndHeight)+offset);
    }    
    cot.stroke();
    $("#background").prepend(canvas);
    //生成格子横线
//    var b_str="";
//    for(var i=0;i<(row-1);i++){
//        for(var j=0;j<(col-1);j++){
//            b_str+="<div class='b_grid'></div>";
//        }
//    }
//    $("#back_grid").append(b_str);
//    $("#back_grid").css({width:((row-1)*widthAndHeight)+"px",height:(col-1)*widthAndHeight+"px",position: "absolute",top:(widthAndHeight/2)+"px",left:(widthAndHeight/2)+"px",border:"solid 1px black"});
//    //减去线的宽度
//    $(".b_grid").css({width:(widthAndHeight-2)+"px",height:(widthAndHeight-2)+"px",border:"solid 1px black"});
    //生成落子格子
    var str="";
    var index = 0;
    for(var i=0;i<row;i++){
        for(var j=0;j<col;j++){
            str+="<div class='grid' id=\""+index+"\"></div>";
            index++;
        }
    }
    $("#chess").empty();
    $("#chess").append(str);
    $("#chess").css({width:(row*widthAndHeight)+"px",height:(col*widthAndHeight)+"px",position: "absolute",top:"0px",left:"0px","z-index":99999});
    $(".grid").on("click",function(){
        WuZiQi.playchess(this);
    });
    $(".grid").css({width:widthAndHeight+"px",height:widthAndHeight+"px"});

});

function get_new(){
    var rst = '';
    $.get("/get_chess",function(rtnFromSvr){
        rst = rtnFromSvr;
    })
    var anti_color = 'black';
    if (color == 'black') {
        anti_color = 'white';
    }
    if (rst != '-1' && rst != '') {
        // $("#messageContent").append("系统：已落子!");
        $("#"+rst).html("<div class=\"chessman "+anti_color+"\"></div>");
        WuZiQi.isEnd(rst,anti_color)
    }
    return rst;
}
setInterval("get_new()",1000);

function get_all(){
    var rst = '';
    $.get("/get_all_black_chess",function(rtnFromSvr){
        rst = rtnFromSvr;
    })
    if (rst == '-2') {
        $("#messageContent").append("系统：已断开连接");
        alert("掉线");
    }
    if (rst != '') {
        rst = rst.split(',')
        for (var i = 0; i < rst.length; i++) {
            $("#"+rst[i]).html("<div class=\"chessman "+"black"+"\"></div>");
        }
    }


    rst = '';
    $.get("/get_all_white_chess",function(rtnFromSvr){
        rst = rtnFromSvr;
    })
    if (rst == '-2') {
        $("#messageContent").append("系统：已断开连接");
        alert("掉线");
    }
    if (rst != '') {
        rst = rst.split(',')
        for (var i = 0; i < rst.length; i++) {
            $("#"+rst[i]).html("<div class=\"chessman "+"white"+"\"></div>");
        }
    }

}

get_all();