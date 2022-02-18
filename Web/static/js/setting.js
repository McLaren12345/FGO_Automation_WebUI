$(function () {
    init_selector(1);
    init_config();
    reset_script();
    init_script_preview_list();
    document.getElementById("script_name").value = "";
    document.getElementById("Force_overwrite").checked = false;
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

function init_selector(flag) {
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', '/device', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中

    if (flag == 1) {
        $.hulla.send("Refreshing devices, please wait.", 'info');
    }

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析

            var current_device = json.result.current_device;
            var device_list = json.result.device_list;
            var selector = document.getElementById("device_selector");
            selector.options.length = 0;
            for (var i = 0; i < device_list.length; i++) {
                selector.options.add(new Option(device_list[i], i));
            }
            if (device_list.length != 0) {
                selector.getElementsByTagName("option")[current_device].selected = true;
            }
            if (flag == 1) {
                raise_info("Device update", "Device updated successfully. " + device_list.length + " device(s) detected.", json);
            }
        }
    }
}

function init_config() {
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', '/config', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            var config = json.conf_map;

            document.getElementById("email_enable").checked = config.email_notice;
            document.getElementById("email_address").value = config.email;
            document.getElementById("email_password").value = config.passwd;
            document.getElementById("crystal_stone").checked = config.use_Crystal_stone;
            document.getElementById("gold_apple").checked = config.use_Gold_apple;
            document.getElementById("silver_apple").checked = config.use_Silver_apple;
            document.getElementById("bronze_apple").checked = config.use_Bronze_apple;
        }
    }
}

function connect_device_func() {
    var selector = document.getElementById("device_selector");
    var index = selector.selectedIndex;
    if (selector.value == '') {
        $.hulla.send("No device selected.", 'warning');
        return;
    }

    $.hulla.send("Connecting device, please wait.", 'info');

    var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
    httpRequest.open('POST', '/device', true); //第二步：打开连接
    httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）
    httpRequest.send("serial_no=" + selector.options[index].text);//发送请求 将情头体写在send中
    /**
     * 获取数据后的处理程序
     */
    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            raise_info("Device connect", "Device connect successfully.", json);
        }
    };
}

function submit_func() {
    var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
    httpRequest.open('POST', '/config', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
    httpRequest.setRequestHeader("Content-type", "application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };

    var newConfig = {
        "email_notice": document.getElementById("email_enable").checked,
        "email": document.getElementById("email_address").value,
        "passwd": document.getElementById("email_password").value,
        "use_Crystal_stone": document.getElementById("crystal_stone").checked,
        "use_Gold_apple": document.getElementById("gold_apple").checked,
        "use_Silver_apple": document.getElementById("silver_apple").checked,
        "use_Bronze_apple": document.getElementById("bronze_apple").checked
    };
    httpRequest.send(JSON.stringify(newConfig));//发送请求 将json写入send中

    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            raise_info("Configuration update", "Configuration update successfully.", json);
        }

    };

}


function test_email_func() {
    if (document.getElementById("email_enable").checked == false) {
        $.hulla.send("Please enable email notice first.", 'warning');
        return;
    }
    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', '/test_email', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中

    $.hulla.send("Sending email, please wait.", 'info');

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            raise_info("Send email", "Email send successfully.", json);
        }
    }
}

var global_script_template = {"MysticCodes": "", "Turns": []};

function reset_script() {
    document.getElementById("character_skill").value = "";
    document.getElementById("master_skill").value = "";
    document.getElementById("card_selector").getElementsByTagName("option")[0].selected = true;
    document.getElementById("mystic_code_selector").getElementsByTagName("option")[0].selected = true;

    var new_script = global_script_template;
    var selector = document.getElementById("mystic_code_selector");
    var index = selector.selectedIndex;
    new_script.MysticCodes = selector.options[index].value;
    document.getElementById("script_viewer").value = JSON.stringify(new_script, undefined, 2);
}


