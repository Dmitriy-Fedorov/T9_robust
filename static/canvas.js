console.log('dimas');
var canvas = document.querySelector('canvas');
//console.log(canvas)
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var c = canvas.getContext('2d');

//console.log(c)

var mouse = {x: undefined, y: undefined};
var click = {x: undefined, y: undefined};

var colorArray = [
    '#020E17',
    '#0E5159',
    '#09736A',
    '#15AB89',
    "#76D9B9"
];
/****************************************EVENT LISTENERS*************************************************************/
window.addEventListener('mousemove',
    function(event){
        mouse.x = event.x;
        mouse.y = event.y;
        //console.log(mouse);
        //console.log(click);
});

window.addEventListener('click',
    function(event) {
        click.x = mouse.x;
        click.y = mouse.y;
        //console.log(click);
    }
);

window.addEventListener('resize',
    function(){
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        init();
        desk.resize();
    }
);
/****************************************CANVAS***********************************************************************/
function Circle(x, y, dx, dy, radius){
    //console.log('new circle');
    this.x = x;
    this.y = y;
    this.dx = dx;
    this.dy = dy;
    this.radius = radius;
    this.minRadius = radius;
    this.maxRadius = radius + Math.random()*5;
    this.color = colorArray[Math.floor(Math.random() * (colorArray.length-1) + 1)];

    this.draw = function(){
        //console.log('draw');
        c.beginPath();
        c.arc(this.x, this.y, this.radius, 0, Math.PI * 2, false);
        c.strokeStyle = 'blue';
        c.stroke;
        c.fillStyle = this.color;
        c.fill();
    }

    this.update = function(){
        if(this.x + this.radius > innerWidth || this.x - this.radius < 0){
                this.dx = -this.dx;
           }

        if(this.y + this.radius > innerHeight || this.y - this.radius < 0){
                this.dy = -this.dy;
           }

        this.x += this.dx;
        this.y += this.dy;

        // interactivity
        if( mouse.x - this.x < 50 &&
            mouse.x - this.x > -50 &&
            mouse.y - this.y < 50 &&
            mouse.y - this.y > -50){
                if(this.radius < this.maxRadius){
                    this.radius += 1;
                }
        }else if(this.radius > this.minRadius){
            this.radius -= 1;
        }
        /*
        if( click.x - this.x < 30 &&
            click.x - this.x > -30 &&
            click.y - this.y < 30 &&
            click.y - this.y > -30){
                click = {x: undefined, y: undefined};
                this.dx = this.dx + 10;
                this.dy = this.dy + 10;
            }*/
        
        this.draw();
    }
}

var circleArray = [];

function init(){
    circleArray = [];

    for(var i = 0; i < 1200; i++){
        var radius = Math.random() * 10 + 1;
        var x = Math.random() * (innerWidth - radius * 2) + radius;
        var y = Math.random() * (innerHeight - radius * 2) + radius;
        var dx = Math.random() - 0.5;
        var dy = Math.random() - 0.5;
        circleArray.push(new Circle(x, y, dx, dy, radius));
    }
}
/****************************************CELL*************************************************************************/

