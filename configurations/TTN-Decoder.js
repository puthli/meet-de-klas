function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = {};
    decoded.co2 = bytes[0]*10000+bytes[1]*1000+bytes[2]*100+bytes[3]*10+bytes[4]
    decoded.humidity = bytes[5]*10+bytes[6]+bytes[7]/10
    decoded.temperature = bytes[8]*10+bytes[9]+bytes[10]/10

  // if (port === 1) decoded.led = bytes[0];

  return decoded;
}
