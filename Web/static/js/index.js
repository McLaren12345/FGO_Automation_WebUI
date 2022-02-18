$(function () {
    init_script_preview_list();
    init_all_info();
    setInterval(() => {
        refresh_info();
    }, 10000)

});

$.hulla = new hullabaloo();

function raise_info(operation, success_info, json_data) {
    var result = json_data.success;
    if (result == true) {
        $.hulla.send(success_info, "success");
    } else {
        $.hulla.send(operation + " failed. ErrMsg: " + json_data.msg, 'danger');
    }
}

function init_script_preview_list() {
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', '/script/all', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析

            var file_list = json.result;
            var selector = document.getElementById("script_selector");
            selector.options.length = 0;
            for (var i = 0; i < file_list.length; i++) {
                selector.options.add(new Option(file_list[i], i));
            }
        }
    }
}

function friend_point_summon_on_click() {
    document.getElementById("script_selector").disabled = true;
    document.getElementById("servant_selector").disabled = true;
    document.getElementById("battle_times").disabled = true;
}

function battle_on_click() {
    document.getElementById("script_selector").disabled = false;
    document.getElementById("servant_selector").disabled = false;
    document.getElementById("battle_times").disabled = false;
}

function create_task() {
    var type_ = $("input[name='radio']:checked").val();
    var script_name = document.getElementById("script_selector").options[document.getElementById("script_selector").selectedIndex].text;
    var servant = document.getElementById("servant_selector").options[document.getElementById("servant_selector").selectedIndex].text;
    var times = document.getElementById("battle_times").value;

    var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
    httpRequest.open('POST', '/task/create', true); //第二步：打开连接
    httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
    httpRequest.send("type=" + type_ + "&times=" + times + "&servant=" + servant + "&script_name=" + script_name);//发送请求 将情头体写在send中
    /**
     * 获取数据后的处理程序
     */
    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            raise_info("Task create", "Task create successfully.", json);
            refresh_info();
        }
    };
}

function task_action(action) {
    var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
    httpRequest.open('POST', '/task/' + action, true); //第二步：打开连接
    httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
    httpRequest.send();//发送请求 将情头体写在send中
    /**
     * 获取数据后的处理程序
     */
    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            raise_info("Task " + action, "Task " + action + " successfully.", json);
            refresh_info();
        }
    };
}

function stop_task() {
    task_action("stop")
}

var friend_summon_alert_first_time = true;

function start_task() {
    if (document.getElementById("task_type").innerText == "Summon" && friend_summon_alert_first_time) {
        if (!confirm("Please confirm that your game is currently on the friend point summon interface, otherwise this task might lead to permanent losses if on other summon interfaces.")) {
            $.hulla.send("Friend point summon cancelled.", 'info');
            return;
        }
        friend_summon_alert_first_time = false;
    }
    task_action("start")
}

function pause_task() {
    task_action("pause")
}

function formatSeconds(value) {
    let result = parseInt(value);
    let h = Math.floor(result / 3600) < 10 ? '0' + Math.floor(result / 3600) : Math.floor(result / 3600);
    let m = Math.floor((result / 60 % 60)) < 10 ? '0' + Math.floor((result / 60 % 60)) : Math.floor((result / 60 % 60));
    let s = Math.floor((result % 60)) < 10 ? '0' + Math.floor((result % 60)) : Math.floor((result % 60));

    let res = '';
    if (h !== '00') res += `${h}h`;
    if (m !== '00') res += `${m}min`;
    res += `${s}s`;
    return res;
}

function init_all_info() {
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', '/status', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            document.getElementById("current_device").innerText = json.dev_serial_no;
            if (json.device_status) {
                document.getElementById("device_status").innerHTML = "<font color=\"#009933\">Connected</font>"
            } else {
                document.getElementById("device_status").innerHTML = "<font color=\"#FF0000\">Disconnected</font>"
            }
            document.getElementById("task_type").innerText = json.taskType.slice(0, 1).toUpperCase() + json.taskType.slice(1).toLowerCase();
            document.getElementById("task_status").innerText = json.taskStatus;
            document.getElementById("err_msg_content").innerText = json.errMsg;
            document.getElementById("craft_drop_num").innerText = json.craftDropped;
            document.getElementById("crystal_stone_used").innerText = json.itemUsage.CrystalStone;
            document.getElementById("gold_apple_used").innerText = json.itemUsage.GoldApple;
            document.getElementById("silver_apple_used").innerText = json.itemUsage.SilverApple;
            document.getElementById("bronze_apple_used").innerText = json.itemUsage.BronzeApple;
            document.getElementById("battle_times").value = json.totalTimes;
            document.getElementById("battle_finished").innerText = (json.totalTimes - json.remainingTime) + "/" + json.totalTimes;
            document.getElementById("process_bar").max = json.totalTimes;
            document.getElementById("process_bar").value = (json.totalTimes - json.remainingTime);
            document.getElementById("last_battle_time_usage").innerText = formatSeconds(json.lastBattleTimeUsage);
            document.getElementById("time_remaining").innerText = formatSeconds(json.timeLeft);

            for (var i = 0; i < document.getElementById("servant_selector").options.length; i++) {
                if (document.getElementById("servant_selector").options[i].value == json.servant) {
                    document.getElementById("servant_selector").selectedIndex = i;
                    break;
                }
            }
            if (json.scriptName != ".json") {
                for (var i = 0; i < document.getElementById("script_selector").options.length; i++) {
                    if (document.getElementById("script_selector").options[i].value == json.servant) {
                        document.getElementById("script_selector").selectedIndex = i;
                        break;
                    }
                }
            }

            $("input[name='radio']").each(function (index) {
                if ($("input[name='radio']").get(index).value == json.taskType) {
                    $("input[name='radio']").get(index).checked = true;
                    $("input[name='radio']").get(index).onclick();
                }
            });

        }
    }
}

function refresh_info() {
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', '/status', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            document.getElementById("current_device").innerText = json.dev_serial_no;
            if (json.device_status) {
                document.getElementById("device_status").innerHTML = "<font color=\"#009933\">Connected</font>"
            } else {
                document.getElementById("device_status").innerHTML = "<font color=\"#FF0000\">Disconnected</font>"
            }
            document.getElementById("task_type").innerText = json.taskType.slice(0, 1).toUpperCase() + json.taskType.slice(1).toLowerCase();
            document.getElementById("task_status").innerText = json.taskStatus;
            document.getElementById("err_msg_content").innerText = json.errMsg;
            if (document.getElementById("craft_drop_num").innerText != json.craftDropped) {
                $.hulla.send("Detect new craft dropped!!!", 'info');
            }
            document.getElementById("craft_drop_num").innerText = json.craftDropped;
            document.getElementById("crystal_stone_used").innerText = json.itemUsage.CrystalStone;
            document.getElementById("gold_apple_used").innerText = json.itemUsage.GoldApple;
            document.getElementById("silver_apple_used").innerText = json.itemUsage.SilverApple;
            document.getElementById("bronze_apple_used").innerText = json.itemUsage.BronzeApple;
            //document.getElementById("battle_times").value = json.totalTimes
            document.getElementById("battle_finished").innerText = (json.totalTimes - json.remainingTime) + "/" + json.totalTimes;
            document.getElementById("process_bar").max = json.totalTimes;
            document.getElementById("process_bar").value = (json.totalTimes - json.remainingTime);
            document.getElementById("last_battle_time_usage").innerText = formatSeconds(json.lastBattleTimeUsage);
            document.getElementById("time_remaining").innerText = formatSeconds(json.timeLeft)

        }
    }
}