function Cell(centerX, centerY, width, height, cellIndex){
    this.centerX = centerX;
    this.centerY = centerY;
    this.width = width;
    this.height = height;
    this.cellIndex = cellIndex;
    this.tuzdyk = false;
    this.upperCorner = {x: this.centerX - this.width/2,
                        y: this.centerY - this.height/2};
    this.bottomCorner = {x: this.centerX + this.width/2,
                         y: this.centerY + this.height/2};
    this.value = 9;
    this.destCell = this.value + this.cellIndex - 1;
    this.id = this.cellIndex;
    if(this.cellIndex > 9){
        this.id -= 10;
    }
    this.mouseOverCell = function(){
        /*if( mouse.x > this.upperCorner.x &&
            mouse.x < this.bottomCorner.x &&
            mouse.y > this.upperCorner.y &&
            mouse.y < this.bottomCorner.y){
            return true;
        }else{
            return false
        }*/
        return ( mouse.x > this.upperCorner.x && mouse.x < this.bottomCorner.x &&
                 mouse.y > this.upperCorner.y && mouse.y < this.bottomCorner.y);
    };

    this.drawDest = function(){
        c.strokeStyle = 'red';
        c.lineWidth = 2;
        c.strokeRect(this.upperCorner.x, this.upperCorner.y, this.width, this.height);
    };

    this.drawCurrent = function(){
        c.strokeStyle = 'blue';
        c.lineWidth = 2;
        c.strokeRect(this.upperCorner.x, this.upperCorner.y, this.width, this.height);
    };

    this.getDestCell = function(){
        var action_1to9 = this.id;
        var action_0to8 = action_1to9 - 1;
        if(this.value === 1){
            if(action_1to9 === 9){
                this.destCell = 1;
            }else{
                this.destCell = -action_1to9 - 1;
            }
        }else if(this.value === 0){
            this.destCell = - action_1to9;
        }else{
            var temp = (action_0to8 + this.value) % (9 * 2);
            //console.log('temp:', temp, action_0to8, action_1to9, this.value, this.id);
            if(temp > 9){
                this.destCell = temp - 9;
            }else if(temp === 0){
                this.destCell = 9;
            }else{
                this.destCell = -temp;
            }
        }
        if(this.cellIndex > 10){
            if(this.destCell > 0){
                this.destCell -= 1;
            }else{
                this.destCell = -this.destCell + 8;
            }
        }else{
            if(this.destCell > 0){
                this.destCell = this.destCell + 8
            }else{
                this.destCell = -this.destCell - 1;
            }
        }
        return this.destCell
    };

    this.draw = function(){
        c.fillStyle = '#15AB89';
        if(this.tuzdyk){
            c.fillStyle = '#0E5159';
        }
        c.fillRect(this.upperCorner.x, this.upperCorner.y, this.width, this.height);
        c.font = "30px Arial";
        c.textAlign = "center";
        c.textBaseline = "middle";
        c.fillStyle = 'black';
        c.fillText(this.value, this.centerX, this.centerY);
    };

    this.update = function(){
        if( click.x > this.upperCorner.x &&
            click.x < this.bottomCorner.x &&
            click.y > this.upperCorner.y &&
            click.y < this.bottomCorner.y){
                console.log('moved from',this.cellIndex,'to',this.getDestCell(), click);
                //this.value += 1;
                ws.send(JSON.stringify(['action', this.cellIndex]));

                click = {x: undefined, y: undefined};

           }
        if( mouse.x > this.upperCorner.x &&
            mouse.x < this.bottomCorner.x &&
            mouse.y > this.upperCorner.y &&
            mouse.y < this.bottomCorner.y){
            //console.log(this.cellIndex, mouse);

           }
        this.draw();
    };

    this.resize = function(centerX, centerY, width, height){
        this.centerX = centerX;
        this.centerY = centerY;
        this.width = width;
        this.height = height;
        this.upperCorner = {x: this.centerX - this.width/2,
                            y: this.centerY - this.height/2};
        this.bottomCorner = {x: this.centerX + this.width/2,
                             y: this.centerY + this.height/2};
    }
}
/****************************************SCORE TABLE*****************************************************************/
function ScoreTable(deskCenterX, deskCenterY, deskWidth, deskHeight) {
    this.score = {p1: 0, p2: 0};
    this.whoMoves = false;
    this.init = function (deskCenterX, deskCenterY, deskWidth, deskHeight) {
        this.deskCenterX = deskCenterX;
        this.deskCenterY = deskCenterY;
        this.deskWidth = deskWidth;
        this.deskHeight = deskHeight;
        this.upperCorner = {x: this.deskCenterX - this.deskWidth/18*3,
            y: this.deskCenterY - this.deskHeight/2 - this.deskWidth/18};
        this.width = this.deskWidth/3;
        this.height = this.deskWidth/18;
        this.p1 = {x: this.upperCorner.x + this.width/4,
            y: this.upperCorner.y + this.height/2};
        this.p2 = {x: this.upperCorner.x + this.width*3/4,
            y: this.upperCorner.y + this.height/2};
    };

    this.init(deskCenterX, deskCenterY, deskWidth, deskHeight);

    /*
    this.deskCenterX = deskCenterX;
    this.deskCenterY = deskCenterY;
    this.deskWidth = deskWidth;
    this.deskHeight = deskHeight;
    this.upperCorner = {x: this.deskCenterX - this.deskWidth/18*3,
                        y: this.deskCenterY - this.deskHeight/2 - this.deskWidth/18};
    this.width = this.deskWidth/3;
    this.height = this.deskWidth/18;
    this.p1 = {x: this.upperCorner.x + this.width/4,
               y: this.upperCorner.y + this.height/2};
    this.p2 = {x: this.upperCorner.x + this.width*3/4,
               y: this.upperCorner.y + this.height/2};
    */
    this.draw = function () {
        //console.log(this.upperCorner,this.width, this.height);
        c.fillStyle = '#020E17';
        c.fillRect(this.upperCorner.x, this.upperCorner.y, this.width, this.height);
        c.strokeStyle = '#15AB89';
        c.strokeRect(this.upperCorner.x, this.upperCorner.y, this.width, this.height);
        c.font = "30px Arial";
        c.textAlign = "center";
        c.textBaseline = "middle";
        c.fillStyle = 'white';
        var text1;
        var text2;
        if(this.whoMoves){
            text1 = 'p1: ' + this.score.p1;
            text2 = 'p2*: ' + this.score.p2;
        }else{
            text1 = 'p1*: ' + this.score.p1;
            text2 = 'p2: ' + this.score.p2;
        }
        c.fillText(text1, this.p1.x, this.p1.y);
        c.fillText(text2, this.p2.x, this.p2.y);
    };

    this.resize = function (deskCenterX, deskCenterY, deskWidth, deskHeight){
        this.init(deskCenterX, deskCenterY, deskWidth, deskHeight);
    }
}
/****************************************DESK**********************************************************************/
function Desk(){
    this.centerX = canvas.width / 2;
    this.centerY = canvas.height / 2;
    this.deskWidth = canvas.width*9/14;
    this.deskHeight = this.deskWidth/3;
    this.upperCenterY = this.centerY - this.deskHeight/4;
    this.lowerCenterY = this.centerY + this.deskHeight/4;
    this.cellWidth = this.deskWidth/9 - this.deskWidth*0.03;
    this.cellHeight = this.deskHeight/2 - this.deskHeight*0.1;
    this.cellArray = [];
    this.cellCenterX = this.centerX - this.deskWidth/2 + this.deskWidth/18;
    this.scoreTable = new ScoreTable(this.centerX, this.centerY, this.deskWidth, this.deskHeight);
    for(var i=0; i < 9; i++){
        this.cellArray.push(new Cell(this.cellCenterX, this.lowerCenterY, this.cellWidth, this.cellHeight, i+1));
        this.cellCenterX += this.deskWidth/9;
    }
    this.cellCenterX = this.centerX + this.deskWidth/2 - this.deskWidth/18;
    for(var i=0; i < 9; i++){
        this.cellArray.push(new Cell(this.cellCenterX, this.upperCenterY, this.cellWidth, this.cellHeight, i+11));
        this.cellCenterX -= this.deskWidth/9;
    }

    this.draw = function(){
        c.fillStyle = '#020E17';
        c.fillRect(this.centerX - this.deskWidth/2, this.centerY - this.deskHeight/2, this.deskWidth, this.deskHeight);
        c.strokeStyle = '#15AB89';
        c.strokeRect(this.centerX - this.deskWidth/2, this.centerY - this.deskHeight/2, this.deskWidth, this.deskHeight);
        var dest = -1;
        for(var i = 0; i < this.cellArray.length; i++){
            this.cellArray[i].update();
            if(this.cellArray[i].mouseOverCell()){
                dest = this.cellArray[i].getDestCell();
                this.cellArray[i].drawCurrent();
            }
        }
        if(dest >= 0){
            this.cellArray[dest].drawDest();
        }
        this.scoreTable.draw();
    };

    this.resize = function(){
        this.centerX = canvas.width / 2;
        this.centerY = canvas.height / 2;
        this.deskWidth = canvas.width*9/14;
        this.deskHeight = this.deskWidth/3;
        this.upperCenterY = this.centerY - this.deskHeight/4;
        this.lowerCenterY = this.centerY + this.deskHeight/4;
        this.cellWidth = this.deskWidth/9 - this.deskWidth*0.03;
        this.cellHeight = this.deskHeight/2 - this.deskHeight*0.1;
        this.cellCenterX = this.centerX - this.deskWidth/2 + this.deskWidth/18;
        for(var i=0; i < 9; i++){
            this.cellArray[i].resize(this.cellCenterX, this.lowerCenterY, this.cellWidth, this.cellHeight);
            this.cellCenterX += this.deskWidth/9;
        }
        this.cellCenterX = this.centerX + this.deskWidth/2 - this.deskWidth/18;
        for(var i=9; i < 18; i++){
            this.cellArray[i].resize(this.cellCenterX, this.upperCenterY, this.cellWidth, this.cellHeight);
            this.cellCenterX -= this.deskWidth/9;
        }
        this.scoreTable.resize(this.centerX, this.centerY, this.deskWidth, this.deskHeight);
    };

    this.updateCells = function (array) {
        for(var i=0;i<18;i++){
            this.cellArray[i].value = array[i];
        }
        if(array[20] > 0){
            this.cellArray[array[20]+8].tuzdyk = true;
        }
        if(array[21] > 0){
            this.cellArray[array[21]-1].tuzdyk = true;
        }
        this.scoreTable.score.p1 = array[18];
        this.scoreTable.score.p2 = array[19];
        this.scoreTable.whoMoves = array [22];
    }
}

