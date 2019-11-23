$(document).ready(function () {
    $('.tablas div').hide();
    $('.tablas div:first').show()

    $('ul.nav-tabs li a').click(function () {
        $('.tablas div').hide();
        $('ul.nav-tabs li a').removeClass('active');
        $(this).addClass('active')
        var activeTab = $(this).attr('href')
        $(activeTab).show();
        return false;
    })
});
