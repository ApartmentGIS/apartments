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
    });

    function init(){
        var freeHeight = $(window).height() - $(".navbar").height();

        $("#map").css("height", freeHeight - 2);
    }

    $(window).on("resize", function(){
        init();
    });

    $(".toggle-filter-form").on("click", function(){
        var aClose = '<a>Закрыть фильтр <i class="glyphicon glyphicon-resize-small"></i></a>',
            aOpen = '<a>Открыть фильтр <i class="glyphicon glyphicon-resize-small"></i></a>',
            filterForm = $(document).find(".filter-form");

        if(filterForm.is(":hidden")){
            filterForm.show();
            $(this).html(aClose);
        }
        else{
            filterForm.hide();
            $(this).html(aOpen);
        };
    });

    init();
});