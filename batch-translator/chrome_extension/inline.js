//document.body.style.backgroundColor="red";
//window.open('http://www.baidu.com', '_blank');

'use strict';

//var CONSOLE = chrome.extension.getBackgroundPage().console;//.log('foo');

//CONSOLE.log('inline.js loaded.');

var g = [];
g.dst = document.getElementById('destText');
g.src = document.getElementById('srcText');
g.exe = document.getElementById('TranslateButton');
g.src_lang = document.querySelector('div.LS_HeaderTitle'); // just get first one.
g.init = false;
g.queue = []

function dest_monitor() {
    try {
        var e = g.dst.children[0].children[0];
        g.id = e.id;
        send(e.innerHTML);
        if (typeof(e.innerHTML) != 'undefined') {
            if (g.init) {
            } else {
                g.queue.push(e.innerHTML);
            }
        }
        var id = setInterval(function() {
          var e = g.dst.children[0].children[0];
          if (e.id != g.id) {
            e.id = g.id;
            //g.result = result;
            //if (g.src_lang.innerHTML.indexOf('English') || g.src_lang.innerHTML.indexOf('Chinese')) {
            //    return
            //}
            send(e.innerHTML);
          }
        }, 500);
        //alert('interval');
    } catch (e) {
        //alert(e.message);
        setTimeout(dest_monitor, 500);
    }
}

function send(message, callback) {
    //alert('send');
    waitForConnection(function () {
        g.websocket.send(message);
        if (typeof callback !== 'undefined') {
          callback();
        }
    }, 500);
};

function waitForConnection(callback, interval) {
    //alert('wait');
    if (g.websocket.readyState === 1) {
        callback();
    } else {
        // optional: implement backoff for interval here
        setTimeout(function () {
            waitForConnection(callback, interval);
        }, interval);
    }
};

function bind_server() {
    var  wsServer = 'ws://127.0.0.1:9001/'; 
    var  websocket = new WebSocket(wsServer); 
    websocket.onopen = function (evt) { onOpen(evt) }; 
    websocket.onclose = function (evt) { onClose(evt) }; 
    websocket.onmessage = function (evt) { onMessage(evt) }; 
    websocket.onerror = function (evt) { onError(evt) }; 

    function onOpen(evt) { 
        //console.log("Connected to WebSocket server."); 
        //alert("Connected to WebSocket server.");
        g.init = true;
        /*if (g.queue.length <= 0) {
            websocket.send('Keith chrome extension from Chrome!');
        } else {
            websocket.send(g.queue.pop());
        }*/
    } 
    function onClose(evt) { 
        //console.log("Disconnected"); 
        alert("Disconnected"); 
    } 
    function onMessage(evt) { 
        //console.log('Retrieved data from server: ' + evt.data); 
        //alert('Retrieved data from server: ' + evt.data);
        g.src.value = evt.data
        dispatch(g.exe, 'click');
    } 
    function onError(evt) { 
        //console.log('Error occured: ' + evt.data); 
        alert('Error occured: ' + evt.data);
    }

    return websocket;
}

function dispatch(element, event) {
    var eObj = document.createEvent('Event');
    eObj.initEvent(event, true, true);
    element.dispatchEvent(eObj);
}

function main() {
    g.websocket = bind_server();
    dest_monitor();
}

main();








