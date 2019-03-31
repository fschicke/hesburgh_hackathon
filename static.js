(function() {

var currentSunday;
var offset;


var newEvent = false;

  $(document).ready(initialize);
  function initialize() {
    currentSunday = new Date();
    initializeDay();
    setDate();
	offset = currentSunday.getDay();
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
    var w = currentSunday.getDay();
    $('#' + w.toString()).attr("checked","checked");
  }


  function setDate() { 

    var m = currentSunday.getMonth()+1;
    var d = currentSunday.getDate();
    var y = currentSunday.getFullYear();
    $('#month').html(m);
    $('#day').html(d);
    $('#year').html(y);

  }

 
  function add7Days() {
    var oneWeekLater = new Date(currentSunday);
    oneWeekLater.setDate(currentSunday.getDate()+7);
    currentSunday = oneWeekLater;
    setDate();
  }

  function subtract7Days() {
    var oneWeekLater = new Date(currentSunday);
    oneWeekLater.setDate(currentSunday.getDate()-7);
    currentSunday = oneWeekLater;
    setDate();
  }


})();
