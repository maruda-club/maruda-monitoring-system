(function (ext) {
    var socket = null;
    var connected = false;
    var myStatus = 1;
    var myMsg = 'not_ready';

    ext.connect = function (callback) {
        window.socket = new WebSocket("ws://127.0.0.1:9000");
        window.socket.onopen = function () {
            var msg = JSON.stringify({
                "command": "ready"
            });

            window.socket.send(msg);
            myStatus = 2;
            myMsg = 'ready';
            connected = true;

            window.setTimeout(function() {
                callback();
            }, 1000);

        };

        window.socket.onmessage = function (message) {
        };

        window.socket.onclose = function (e) {
            console.log("Connection closed.");
            socket = null;
            connected = false;
            myStatus = 1;
            myMsg = 'not_ready'
        };
    };

    ext._shutdown = function () {
        var msg = JSON.stringify({
            "command": "shutdown"
        });
        window.socket.send(msg);
    };

    ext._getStatus = function (status, msg) {
        return {status: myStatus, msg: myMsg};
    };

    ext.sendmsg = function (msg) {
        if (connected == false) {
            alert("Server Not Connected");
        }
        // validate the pin number for the mode
        var msg = JSON.stringify({
            "command": 'sendmsg', 'msg': msg
        });
        console.log(msg);
        window.socket.send(msg);
    };

    var descriptor = {
        blocks: [
            ["w", 'Connect to Monitoring System.', 'connect'],
            [" ", "Send a message: %s", "sendmsg", "Hello World!"]

        ],
        "menus": {
            "high_low": ["0", "1"]

        },
        url: 'https://maruda-club.github.io/maruda-monitoring-system/'
    };

    ScratchExtensions.register('Maruda Club', descriptor, ext);
})({});

