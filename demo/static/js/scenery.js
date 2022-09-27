 window.onload = function()
  {
      var oDiv = document.getElementById("div1");
      var oUl = document.getElementsByTagName("ul")[0];
      var oLi = document.getElementsByTagName("li");
      var oA = document.getElementsByTagName("a");
      var timer = null;
      var iSpeed = 3;
      //复制一遍ul
      oUl.innerHTML +=oUl.innerHTML;
      //ul的宽度是所有li宽度之和，复制ul之后的整个ul的宽度就是li的长度乘以一个li的宽度
      oUl.style.width = oLi.length*oLi[0].offsetWidth + "px";
      function fnMove()
      {
          //图片向左移动时的条件，即在div里的ul的offsetLeft小于一个ul的宽度
          if (oUl.offsetLeft<-oUl.offsetWidth/2)
          {
              //将整个复制的ul向右拖拽直至整个ul中的第一张图归位到起点
              oUl.style.left = 0;
          }
          //图片向右移动时的条件，即在div里的ul的offsetLeft大于等于0
          else if (oUl.offsetLeft>=0)
         {
              //将整个复制的ul向左拖拽直至整个ul中的第一张图归位到起点
             oUl.style.left = -oUl.offsetWidth/2 + "px";
          }
          //给ul一个速度让整个ul的offsetLeft增加或减少，速度为正则向右移动，速度为负则向左移动
          oUl.style.left = oUl.offsetLeft +iSpeed + "px";
     }
      //点击向左滚动即触发第一个a元素标签
      oA[4].onclick = function()
      {
          iSpeed = -3;
      }
      //点击向右滚动即触发第二个a元素标签
      oA[5].onclick = function()
      {
          iSpeed = 3;
      }
      //当鼠标移动到div里面的时候图片滚动暂停，此时清除定时器即可。
      oDiv.onmouseover = function()
      {
         clearInterval(timer);
     }
      //当鼠标移出div的时候图片继续滚动，此时重新加载定时器。
     oDiv.onmouseout = function()
      {
          timer=setInterval(fnMove,30);
      }
  }