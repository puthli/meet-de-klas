TYPE_TEMP         = 0x01; //temp 2 bytes -3276.8°C -->3276.7°C
TYPE_RH           = 0x02; //Humidity 1 byte  0-100%
TYPE_ACC          = 0x03; //acceleration 3 bytes X,Y,Z -128 --> 127 +/-63=1G
TYPE_LIGHT        = 0x04; //Light 2 bytes 0-->65535 Lux
TYPE_MOTION       = 0x05; //No of motion 1 byte  0-255
TYPE_CO2          = 0x06; //Co2 2 bytes 0-65535 ppm
TYPE_VDD          = 0x07; //VDD 2byte 0-65535mV
TYPE_ANALOG1      = 0x08; //VDD 2byte 0-65535mV
TYPE_GPS          = 0x09; //3bytes lat 3bytes long binary
TYPE_PULSE1       = 0x0A; //2bytes relative pulse count
TYPE_PULSE1_ABS   = 0x0B;  //4bytes no 0->0xFFFFFFFF
TYPE_EXT_TEMP1    = 0x0C;  //2bytes -3276.5C-->3276.5C
TYPE_EXT_DIGITAL  = 0x0D;  //1bytes value 1 or 0
TYPE_EXT_DISTANCE = 0x0E;  //2bytes distance in mm
TYPE_ACC_MOTION   = 0x0F;  //1byte number of vibration/motion
TYPE_IR_TEMP      = 0x10;  //2bytes internal temp 2bytes external temp -3276.5C-->3276.5C
TYPE_OCCUPANCY    = 0x11;  //1byte data
TYPE_WATERLEAK    = 0x12;  //1byte data 0-255
TYPE_GRIDEYE      = 0x13;  //65byte temperature data 1byte ref+64byte external temp
TYPE_PRESSURE     = 0x14;  //4byte pressure data (hPa)
TYPE_SOUND        = 0x15;  //2byte sound data (peak/avg)
TYPE_PULSE2       = 0x16;  //2bytes 0-->0xFFFF
TYPE_PULSE2_ABS   = 0x17;  //4bytes no 0->0xFFFFFFFF
TYPE_ANALOG2      = 0x18;  //2bytes voltage in mV
TYPE_EXT_TEMP2    = 0x19;  //2bytes -3276.5C-->3276.5C

function bin16dec(bin) {
    var num=bin&0xFFFF;
    if (0x8000 & num)
        num = - (0x010000 - num);
    return num;
}
function bin8dec(bin) {
    var num=bin&0xFF;
    if (0x80 & num)
        num = - (0x0100 - num);
    return num;
}
function hexToBytes(hex) {
    for (var bytes = [], c = 0; c < hex.length; c += 2)
        bytes.push(parseInt(hex.substr(c, 2), 16));
    return bytes;
}
function DecodeElsysPayload(data){
    var obj = new Object();
    for(i=0;i<data.length;i++){
        //console.log(data[i]);
        switch(data[i]){
            case TYPE_TEMP: //Temperature
                var temp=(data[i+1]<<8)|(data[i+2]);
                temp=bin16dec(temp);
                obj.temperature=temp/10;
                i+=2;
            break
            case TYPE_RH: //Humidity
                var rh=(data[i+1]);
                obj.humidity=rh;
                i+=1;
            break
            case TYPE_ACC: //Acceleration
                obj.x=bin8dec(data[i+1]);
                obj.y=bin8dec(data[i+2]);
                obj.z=bin8dec(data[i+3]);
                i+=3;
            break
            case TYPE_LIGHT: //Light
                obj.light=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_MOTION: //Motion sensor(PIR)
                obj.motion=(data[i+1]);
                i+=1;
            break
            case TYPE_CO2: //CO2
                obj.co2=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_VDD: //Battery level
                obj.vdd=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_ANALOG1: //Analog input 1
                obj.analog1=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_GPS: //gps
                obj.lat=(data[i+1]<<16)|(data[i+2]<<8)|(data[i+3]);
                obj.long=(data[i+4]<<16)|(data[i+5]<<8)|(data[i+6]);
                i+=6;
            break
            case TYPE_PULSE1: //Pulse input 1
                obj.pulse1=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_PULSE1_ABS: //Pulse input 1 absolute value
                var pulseAbs=(data[i+1]<<24)|(data[i+2]<<16)|(data[i+3]<<8)|(data[i+4]);
                obj.pulseAbs=pulseAbs;
                i+=4;
            break
            case TYPE_EXT_TEMP1: //External temp
                var temp=(data[i+1]<<8)|(data[i+2]);
                temp=bin16dec(temp);
                obj.externalTemperature=temp/10;
                i+=2;
            break
            case TYPE_EXT_DIGITAL: //Digital input
                obj.digital=(data[i+1]);
                i+=1;
            break
            case TYPE_EXT_DISTANCE: //Distance sensor input
                obj.distance=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_ACC_MOTION: //Acc motion
                obj.accMotion=(data[i+1]);
                i+=1;
            break
            case TYPE_IR_TEMP: //IR temperature
                var iTemp=(data[i+1]<<8)|(data[i+2]);
                iTemp=bin16dec(iTemp);
                var eTemp=(data[i+3]<<8)|(data[i+4]);
                eTemp=bin16dec(eTemp);
                obj.irInternalTemperature=iTemp/10;
                obj.irExternalTemperature=eTemp/10;
                i+=4;
            break
            case TYPE_OCCUPANCY: //Body occupancy
                obj.occupancy=(data[i+1]);
                i+=1;
            break
            case TYPE_WATERLEAK: //Water leak
                obj.waterleak=(data[i+1]);
                i+=1;
            break
            case TYPE_GRIDEYE: //Grideye data
                i+=65;
            break
            case TYPE_PRESSURE: //External Pressure
                var temp=(data[i+1]<<24)|(data[i+2]<<16)|(data[i+3]<<8)|(data[i+4]);
                obj.pressure=temp/1000;
                i+=4;
            break
            case TYPE_SOUND: //Sound
                obj.soundPeak=data[i+1];
                obj.soundAvg=data[i+2];
                i+=2;
            break
            case TYPE_PULSE2: //Pulse 2
                obj.pulse2=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_PULSE2_ABS: //Pulse input 2 absolute value
                obj.pulseAbs2=(data[i+1]<<24)|(data[i+2]<<16)|(data[i+3]<<8)|(data[i+4]);
                i+=4;
            break
            case TYPE_ANALOG2: //Analog input 2
                obj.analog2=(data[i+1]<<8)|(data[i+2]);
                i+=2;
            break
            case TYPE_EXT_TEMP2: //External temp 2
                var temp=(data[i+1]<<8)|(data[i+2]);
                temp=bin16dec(temp);
                obj.externalTemperature2=temp/10;
                i+=2;
            break
            default: //somthing is wrong with data
                i=data.length;
            break
        }
    }
    return obj;
}

function Decoder(bytes, port) {
  // Decode an uplink message from a buffer
  // (array) of bytes to an object of fields.
  var decoded = DecodeElsysPayload(bytes)
  // if (port === 1) decoded.led = bytes[0];
  return decoded;
}
