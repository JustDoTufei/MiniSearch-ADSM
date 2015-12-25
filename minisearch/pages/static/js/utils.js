
function parse_to_table(begin_num, data) {
    var ret = "";
    var index_map = [null, 1, 2, 6, 7, 8, 9, 10,11];
    len = data.length;
    
    for (i = 0; i < len; i++) {
        ret += "<tr>";
        for (j in index_map) {
            if (null == index_map[j]) {
                ret += ("<td>" + String(begin_num + i) + "</td>");
            }
			/*
            else if (11 == index_map[j]) {
				ret += ('<td><a href="javascript:void(0);" onclick="show_detail(' + String(i) + ')">' + data[i][index_map[j]] +'</a></td>');
            }*/
			else if ( 2 == index_map[j]){
				ret += ("<td>" + data[i][index_map[j]].substr(0,8) + "</td>");
			}
			else {
                ret += ("<td>" + data[i][index_map[j]] + "</td>");
            }
        }
        ret += "<tr/>";
    }
    
    return ret;
}

function pagination(pages, cur) {
    var ret = "";
    var max_pages = 10;
    
    if (cur < 1) {
        cur = 1;
    } else if (cur > pages) {
        cur = pages;
    }
    
    var show_count = (pages > max_pages) ? max_pages : pages;
    var begin = 0;
    
    if (cur < parseInt(show_count / 2)) {
        begin = 1;
    } else if (cur > pages - parseInt(show_count / 2)) {
        begin = pages - show_count + 1;
    } else {
        begin = cur - parseInt(show_count / 2);
    }
    
    if (begin < 1) begin = 1;
    
    var onclick = 'onclick="page_bar_click(' + String(cur - 1) + ');"';
    
    if (1 == cur) {
        ret += '<li class="disabled"><a href="javascript:void(0);" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>';
    } else {
        ret += '<li><a href="javascript:void(0);" ' + onclick + ' aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>';
    }
    
    for (var i = 0; i < show_count; i++) {
        var num = begin + i;
        onclick = 'onclick="page_bar_click(' + String(num) + ');"';
        
        if (num == cur) {
            ret += '<li class="active"><a href="javascript:void(0);">' + String(num) + '<span class="sr-only">(current)</span></a></li>';
        } else {
            ret += '<li><a href="javascript:void(0);" ' + onclick + '>' + String(num) + '</a></li>';
        }
    }
    
    onclick = 'onclick="page_bar_click(' + String(cur + 1) + ');"';
    if (cur == pages) {
        ret += '<li class="disabled"><a href="javascript:void(0);" aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>';
    } else {
        ret += '<li><a href="javascript:void(0); "' + onclick + ' aria-label="Next"><span aria-hidden="true">&raquo;</span></a></li>';
    }
    
    return ret;
}
