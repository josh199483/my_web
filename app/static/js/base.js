$(function () {
    //每次資料有變化就再判斷一次,讓footer的位置正常
    // $(document).ajaxStop(function () { // ajaxStop 
    //     if (parseInt($('body').css('height')) > parseInt($('html').css('height'))) {
    //         $('.footer').offset({
    //             top: parseInt($('body').css('height')),
    //             left: 0,
    //         });
    //     } else if ($('.footer').offset().top < parseInt($('html').css('height'))){
    //         $('.footer').offset({
    //             top: parseInt($('html').css('height')),
    //             left: 0
    //         });
    //     }
    // });
});


// 套用所有 ajax初始設定
$.ajaxSetup({
    cache: false,       // 瀏覽器快取無效
});
