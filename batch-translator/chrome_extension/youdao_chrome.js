﻿//document.body.style.backgroundColor="red";
//window.open('http://www.baidu.com', '_blank');

'use strict';

var g = [];
g.judge = document.getElementById('translated');
//g.dst = document.querySelector('translated_result');
g.src = document.getElementById('inputText');
g.exe = document.getElementById('translateBtn');
//g.prv = '';

var DEBUG = false;

function l(v) {
    if (DEBUG) console.log(v);
}

function fetch_dest() {
    return document.querySelector('.translated_result');
}

function merge_result(element) {
    //console.log('11');
    //console.log(element);
    var i = 0;
    var len = element.length;
    var result = "";
    while (i < len) {
        var children = element[i];
        //console.log('22');
        //console.log(children);
        var grandChildren = children.children;
        //console.log(grandChildren.length);
        if (grandChildren.length > 0) {
            //console.log('33');
            //console.log(grandChildren);
            result += merge_result(grandChildren);
        } else {
            result += children.innerHTML;
        }
        i += 1;
    }
    //console.log(result);
    return result;
}

function dest_monitor() {
    l('1');
    var dst = fetch_dest();
    if (dst === null || g.judge.getAttribute('style').indexOf('display: none') != -1) {
        setTimeout(dest_monitor, 300);
        return;        
    }
    l('2');
    var children = dst.children;
    var len = children.length;
    if (len == 0) {
        setTimeout(dest_monitor, 300);
        return;
    } else {
        l('3');
        var result = merge_result(children);
        if (result.length === 0/*g.prv === result*/) {
            setTimeout(dest_monitor, 300);
            return;
        }
        l(result);
        if (result.length > 0) {
            //g.prv = result;
            send(result);
            clean();
            setTimeout(dest_monitor, 300);
        } else {
            alert('result is empty?');
        }
    }
}

dest_monitor();

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

function translate(text) {
    g.src.value = text;
    dispatch(g.exe, 'click');
}

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
        translate(evt.data);
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

function clean() {
    var dst = fetch_dest();
    if (dst !== null) dst.remove();
}

function main() {
    clean();
    g.websocket = bind_server();
    dest_monitor();
}

main();



