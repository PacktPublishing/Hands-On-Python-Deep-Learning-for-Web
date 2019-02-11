var express = require('express');
var app = express();

const tf = require('@tensorflow/tfjs');
const iris = require('./iris.json');

tf.disableDeprecationWarnings();

const trainingData = tf.tensor2d(iris.map(item=> [
    item.sepal_length, item.sepal_width, item.petal_length, item.petal_width
]
),[144,4])

const outputData = tf.tensor2d(iris.map(item => [
    item.species === 'setosa' ? 1 : 0,
    item.species === 'virginica' ? 1 : 0,
    item.species === 'versicolor' ? 1 : 0

]), [144,3])

const model = tf.sequential();


model.add(tf.layers.dense(
    {   inputShape: 4, 
        activation: 'sigmoid', 
        units: 10
    }
));

model.add(tf.layers.dense(
    {
        inputShape: 10, 
        units: 3, 
        activation: 'softmax'
    }
));

model.summary();

model.compile({
    loss: "categoricalCrossentropy",
    optimizer: tf.train.adam()
});

async function train_data(){

	console.log("Training Started");
    for(let i=0;i<50;i++){
		let res = await model.fit(trainingData, outputData, {epochs: 50});
		console.log(`Iteration ${i}: ${res.history.loss[0]}`);
	}
	console.log("Training Complete");
}

app.use(express.static('./public')).get('/', function (req, res) {
    res.sendFile('./index.html');
});

var bodyParser = require('body-parser');

app.use(bodyParser.urlencoded({ extended: false }));

app.post('/predict', function(req, res) {
    var sepLen = req.body.sepLen;
    var sepWid = req.body.sepWid;
    var petLen = req.body.petLen;
    var petWid = req.body.petWid;

    var test = tf.tensor2d([sepLen, sepWid, petLen, petWid], [1,4]);
    var out = model.predict(test);

    var maxIndex = 0;
    for (let i=1;i<out.size; i++){
    	if (out.buffer().get(0, i) > out.buffer().get(0, maxIndex)){
    		maxIndex = i;
    	}
    }

    console.log(maxIndex);

    ans = "Undetermined";

    switch(maxIndex) {
		case 0:
			ans = "Setosa";	
		break;
		case 1:
			ans = "Virginica";	
		break;
		case 2:
			ans = "Versicolor";	
		break;	
	}
	
	res.send(ans);

});

var doTrain = async function (req, res, next) {
	await train_data();
	next();
}

app.use(doTrain).post('/train', function(req, res) {
	res.send("1");
});

app.listen(3000);