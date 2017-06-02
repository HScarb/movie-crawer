


(function ($) {
    "use strict";
    var mainApp = {
       
        reviews_fun:function()
        {
            ($)(function () {
                $('#carousel-example').carousel({
                    interval: 3000 //TIME IN MILLI SECONDS
                });
            });

        },
     
        custom_fun:function()
        {


            /*====================================
             WRITE YOUR   SCRIPTS  BELOW
            ======================================*/




        },

    }
   
   
    $(document).ready(function () {
        mainApp.reviews_fun();
        mainApp.custom_fun();

    });
}(jQuery));


