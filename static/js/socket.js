$(document).ready(function() {
    let room = null
    let socket_chat = io.connect(location.protocol + "//" + document.domain + ":" + location.port + "/chat");

    socket_chat.on('connect', function() {
        console.log('here socket')
        socket_chat.emit('first', {data: "1"});
    });
    
    socket_chat.on('makechat', function(data){
        var chat = document.getElementById('chat');
        var message = document.createElement('div');
        var node = document.createTextNode(`${data.name} : ${data.message}`);
        var className = '';

        if (room == null){
            room = data['room']
        }

        console.log(data['room'])
        console.log(room)

        if (room !== data['room']){
            console.log("why?")
            return
        }

        // 타입에 따라 적용할 클래스를 다르게 지정
        switch(data.type) {
            case 'message':
            className = 'other';
            break;

            case 'connect':
            className = 'connect';
            break;

            case 'disconnect':
            className = 'disconnect';
            break;
        }

        message.classList.add(className);
        message.appendChild(node);
        chat.appendChild(message);
    });

    $("#send_btn").click(function() {
        // 입력되어있는 데이터 가져오기
        var message = document.getElementById('test').value;
        
        // 가져왔으니 데이터 빈칸으로 변경
        document.getElementById('test').value = '';
    
        // 내가 전송할 메시지 클라이언트에게 표시
        var chat = document.getElementById('chat');
        var msg = document.createElement('div');
        var node = document.createTextNode(message);
        msg.classList.add('me');
        msg.appendChild(node);
        chat.appendChild(msg);
    
        // 서버로 message 이벤트 전달 + 데이터와 함께
        socket_chat.emit('message', {type: 'message', message: message});
    });
});