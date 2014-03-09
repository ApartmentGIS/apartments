$(function(){
//    function checkDisabledKindergartenSlider(){
//        if($("#kindergarten-check").is(":checked"))
//            $("#kindergarten-slider").removeAttr("disabled");
//        else
//            $("#kindergarten-slider").attr("disabled", "true");
//    };
//
//    checkDisabledKindergartenSlider();
//
//    $("#kindergarten-check").on("change", function(){
//        checkDisabledKindergartenSlider();
//    });

    $("#id_district_1, #id_rooms_num_1").on("change", function(){
        var self = $(this),
            btnGroup = self.closest(".btn-group");

        if(self.is(":checked")){
            btnGroup.find(".active").removeClass("active").find("input").removeAttr("checked");
        }
    });

    $(".districts, .rooms_nums").find("input:not(#id_district_1, #id_rooms_num_1)").on("change", function(){
        var self = $(this),
            btnGroup = self.closest(".btn-group");

        if(self.is(":checked")){
            btnGroup.find("label").eq(0).removeClass("active").find("input").removeAttr("checked");
        };
    })

});