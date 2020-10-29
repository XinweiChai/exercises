window.onload=function(){

function Createselect(id1,id2,id3,json){
      //数据
      this.province=json[id1];
      this.city=json[id2];
      this.county=json[id3];

      //选择框
     this.provinceBox=document.getElementById(id1);
     this.cityBox=document.getElementById(id2);
     this.countyBox=document.getElementById(id3);
     this.ts="---请选择---";
}

Createselect.prototype={
      init:function(){
          this.provinceBox.options[0]=new Option(this.ts);
          this.cityBox.options[0]=new Option(this.ts);
          this.countyBox.options[0]=new Option(this.ts);
          this.createCun();
          this.createCity(-1);
          this.createXian(-1,-1);
      },
      createCun:function(){
              var This=this;
              for(var i=0;i<This.province.length;i++){
                     This.provinceBox.options[i+1]=new Option(This.province[i],This.province[i]);
              }
              This.provinceBox.onchange=function(){
                    This.createCity(This.provinceBox.selectedIndex);
                    This.createXian(-1,-1);
              }

      },
     createCity:function(num){
           var This=this;
            if(num<=0){
                This.cityBox.length=1;
                This.cityBox.disabled=true;
                This.cityBox.options[0]=new Option(This.ts)
            }else{
                This.cityBox.length=1;
                This.cityBox.disabled=false;
                var cit=This.province[num-1];
                var arr=This.city[cit];
                for(var i=0;i<arr.length;i++){
                   This.cityBox.options[i+1]=new Option(arr[i],arr[i]);
                }

            }
            This.cityBox.onchange=function(){
                    This.createXian(num,This.cityBox.selectedIndex);
            }

        },
        createXian:function(snum,xin){
                var This=this;
                if(snum<=0||xin<=0){
                    This.countyBox.length=1;
                    This.countyBox.disabled=true;
                    This.countyBox.options[0]=new Option(This.ts)
                    return;
                }else{
                    This.countyBox.length=1;
                    This.countyBox.disabled=false;
                    var qnum=snum-1;
                    var sxin=xin-1;
                    var cit=This.city[This.province[qnum]][sxin];
                    var arr=This.county[qnum][cit];
                    for(var i=0;i<arr.length;i++){
                       This.countyBox.options[i+1]=new Option(arr[i],arr[i]);
                    }
                }
                //获取值
               //  This.countyBox.onchange=function(){
               //      alert(This.getValue());
               // }

         },
         getValue:function(){
              var This=this;
              var val=This.provinceBox.value+","+This.cityBox.value+","+This.countyBox.value;
              return val;
         }

}

/*

  数据一共分为3级并且每一级的数据要一一对应，每一级的数据名字于对应id名字相同。

*/

// var json={
//                province:["北京","上海"],//第一级

//                city :{              //第二级

//                     "北京":["海淀","延庆","朝阳","丰台"],
//                     "上海":["浦东","浦西","虹口","外滩"]
//                },

//                county:[                //第三级

//                     {
//                       "海淀":["海淀上","海淀下","海淀中"],
//                       "延庆":["延庆上","延庆下","延庆中","延庆下下","延庆中中"],
//                       "朝阳":["朝阳上","朝阳下","朝阳中"],
//                       "丰台":["丰台上","丰台下","丰台中","丰台中中"]

//                     },
//                     {
//                       "浦东":["浦东上","浦东下","浦东中"],
//                       "浦西":["浦西上","浦西下","浦西中"],
//                       "虹口":["虹口上","虹口下","虹口中","虹口上上","虹口下下","虹口中中"],
//                       "外滩":["外滩上","外滩下","外滩中"]
//                     }

//               ]
//     };

var json={
               province:["江苏"],//第一级

               city :{              //第二级

                    "江苏":["泰州"]
               },

               county:[                //第三级

                    {
                      "泰州":["姜堰市"]
                    }
              ]
    };


var cres=new Createselect("province","city","county",json);
cres.init();

}