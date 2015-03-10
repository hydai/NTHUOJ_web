/*
The MIT License (MIT)
Copyright (c) 2014 NTHUOJ team
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/
$('#myTab a').click(function(e) {
    e.preventDefault()
    $('#myTab a[href="#overview"]').tab('show')
    $('#myTab a[href="#problem"]').tab('show')
    $('#myTab a[href="#scoreboard"]').tab('show')
    $('#myTab a[href="#status"]').tab('show')
})

function checkTime(i) {
    if (i < 10) {
        i = "0" + i
    }; // add zero in front of numbers < 10
    return i;
}

function getRestTime() {
    var end = new Date(document.getElementById('end').innerHTML.replace(/-/g, "/"))
    var start = new Date(document.getElementById('start').innerHTML.replace(/-/g, "/"))
    var serverTime = new Date(document.getElementById('server_time').innerHTML.replace(/-/g, "/"));
    if ( serverTime.getTime() < end.getTime()) {
        var result = (end.getTime() - Date.now()) / 1000;
        var s = parseInt(result % 60);
        result /= 60;
        var m = parseInt(result % 60);
        result /= 60;
        var h = parseInt(result % 60);
        m = checkTime(m);
        s = checkTime(s);
        h = checkTime(h);
        var percentage = (Date.now() - start.getTime()) / (end.getTime() - start.getTime());
        document.getElementById('clock').innerHTML = h + ":" + m + ":" + s;
        document.getElementById('timeline').style.width = percentage * 100 + "%";
        var t = setTimeout(function() {
            getRestTime(start, end)
        }, 500);
    } else {
        document.getElementById('timeline').style.width = "100%";
        document.getElementById('clock').innerHTML = "Contest Ended";
    }
}
