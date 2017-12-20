console.log('dimas')
var canvas = document.querySelector('canvas');
//console.log(canvas)
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var c = canvas.getContext('2d');

//c.fillRect(100, 100, 100, 100)
//console.log(c)

var mouse = {
    x: undefined,
    y: undefined
}

var maxRadius = 10;
var minRadius = 5;

var colorArray = [
    '#020E17',
    '#0E5159',
    '#09736A',
    '#15AB89',
    "#76D9B9"
];

console.log('asd');
window.addEventListener('mousemove',
    function(event){
        mouse.x = event.x;
        mouse.y = event.y;
        //console.log(mouse);
    });

window.addEventListener('resize',
        function(){
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
            init();
        }
    );

function Circle(x, y, dx, dy, radius){
    //console.log('new circle');
    this.x = x;
    this.y = y;
    this.dx = dx;
    this.dy = dy;
    this.radius = radius;
    this.minRadius = radius;
    this.color = colorArray[Math.floor(Math.random() * colorArray.length + 1)];

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
        if(mouse.x - this.x < 50 &&
           mouse.x - this.x > -50 &&
           mouse.y - this.y < 50 &&
           mouse.y - this.y > -50){
                if(this.radius < maxRadius){
                    this.radius += 1;
                }
        }else if(this.radius > this.minRadius){
            this.radius -= 1;
        }
        
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

var centerX = canvas.width / 2;
var centerY = canvas.height / 2;
var deskWidth = 900;
var deskHeight = 300;
var upperCenterY = centerY - deskHeight/4;
var lowerCenterY = centerY + deskHeight/4;
var cellWidth = deskWidth/9 - deskWidth*0.03;
var cellHeight = deskHeight/2 - deskHeight*0.1;
var cellCenterX = centerX - deskWidth/2 + deskWidth/18;

function drawRect(centerX, centerY, width, height){
    c.strokeRect(centerX - width/2, centerY - height/2, width, height)
}
function drawFillRect(centerX, centerY, width, height){
    c.fillRect(centerX - width/2, centerY - height/2, width, height)
}
function drawClearRect(centerX, centerY, width, height){
    c.fillRect(centerX - width/2, centerY - height/2, width, height)
}
function text(text,x,y){
    strokeText(text,x,y)
}

function T9_game_back(){
    cellCenterX = centerX - deskWidth/2 + deskWidth/18 ;
    c.fillStyle = '#020E17'
    drawFillRect(centerX, centerY, deskWidth, deskHeight);
    c.font = "30px Arial";
    c.textAlign = "center";
    for(var i=0; i < 9; i++){
        c.fillStyle = '#15AB89';
        drawFillRect(cellCenterX, upperCenterY, cellWidth, cellHeight);
        drawFillRect(cellCenterX, lowerCenterY, cellWidth, cellHeight);
        c.fillStyle = 'black';
        c.fillText('9', cellCenterX, upperCenterY);
        c.fillText('9', cellCenterX, lowerCenterY);
        cellCenterX += deskWidth/9;
    }
}



function animate(){
    //console.log('animate')
    requestAnimationFrame(animate);
    c.clearRect(0, 0, innerWidth, innerHeight);

    for(var i = 0; i < circleArray.length; i++){
        circleArray[i].update();
    }

    T9_game_back();

}

/*
var net = require('net');
var client = new net.Socket();
client.connect(5005, '127.0.0.1', function() {
	console.log('Connected');
	client.write('Hello, server! Love, Client.');
});

client.on('data', function(data) {
	console.log('Received: ' + data);
	client.destroy(); // kill client after server's response
});

client.on('close', function() {
	console.log('Connection closed');
});
*/
/*
var ws = new WebSocket("ws://127.0.0.1:5006/"),
messages = document.createElement('ul');
ws.onmessage = function (event) {
    var messages = document.getElementsByTagName('ul')[0],
        message = document.createElement('li'),
        content = document.createTextNode(event.data);
    message.appendChild(content);
    messages.appendChild(message);
};
document.body.appendChild(messages);
*/
init();
animate();

