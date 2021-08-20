const fs = require('fs');
const readline = require('readline');
const request = require('request')

/*
let range = n => Array.from(Array(n).keys())

data = range(1000)

data.forEach(function (item) {
  request.get("https://httpbin.org/ip", function (error, response, body){
      console.log("Request " + item + " complete.")
      console.log(response.statusCode)
  });
})
*/



const rl = readline.createInterface({
    input: fs.createReadStream('./data/2021-08-17.txt'),
    output: process.stdout,
    terminal: false
});

rl.on('line', (line) => {
    //console.log(line);
    request.head("Https://" + line, function(error, response){
        if ( ! error && response == 200) {
            console.log(line)
        }
    });
});