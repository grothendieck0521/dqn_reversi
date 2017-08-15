var PieceX = 32;
var PieceY = 32;
var Pieces = new Array();
var BLACK  = 1;
var WHITE  = -1;
var ctx;
var turn   = 0;    // 0:ゲーム外, 1:黒番, 2:白番
var CPUFlg = 2;
var count   = 0;

var request = window.superagent;
var url = "test_api";

window.onload = function() {
    setTimeout(function(){ window.scrollTo(0,1); } , 500);
    var canvas = document.getElementById("main");
    ctx = canvas.getContext("2d");
    showBoard();
};

var gameStart = function() {
    len = document.all["color"].length;
    for (var i = 0; i < len; ++i) {
        if (document.all["color"][i].checked) {
            CPUFlg = document.all["color"][i].value * -1;
        }
    }
    showBoard();
    initPieces();
}


var showBoard = function() {
    ctx.fillStyle = "rgb(0, 128, 0)";
    ctx.fillRect(0, 0, PieceX * 8, PieceY * 8);
    ctx.fillStyle = "rgb(255, 255, 255)";
    for (var i = 0; i <= 8; i++) {
        ctx.beginPath();
        ctx.moveTo(PieceX * i, 0);
        ctx.lineTo(PieceX * i, PieceY * 8);
        ctx.closePath();
        ctx.stroke();
        ctx.closePath();
        ctx.beginPath();
        ctx.moveTo(0, PieceY * i);
        ctx.lineTo(PieceX * 8, PieceY * i);
        ctx.closePath();
        ctx.stroke();
    }
};

var initPieces = function() {
    for (var x = 0; x <= 9; ++x) {
        Pieces[x] = new Array();
        for (var y = 0; y <= 9; ++y) {
            Pieces[x][y] = 0;
        }
    }

    Pieces[4][4] = BLACK;
    Pieces[5][5] = BLACK;
    Pieces[4][5] = WHITE;
    Pieces[5][4] = WHITE;
    showPieces();
    turn = BLACK;
    showTurn(1);
    if (BLACK == CPUFlg) {
        CPUTurn();
    }
};

var showPieces = function() {

    for (var x = 1; x <= 8; ++x) {
        for (var y = 1; y <= 8; ++y) {
            if (0 != Pieces[x][y]) {
                if (BLACK == Pieces[x][y]) {
                    ctx.fillStyle = "rgb(0, 0, 0)";
                } else {
                    ctx.fillStyle = "rgb(255, 255, 255)";
                }
                ctx.beginPath();
                ctx.arc(PieceX * (x - 1 / 2), PieceY * (y - 1 / 2), PieceX / 2 - 3, 0 , Math.PI*2, true);
                ctx.closePath();
                ctx.fill();
            }
        }
    }
};

document.onclick = function() {
    if (0 != turn && CPUFlg != turn) {
        var x = event.x;
        var y = event.y;
        if(0 <= x && x <= PieceX * 8 && 0 <= y && y <= PieceY * 8) {
            x = Math.floor(x / PieceX) + 1;
            y = Math.floor(y / PieceY) + 1;

            var putFlg = putPiece(x, y, true);

            if (putFlg) {
                showPieces();
                changeTurn();
            }
        }
    }
};

var changeTurn = function() {
     // ターンチェンジ
     turn = turn * -1;

     if (false == checkPieces()) {
         turn = turn * -1
         if (false == checkPieces()) {
             gameEnd();
             // 終了
             return;
         } else {
             showTurn(2);
             if (turn == CPUFlg) {
                 // CPU
                 CPUTurn();
             }
             return;
         }
     } 
     showTurn(1);
     
     if (turn == CPUFlg) {
         // CPU
         setTimeout(CPUTurn ,500);
     }
};

