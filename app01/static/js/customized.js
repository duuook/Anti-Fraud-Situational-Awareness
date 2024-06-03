import './echarts.min.js';
import $ from './jquery-3.6.0.min.js';

$(document).ready(function () {
    var scrollTable = $('tbody');
    setInterval(function () {
        var scrollPos = scrollTable.scrollTop();
        scrollTable.scrollTop(scrollPos + 1);
    }, 100);  // 每100毫秒滚动一次
});