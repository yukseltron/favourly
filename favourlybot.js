if (!process.env.token) {
    console.log('Error: Specify token in environment');
    process.exit(1);
}

var Botkit = require('botkit');
var fs = require("fs");
var os = require('os');
var util = require('util');


var controller = Botkit.slackbot({
    debug: false
});

var bot = controller.spawn({
    token: process.env.token
}).startRTM();


controller.hears([''], 'direct_message,direct_mention,mention', function(bot, message) {

    bot.api.reactions.add({
        timestamp: message.ts,
        channel: message.channel,
        name: 'robot_face',
    }, function(err, res) {
        if (err) {
            bot.botkit.log('Failed to add emoji reaction :(', err);
        }
    });


    controller.storage.users.get(message.user, function(err, user) {
        var fileName = "./message.json";
        var log_file = fs.createWriteStream(`${fileName}`, {
          flags: 'w' //Opens file for writing; creates file if it doesn't exist or truncates if it exists
        });

        console.log = function(d) { //overwrites console
          log_file.write(util.format(d) + '\n');
        }

        if (user && user.name) {
            bot.reply(message, 'Hello ' + user.name + '!!');
        } else {
            bot.reply(message, 'Favour initiated!');
            console.log(message);

        }
    });
});
