jQuery( document ).ready(function($){

    //Закладки http://prntscr.com/okdp9c --------------------------------------------------------------------------------------------------------------
    $(".tab-section li").click(function () {
        $(".tab-section li").removeClass('tab-section-active');
        $(this).addClass('tab-section-active');
    });

     //Выбор месяца и года http://prntscr.com/okdpyw --------------------------------------------------------------------------------------------------------------
    $(".mp-month").click(function () {
        $(".mp-month").removeClass('active');
        $(this).addClass('active');
    });
    $(".mp-year").click(function () {
        $(".mp-year").removeClass('active');
        $(this).addClass('active');
    });

    //Всплывалка выбора года http://prntscr.com/okdtu1 --------------------------------------------------------------------------------------------------------------
    $(".month-item").click(function () {
        $(this).toggleClass('mp-open');
        $(".month-picker").slideToggle(100);
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest(".month-item").length && !$(e.target).closest(".month-picker").length ) {
            $('.month-picker').hide();
            $(".month-item").removeClass('mp-open');
        }
        e.stopPropagation();
    });

    // Скрипт замены стандартного селекта http://prntscr.com/okdutz  http://prntscr.com/okdv5i--------------------------------------------------------------------------------------------------------------
    $('.fs-select').selectize({
        placeholder: 'Kaikki käyttäjät',
    });
    $('.rv-select').selectize({
        placeholder: 'Valitse...',
    });
    $('.select').selectize();

    // Всплывалка фильтра http://prntscr.com/okdvop --------------------------------------------------------------------------------------------------------------
    $(".fs-filter").click(function () {
        $(".fs-filter-container").slideToggle(100);
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest(".fs-filter-block").length ) {
            $('.fs-filter-container').fadeOut();
        }
        e.stopPropagation();
    });

    $(".fs-filter-close").click(function () {
        $('.fs-filter-container').fadeOut();
    });
    
    // Закладки http://prntscr.com/okdwfo --------------------------------------------------------------------------------------------------------------
    $(".fs-tab li").click(function () {
        $(".fs-tab li").removeClass("active");
        $(this).addClass('active');
    });

    //Выбор документа в списке http://prntscr.com/oke25d   --------------------------------------------------------------------------------------------------------------
    $(".receiptItem-choice").click(function () {
        $(".receiptList-content").removeClass('active');
        $(this).parent('.receiptList-content').addClass('active');
    });
    
    // Раскрытие таблицы в мобильной версии  http://prntscr.com/oke4ph --------------------------------------------------------------------------------------------------------------
    if($(window).width() < 1024) {
        $(".summary-flex").click(function () {
            $(this).parents().find('.summary-table').slideToggle(100);
        });
    }

    // В мобильной версии всплывающее окно чека http://prntscr.com/okegos --------------------------------------------------------------------------------------------------------------
    $(".btn-check").click(function () {
        $("#site").addClass('open-receipt-pic');
    });

    $(".icon-close").click(function () {
        $("#site").removeClass('open-receipt-pic');
    });

    // В мобильной версии всплывающее окно заполнения полей http://prntscr.com/okeh3v --------------------------------------------------------------------------------------------------------------
    $(".btn-field").click(function () {
        $("#site").addClass('open-receipt-container');
    });

    $(".icon-close").click(function () {
        $("#site").removeClass('open-receipt-container');
    });

    // Плагин колендаря http://prntscr.com/okehgy --------------------------------------------------------------------------------------------------------------
    $('[data-toggle="datepicker"]').datepicker();


        
});//конец ready