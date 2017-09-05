// Keith Tu

//console.log('background.js loaded.');

/*function onCompleted(data) {
  console.log(data.url);
  if (data.url.indexOf('www.bing.com/translator') != -1) {
    alert('begin monitor:' + data.url);
    chrome.tabs.executeScript(data.tabId, {file: 'inline.js'});
  }
}*/

function start(tab) {
    /*chrome.tabs.query({active : true}, function (tabs) {
        alert('active!');
        tabs[0]
    }*/

    //alert('start ' + tab.url);

    if (tab.url.indexOf('fanyi.youdao.com') != -1) {
        chrome.tabs.executeScript(tab.id, {file: 'youdao_chrome.js'});
    } else if (tab.url.indexOf('www.bing.com/translator') != -1) {
        chrome.tabs.executeScript(tab.id, {file: 'bing.js'});        
    } else {
        alert('NOT SUPPORTED PAGE.');
    }

    //chrome.webNavigation.onHistoryStateUpdated.addListener(onHistoryStateUpdated_);
    //chrome.webNavigation.onCompleted.addListener(onCompleted);

  //chrome.tabs.executeScript({ file: 'inline.js' });
  //chrome.tabs.executeScript({ code: 'document.body.style.backgroundColor="red"' });
  //chrome.windows.getCurrent(getWindows);
}

// Set up a click handler so that we can merge all the windows.
chrome.browserAction.onClicked.addListener(start);

function bind_server() {
    var  wsServer = 'ws://127.0.0.1:9001/'; 
    var  websocket = new WebSocket(wsServer); 
    websocket.onopen = function (evt) { onOpen(evt) }; 
    websocket.onclose = function (evt) { onClose(evt) }; 
    websocket.onmessage = function (evt) { onMessage(evt) }; 
    websocket.onerror = function (evt) { onError(evt) }; 

    function onOpen(evt) { 
        //console.log("Connected to WebSocket server."); 
        alert("Connected to WebSocket server.");
        websocket.send('test from Keith!');
    } 
    function onClose(evt) { 
        //console.log("Disconnected"); 
        alert("Disconnected"); 
    } 
    function onMessage(evt) { 
        //console.log('Retrieved data from server: ' + evt.data); 
        alert('Retrieved data from server: ' + evt.data);
    } 
    function onError(evt) { 
        //console.log('Error occured: ' + evt.data); 
        alert('Error occured: ' + evt.data);
    }
}

// we can directly connect to server in inline.js
//bind_server();
