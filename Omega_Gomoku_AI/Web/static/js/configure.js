function request(url, json, successCallback) {
    var XHR = new XMLHttpRequest();
    XHR.open("POST", url);
    XHR.setRequestHeader('content-type', 'application/json');
    XHR.send(JSON.stringify(json));
    XHR.onreadystatechange = function () {
        if (XHR.readyState === 4 && XHR.status === 200) {
            successCallback(XHR.responseText);
        }
    }
}


const select_row5_html = function (section, list) {
    const head = "<h4 id=\"select" + section + "-5-title\">" + section +
        "-5. 请选择想要使用的网络模型。 Please select the network model you want to use.</h4>\n";
    let content = "";
    for(let i = 0; i < list.length; i++)
    {
        content += "<label><input type='radio' " + "id='select" + section + "-5-input-" + (i+1) + "'" +
            " onclick='selected(" + section + ", 5, " + (i+1) + ")' name='select" + section + "-5' value='" + (i+1) + "'>" +
            list[i] + "</label><br>";
    }
    return head + content;
};

const select_row6_html = function (section, list) {
    const head = "<h4 id=\"select" + section + "-6-title\">" + section +
        "-6. 请选择想要使用的模型记录。 Please select the model record you want to use.</h4>\n";
    let content = "";
    for(let i = 0; i < list.length; i++)
    {
        content += "<label><input type='radio' " + "id='select" + section + "-6-input-" + (i+1) + "'" +
            " onclick='selected(" + section + ", 6, " + (i+1) + ")' name='select" + section + "-6' value='" + (i+1) + "'>" +
            list[i] + "</label><br>";
    }
    return head + content;
};


function enable(displayid, ableid) {
    document.getElementById(displayid).style.display = "block";
    if (document.getElementById(ableid)) {
        document.getElementById(ableid).required = true;
    }
}

function disable(displayid, ableid) {
    document.getElementById(displayid).style.display = "none";
    if (document.getElementById(ableid)) {
        document.getElementById(ableid).required = false;
    }
}

function is_radio_checked(name) {
    let radio = document.getElementsByName(name);
    if (!radio) {
        return false
    }
    for (let one_option of radio)
    {
        if (one_option.checked) {
            return true
        }
    }
    return false
}


function selected(section, row, value) {
    switch (row) {
        case 0:
            document.getElementById("select" + section + "-1").style.display = "block";
            switch (value) {
                case 1: // Human
                    disable("select" + section + "-2", "select" + section + "-2-input");
                    disable("select" + section + "-3", "select" + section + "-3-input");
                    disable("select" + section + "-4", "select" + section + "-4-input");
                    disable("select" + section + "-5", "select" + section + "-5-input-1");
                    disable("select" + section + "-6", "select" + section + "-6-input-1");
                    break;
                case 2: // pure MCTS AI
                    enable("select" + section + "-2", "select" + section + "-2-input");
                    enable("select" + section + "-3", "select" + section + "-3-input");
                    disable("select" + section + "-4", "select" + section + "-4-input");
                    disable("select" + section + "-5", "select" + section + "-5-input-1");
                    disable("select" + section + "-6", "select" + section + "-6-input-1");
                    break;
                case 3: // neural network AI
                    enable("select" + section + "-2", "select" + section + "-2-input");
                    enable("select" + section + "-3", "select" + section + "-3-input");
                    enable("select" + section + "-4", "select" + section + "-4-input");
                    if (is_radio_checked("select" + section + "-4"))
                        enable("select" + section + "-5", "select" + section + "-5-input-1");
                    if (is_radio_checked("select" + section + "-5"))
                        enable("select" + section + "-6", "select" + section + "-6-input-1");
                    break;
            }
            break;
        case 4:
            enable("select" + section + "-5", "select" + section + "-5-input-1");
            document.getElementById("select" + section + "-5").innerHTML = "<h4>加载中... Loading...</h4>";
            request("/configure/models", {"player" : section - 1, "network" : value}, function (responseText) {
                let arr = JSON.parse(responseText);
                document.getElementById("select" + section + "-5").innerHTML = select_row5_html(section, arr);
                enable("select" + section + "-5", "select" + section + "-5-input-1");
            });
            break;
        case 5:
            enable("select" + section + "-6", "select" + section + "-6-input-1");
            document.getElementById("select" + section + "-6").innerHTML = "<h4>加载中... Loading...</h4>";
            request("/configure/records", {"player" : section - 1, "model" : value - 1}, function (responseText) {
                let arr = JSON.parse(responseText);
                document.getElementById("select" + section + "-6").innerHTML = select_row6_html(section, arr);
                enable("select" + section + "-6", "select" + section + "-6-input-1");
            });
            break;
    }
}


function validateForm() {
    for (let i = 1; i <= 2; i++)
    {
        const select0 = document.forms["configure"]["select" + i + "-0"].value;
        const select1 = document.forms["configure"]["select" + i + "-1"].value;
        if (select0 === "" || select1 === "")
        {
            alert("选项 " + i + " 或 " + i + "-1 未填写\n" +
                "select " + i + " or " + i + "-1 unfilled.");
            return false;
        }
        if (select0 !== "1")
        {
            try {
                const select2 = document.forms["configure"]["select" + i + "-2"].value;
                const select3 = document.forms["configure"]["select" + i + "-3"].value;
                if (select2 === "" || select3 === "") {
                    alert("选项 " + i + "-2 或 " + i + "-3 未填写\n" +
                        "select " + i + "-2 or " + i + "-3 unfilled.");
                    return false;
                }
            } catch (e) {
                alert("选项 " + i + "-2 或 " + i + "-3 未填写\n" +
                    "select " + i + "-2 or " + i + "-3 unfilled.");
                return false;
            }
        }
        if (select0 === "3")
        {
            try {
                const select4 = document.forms["configure"]["select" + i + "-4"].value;
                const select5 = document.forms["configure"]["select" + i + "-5"].value;
                const select6 = document.forms["configure"]["select" + i + "-6"].value;
                if (select4 === "" || select5 === "" || select6 === "") {
                    alert("选项 " + i + "-4 或 " + i + "-5 或 " + i + "-6 未填写\n" +
                        "select " + i + "-4 or " + i + "-5 or " + i + "-6 unfilled.");
                    return false;
                }
            } catch (e) {
                alert("选项 " + i + "-4 或 " + i + "-5 或 " + i + "-6 未填写\n" +
                    "select " + i + "-4 or " + i + "-5 or " + i + "-6 unfilled.");
                return false;
            }

        }
    }

}