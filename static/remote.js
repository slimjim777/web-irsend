var event;
var attendQuery;

$(document).ready(function () {
    //docReady();
});

function clickedOp(device_id, op)
{
    $.ajax({url:'/device/' + device_id + '/clicked/' + op});
}