function undo_script() {
    var current_script = jQuery.parseJSON(document.getElementById("script_viewer").value);
    if (current_script.Turns.length == 0) {
        return;
    }
    var last_turn = current_script.Turns[current_script.Turns.length - 1];
    current_script.Turns.pop();
    document.getElementById("script_viewer").value = JSON.stringify(current_script, undefined, 2);
    document.getElementById("character_skill").value = JSON.stringify(last_turn.character_skill);
    document.getElementById("master_skill").value = JSON.stringify(last_turn.master_skill);
    document.getElementById("card_selector").getElementsByTagName("option")[last_turn.card - 1].selected = true;

}


function mystic_code_on_change() {
    var current_script = jQuery.parseJSON(document.getElementById("script_viewer").value);
    var mystic_code_selector = document.getElementById("mystic_code_selector");
    var mystic_code_index = mystic_code_selector.selectedIndex;
    current_script.MysticCodes = mystic_code_selector.options[mystic_code_index].value;
    document.getElementById("script_viewer").value = JSON.stringify(current_script, undefined, 2);
}

function add_to_script() {
    var character_skill_list = document.getElementById("character_skill").value.replace(/\s*/g, "");
    var master_skill_list = document.getElementById("master_skill").value.replace(/\s*/g, "");

    if (character_skill_list.substr(0, 2) != "[[") {
        if (character_skill_list == "" || character_skill_list == "[]") {
            character_skill_list = "[]"
        } else {
            $.hulla.send("Wrong skill list format. Expected to be list of list.", 'warning');
            return;
        }
    }
    if (character_skill_list.substr(2, 1) == "[" || character_skill_list.substr(2, 1) == "]") {
        $.hulla.send("Wrong skill list format. Expected to be list of list. Or empty list contained.", 'warning');
        return;
    }
    if (master_skill_list.substr(0, 2) != "[[") {
        if (master_skill_list == "" || master_skill_list == "[]") {
            master_skill_list = "[]"
        } else {
            $.hulla.send("Wrong skill list format. Expected to be list of list.", 'warning');
            return;
        }
    }
    if (master_skill_list.substr(2, 1) == "[" || master_skill_list.substr(2, 1) == "]") {
        $.hulla.send("Wrong skill list format. Expected to be list of list. Or empty list contained.", 'warning');
        return;
    }
    try {
        json_character_skill_list = jQuery.parseJSON(character_skill_list);
        json_master_skill_list = jQuery.parseJSON(master_skill_list);
    } catch (e) {
        $.hulla.send("Phrase JSON error: " + e, 'danger');
    }

    for (var i = 0; i < json_character_skill_list.length; i++) {
        var temp_list = json_character_skill_list[i];
        if (temp_list.length > 3 || temp_list.length < 2) {
            $.hulla.send("Invalid syntax. Character skill parameters list's length shouldn't be large than 3 or less than 2.", 'warning');
            return;
        }
        for (var j = 0; j < temp_list.length; j++) {
            if (temp_list[j] > 3) {
                $.hulla.send("Invalid syntax. Skill parameters shouldn't be large than 3.", 'warning');
                return;
            }
        }
    }
    for (var i = 0; i < json_master_skill_list.length; i++) {
        var temp_list = json_master_skill_list[i];
        if (temp_list.length > 3) {
            $.hulla.send("Invalid syntax. Skill parameters list length shouldn't be large than 3.", 'warning');
            return;
        }
        for (var j = 0; j < temp_list.length; j++) {
            if (temp_list[j] > 3) {
                $.hulla.send("Invalid syntax. Skill parameters shouldn't be large than 3.", 'warning');
                return;
            }
        }
    }
    var current_script = jQuery.parseJSON(document.getElementById("script_viewer").value);

    var selector = document.getElementById("card_selector");
    var index = selector.selectedIndex;

    var mystic_code_selector = document.getElementById("mystic_code_selector");
    var mystic_code_index = mystic_code_selector.selectedIndex;
    current_script.MysticCodes = mystic_code_selector.options[mystic_code_index].value;

    var new_turn = {
        "character_skill": json_character_skill_list,
        "master_skill": json_master_skill_list,
        "card": Number(selector.options[index].value)
    };

    current_script.Turns.push(new_turn);
    document.getElementById("script_viewer").value = JSON.stringify(current_script, undefined, 2);

    document.getElementById("character_skill").value = "";
    document.getElementById("master_skill").value = "";
//    document.getElementById("card_selector").getElementsByTagName("option")[0].selected=true;
}


