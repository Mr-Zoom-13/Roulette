$(document).ready(function () {
    var socket = io();

    socket.on('connect', function () {
        socket.emit('filling');
    })

    socket.on('update_users', function (data) {
        console.log("ZASHEL");
        console.log(data)
        var spisok = $(".spisok"), spisok_roulette = $(".list")
        spisok.empty()
        spisok_roulette.empty()
        for (i = 0; i < data.users.length; i++) {
            spisok.append(`<li><img src="${data.users[i].photo}" alt="avatar"><p>${data.users[i].username}</p><p>${data.users[i].summ}</p><p>${data.users[i].prc}%</p></li>`)
            spisok_roulette.append(`<li><img src="${data.users[i].photo}" alt="avatar"></li>`)
        }
        z = 5;
        for (i = 0; i < z; i++) {
            $(".list li").clone().appendTo(".list");
        }
    })
    $('#roulette').click(function () {
        socket.emit("start_roulette")
    })

    socket.on('roulette', function (data) {
        console.log(data)
        var audio = new Audio('/static/music/2.mp3');
        audio.play();
        $('.window').css({
            right: "0"
        })
        $('.list li').css({
            border: '4px solid transparent'
        })

        function selfRandom(min, max) {
            return Math.floor(Math.random() * (max - min + 1)) + min;
        }
        var y_prog = 100 / data.len_users
        console.log(y_prog)
        var x = y_prog * data.len_users + data.win_id - 1;
        var g = x + 1;
        var y = selfRandom(65, 165);
        $('.window').animate({
            right: ((x * 130) + (x * 8 - z * 4) - y)
        }, 10000, function () {
            $('.list li:eq(' + g + ')').css({border: '4px solid #00ba00'});
            const modal = new ItcModal({
                title: data.win_username,
                content: `<img src="${data.win_photo}" alt="" /><br/><h1 class="text_win">${data.win_summ}</h1>`
            });
            setTimeout(() => {
                modal.show();
                setTimeout(() => {
                    socket.emit('filling');
                }, 1000)
            }, 700);
        });
    })
})