var desk = new Desk();

/***********************************Web socket*************************************************************/
var ws = new WebSocket("ws://192.168.1.102:8080/ws");

ws.onmessage = function(event) {
    //alert("Получены данные " + event.data);
    //console.log("Получены данные: " + event.data);
    var data = JSON.parse(event.data);
    desk.updateCells(data);
    console.log(data);
    console.log(data[0]);
};

ws.onopen = function() {
    console.log("Соединение установлено.");
};

ws.onclose = function(event) {
    if (event.wasClean) {
        //alert('Соединение закрыто чисто');
        console.log('Connection closed');
    } else {
        //alert('Обрыв соединения'); // например, "убит" процесс сервера
        console.log('Обрыв соединения');
    }
    //alert('Код: ' + event.code + ' причина: ' + event.reason);
    console.log('Код: ' + event.code + ' причина: ' + event.reason);
};

ws.onerror = function(error) {
    alert("Ошибка " + error.message);
};

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
function animate(){
    //console.log('animate')
    requestAnimationFrame(animate);
    c.clearRect(0, 0, innerWidth, innerHeight);
    c.fillStyle = "#020E17";
    c.fillRect(0, 0, innerWidth, innerHeight);

    for(var i = 0; i < circleArray.length; i++){
        circleArray[i].update();
    }

    //console.log(desk.cellArray[0].mouseOverCell());
    desk.draw();

}

//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
init();
animate();