function save_script() {
    var httpRequest = new XMLHttpRequest();//第一步：创建需要的对象
    httpRequest.open('POST', '/script/save', true); //第二步：打开连接/***发送json格式文件必须设置请求头 ；如下 - */
    httpRequest.setRequestHeader("Content-type", "application/json");//设置请求头 注：post方式必须设置请求头（在建立连接后设置请求头）var obj = { name: 'zhansgan', age: 18 };

    if (document.getElementById("script_name").value == "") {
        $.hulla.send("Script file name is not specified.", 'warning');
        return;
    }

    var newScript = {
        "script": jQuery.parseJSON(document.getElementById("script_viewer").value),
        "script_name": document.getElementById("script_name").value,
        "force_overwrite": document.getElementById("Force_overwrite").checked
    };
    httpRequest.send(JSON.stringify(newScript));//发送请求 将json写入send中

    httpRequest.onreadystatechange = function () {//请求后的回调接口，可将请求成功后要执行的程序写在其中
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {//验证请求是否发送成功
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            raise_info("Save battle script", "Battle script save successfully.", json);
            init_script_preview_list();
        }

    };
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
            if (file_list.length != 0) {
                preview_script_on_change();
            } else if (file_list.length == 0) {
                document.getElementById("script_viewer2").value = "";
                document.getElementById("script_viewer3").value = "";
            }
        }
    }
}

function preview_script_on_change() {
    var selector = document.getElementById("script_selector");
    var index = selector.selectedIndex;
    var script_name = selector.options[index].text;

    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('GET', '/script/single?script_name=' + script_name.substr(0, script_name.length - 5), true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.send();//第三步：发送请求  将请求参数写在URL中

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            var script = json.result;
            document.getElementById("script_viewer2").value = JSON.stringify(script, undefined, 2);
            phrase_script(script);
        }
    }
}

function phrase_script(script) {
    content = "Mystic Code: " + script.MysticCodes;
    for (var i = 0; i < script.Turns.length; i++) {
        content = content + "\n" + "Turn" + (i + 1) + ":\n" +
            "  Character skill: " + JSON.stringify(script.Turns[i].character_skill) + "\n" +
            "  Master skill: " + JSON.stringify(script.Turns[i].master_skill) + "\n" +
            "  Noble phantasm to press: " + script.Turns[i].card;
    }
    document.getElementById("script_viewer3").value = content;
}

function confirm_del() {
    if (confirm("Confirm to delete specified script file?")) {
        delete_script();
    }
}

function delete_script() {
    var selector = document.getElementById("script_selector");
    var index = selector.selectedIndex;
    var script_name = selector.options[index].text;

    var httpRequest = new XMLHttpRequest();//第一步：建立所需的对象
    httpRequest.open('POST', '/script/delete', true);//第二步：打开连接  将请求参数写在url中  ps:"./Ptest.php?name=test&nameone=testone"
    httpRequest.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
    httpRequest.send('script_name=' + script_name.substr(0, script_name.length - 5),);//第三步：发送请求  将请求参数写在URL中

    httpRequest.onreadystatechange = function () {
        if (httpRequest.readyState == 4 && httpRequest.status == 200) {
            var json = jQuery.parseJSON(httpRequest.responseText);//获取到json字符串，还需解析
            raise_info("Delete battle script", "Battle script delete successfully.", json);
            init_script_preview_list();
        }
    }
}

function email_validation() {
    let textBox = document.getElementById("email_address").value;
    let re = /^\w+@[a-zA-Z0-9]{2,10}(?:\.[a-z]{2,4}){1,3}$/;
	//判断检测这个值是否正确，
	if (re.test(textBox) || textBox == "") { //如果验证正确执行以下代码
		document.getElementById("email_validation").innerHTML = '';
	} else { //验证不成功，执行以下代码
		document.getElementById("email_validation").innerHTML = "<font color=\"#FF0000\">Invalid email address!</font>";
	}
}