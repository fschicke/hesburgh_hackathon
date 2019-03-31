(function() {

var TodayDate;
var currentSunday;
var currentWeekday;

var newEvent = false;

  $(document).ready(initialize);
  function initialize() {
    TodayDate = new Date();
    initializeDay();
    setDate();
    $('#leftDate').click(subtract7Days);
    $('#rightDate').click(add7Days);
    $('#sidebarToggle').click(function() {
        if (!newEvent) {
            newEvent = true;
            $('#newEvent').css("display","none");
        } else {
            $('#newEvent').css("display","block")
            newEvent = false;
        }
    });
  }


  function initializeDay() {
    var w = TodayDate.getDay();
    $('#' + w.toString()).attr("checked","checked");
  }

  function setDate() { 

    var m = TodayDate.getMonth()+1;
    var d = TodayDate.getDate();
    var y = TodayDate.getFullYear();
    $('#month').html(m);
    $('#day').html(d);
    $('#year').html(y);

  }

  


  function add7Days() {
    var oneWeekLater = new Date(TodayDate);
    oneWeekLater.setDate(TodayDate.getDate()+7);
    TodayDate = oneWeekLater;
    setDate();
  }

  function subtract7Days() {
    var oneWeekLater = new Date(TodayDate);
    oneWeekLater.setDate(TodayDate.getDate()-7);
    TodayDate = oneWeekLater;
    setDate();
  }


})();