// Game終了
var gameEnd = function() {
    var bCnt = countPieces(BLACK);
    var wCnt = countPieces(WHITE);

    if (bCnt < wCnt) {
         document.getElementById("msg").innerHTML = "白の勝利：" +bCnt+ " 白：" +wCnt;
    } else if (bCnt > wCnt) {
         document.getElementById("msg").innerHTML = "黒の勝利：" +bCnt+ " 白：" +wCnt;
    } else {
         document.getElementById("msg").innerHTML = "引き分け：" +bCnt+ " 白：" +wCnt;
    }
};

var CPUTurn = function() {
    var pieces = "";
    
    for (var i = 1; i <= 8; ++i) {
        for (var j = 1; j <= 8; ++j) {
            if (i == 1 && j == 1) {
                pieces = Pieces[i][j];
            } else {
                pieces += "," + Pieces[i][j];
            }
        }
    }
    
    request
      .post(url)
        .send({pieces: pieces, turn: CPUFlg})
        .end(function(err, res){
            if (err) {
                alert("SERVER ERROR");
                return;
            }
            
            data = JSON.parse(res.text);
            data = data["tags"][0]
            var x = data.x + 1;
            var y = data.y + 1;
            console.log(x)
            console.log(y)
            if (putPiece(x, y, true)) {
                showBoard();
                showPieces();
                changeTurn();
            } else {
                document.getElementById("msg").innerHTML = "CPU MISS";
            }
      });
};


// 置けるところがあるかチェックする
var checkPieces = function() {
    for (var i = 1; i <= 8; ++i) {
        for (var j = 1; j <= 8; ++j) {
            if (putPiece(i, j, false)) {
                return true;
            }
        }
    }
    return false;
};


// 指定した色の数を数える
var countPieces = function(color) {
    var count = 0;
    for (var i = 1; i <= 8; ++i) {
        for (var j = 1; j <= 8; ++j) {
            if (color == Pieces[i][j]) {
                count++;
            }
        }
    }
    return count;
}


// x,yで指定した場所に置けるかどうかチェックする。
// flgにtrueを設定すると置ける場合は置く。
var putPiece = function(x, y, flg) {
    var putFlg = false;

    if (0 != Pieces[x][y]) {
        return;
    }

    for (var i = -1; i <= 1; ++i) {
        for (var j = -1; j <= 1; ++j) {
            if (0 != i || 0 != j) {
                if (checkPiece(x, y, i, j, false)) {
                    if (flg) {
                        checkPiece(x, y, i, j, true);
                        Pieces[x][y] = turn;
                    }
                    putFlg = true;
                }
            }
        }
    }
    return putFlg;
};


var checkPiece = function(x, y, i, j, putFlg) {
    var count = 0;
    var dx = i;
    var dy = j;
    while (true) {
        if( turn  == Pieces[x + dx][y + dy]) {
            if (false == putFlg) {
                if (count > 0) {
                    break;
                } else {
                    return false;
                }
            } else {
               break;
            }

        } else if (0 == Pieces[x + dx][y + dy]) {
            return false;
        } else {
            if (putFlg) {
                Pieces[x + dx][y + dy] = turn;
            }
            ++count;
            dx += i;
            dy += j;
        }
    }

    return true;
};

var showTurn = function(msg) {

    var bCnt = countPieces(BLACK);
    var wCnt = countPieces(WHITE);

    switch(msg) {

        case 1:
            if (BLACK == turn) {
                document.getElementById("msg").innerHTML = "黒のターン 黒：" +bCnt+ " 白：" +wCnt;
            } else {
                document.getElementById("msg").innerHTML = "白のターン 黒：" +bCnt+ " 白：" +wCnt;
            }
           break;
        case 2:
            if (BLACK == turn) {
                document.getElementById("msg").innerHTML = "白のターンをスキップ 黒：" +bCnt+ " 白：" +wCnt;
            } else {
                document.getElementById("msg").innerHTML = "黒のターンをスキップ 黒：" +bCnt+ " 白：" +wCnt;
            }
            break;
   }
};

