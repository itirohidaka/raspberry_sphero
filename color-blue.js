"use strict";

var Cylon = require("cylon");

Cylon.robot({
  connections: {
    sphero: { adaptor: "sphero", port: "/dev/rfcomm0" }
  },

  devices: {
    sphero: { driver: "sphero" }
  },

  work: function(my) {
      my.sphero.color(0x0000FF); //blue

      after((2).seconds(), function() {
        console.log("I'm shutting down now.");
        Cylon.halt();
        process.exit();
      });
  }
});

Cylon.start();
