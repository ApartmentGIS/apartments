$(function(){
    $("#price-slider").noUiSlider({
       range: [3000, 15000],
       start: 3000,
       step: 500,
       connect: "lower",
       handles: 1,
       serialization: {
           resolution: 1,
           to: [
               [$('#price-to'), 'html']
           ]
        }
    });

    $("#kindergarten-slider").noUiSlider({
       range: [100, 1000],
       start: 100,
       step: 100,
       connect: "lower",
       handles: 1,
       serialization: {
           resolution: 1,
           to: [
               [$('#kindergarten-to'), 'html']
           ]
        }
    });

    var checkDisabledKindergartenSlider = function(){
        if($("#kindergarten-check").is(":checked"))
            $("#kindergarten-slider").removeAttr("disabled");
        else
            $("#kindergarten-slider").attr("disabled", "true");
    };

    checkDisabledKindergartenSlider();

    $("#kindergarten-check").change(function(){
        checkDisabledKindergartenSlider();
    });


});