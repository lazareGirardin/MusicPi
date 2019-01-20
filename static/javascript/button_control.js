$(function() {
  $('a#pause').bind('click', function() {
    $.getJSON('/pause_pressed',
        function(data) {
      //do nothing
    });
    return false;
  });
});
$(function() {
  $('a#next').bind('click', function() {
    $.getJSON('/next_pressed',
        function(data) {
          $("#now_playing").text("Now Playing: " + data['now'])
          $("#song1").text(data['0'])
          $("#song2").text(data['1'])
          $("#song3").text(data['2'])
          $("#song4").text(data['3'])
          $("#song5").text(data['4']);
    });
    return false;
  });
});

$(document).ready(function(){
    var socket = io.connect();
    socket.on('song changed', function(data) {
      $("#now_playing").text("Now Playing: " + data['now'])
      $("#song1").text(data['0'])
      $("#song2").text(data['1'])
      $("#song3").text(data['2'])
      $("#song4").text(data['3'])
      $("#song5").text(data['4']);
    });
});
