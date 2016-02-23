/*
 Project: AltSoftSerialYunDatalogger
 Author: Michael Gries
 Creation: 2014-05-04
 Modified: 2014-05-27
*/

/*
 since SofftwareSerial-library failed on Arduini Yun for some reason
 Receive chracters sometimes corupted  - tested on variable bazd rates
 like 2400, 9600, 19200, 115000
 Mmost likely fault reasons could be interfering with bridge library since
 Softserial uses interrupts.
 
 This sketch should ensure that alternative software solution of 
 USART functionality can be applied to Arduino Yun Home Automation project AF104
*/ 

// AltSoftSerial always uses these pins:
//
// Board          Transmit  Receive   PWM Unusable
// -----          --------  -------   ------------
// Teensy 2.0         9        10       (none)
// Teensy++ 2.0      25         4       26, 27
// Arduino Uno        9         8         10
// Arduino Mega      46        48       44, 45

/* Reference copied from 'known_boards.h' og AltSoftSerial config folder
// Arduino Leonardo & Yun (from Cristian Maglie)
//
#elif defined(ARDUINO_AVR_YUN) 
     #define ALTSS_USE_TIMER3         // uses 16 bit timer
     #define INPUT_CAPTURE_PIN     13 // receive
     #define OUTPUT_COMPARE_A_PIN   5 // transmit
*/

/*
 used Libraries:          http://arduino.cc/en/Guide/Libraries
 Bridge-Library           http://arduino.cc/en/Reference/YunBridgeLibrary
 AltSoftSerial-Library    https://www.pjrc.com/teensy/td_libs_AltSoftSerial.html
 FileIO-Example           http://arduino.cc/en/Tutorial/YunDatalogger
 Date/Time-Example        http://arduino.cc/en/Tutorial/TemperatureWebPanel
 Mailbox-Example          http://arduino.cc/en/Tutorial/MailboxReadMessage
*/

#include <AltSoftSerial.h>
#include <Bridge.h>
#include <FileIO.h>

#define PROGRAM "AltSoftSerialYunDataLogger" 
#define VERSION "14.5.27" 

#define BAUDRATE 19200
#define commandVCRdebugBegin "DDD"
#define commandVCRdebugEnd   "d"
#define commandVCRtraceBegin "YYY"
#define commandVCRtraceEnd   "y"

#define DATEFMT "date +%Y-%m-%d"

AltSoftSerial altSerial;
int ledExtGreen = 6;
String datagram;
// logfile will lock like /mnt/sd/arduino/www/vrc/vrc_YYYY-MM-DD.log
String fileHost = "/mnt/sd/arduino/www/";
String filePath = "vrc/";
String fileName = "vrc_";
String fileDate = "1970-01-01";
String fileDateRef = "0000-01-01";
String fileExtension = ".log";
String fileLogfile;
// logfile will lock like /mnt/sd/arduino/www/vrc_YYYY-MM-DD.log
char logfilename[50] = "/mnt/sd/arduino/www/vrc_1970-01-01.log";

char oldDateChar = 'x';
char newDateChar = 'y';

void setup() {
  int i;
  pinMode(ledExtGreen, OUTPUT);
  analogWrite(ledExtGreen, 255);
  delay(1000);
  analogWrite(ledExtGreen, 16);
  Bridge.begin();
  // Bridge interface (Console) copied from ConsoleRead example
  FileSystem.begin();
  Console.begin(); 
  // Wait for Console port to connect
  //while (!Console); 
  Console.println(">>>: Console active ...");
  // active VRC communication 
  altSerial.begin(BAUDRATE);
  delay(500);
  Console.println(PROGRAM);  Console.println(VERSION);
  Console.print(">>>: by altSerial received bytes at setup: ");
  delay(500);
  i=altSerial.available();
  Console.println(i);
  // activate VRC interface for trace data
  altSerial.println(commandVCRdebugEnd);
  altSerial.println(commandVCRtraceBegin);
  
  if (FileSystem.exists("/mnt/sd/arduino/www/")){
     // get the Day as YYYY-MM-DD format by date shellcomand for filename extention
     Process dayToday;
     dayToday.runShellCommand(DATEFMT);
     while(dayToday.available()) {
       char c = dayToday.read();
       fileDate += c;
     }
     fileDate = "1970-01-01"; // for test purposes only 
     //assemble Logfilename (Strings to array)
     fileLogfile = "";
     fileLogfile.concat(fileHost); 
     fileLogfile.concat(filePath); 
     if (FileSystem.exists("/mnt/sd/arduino/www/vrc/")) {
       fileLogfile.concat(fileName); 
       fileLogfile.concat(fileDate); 
       fileLogfile.concat(fileExtension); 
       fileLogfile.toCharArray(logfilename, 50); 
       int j;
       for (j = 0; j < 50; j++) {
        Console.print(fileLogfile); Console.println(" does not exist !");
       }
     } else {
       Console.print("No SD card available"); 
     }
   } else {
     Console.println("No SD card available"); 
   }
}

void loop() {
  char c;

  
  if (Console.available()) {
    c = Console.read();
    altSerial.print(c);

   if (c == '&') {  // evaluates new date on request by '&'
     // get the Day as YYYY-MM-DD format by date shellcomand for filename extention
     fileDate = "";
     Process dayToday;
     dayToday.runShellCommand(DATEFMT);
     while(dayToday.available()) {
       char c = dayToday.read();
       if (c != '\n') {
         fileDate += c;
       }
     } // filedate must not contain '\n' at the end
     fileLogfile = "";
     fileLogfile.concat(fileHost); 
     fileLogfile.concat(filePath); 
     fileLogfile.concat(fileName); 
     fileLogfile.concat(fileDate); 
     fileLogfile.concat(fileExtension); 
     fileLogfile.toCharArray(logfilename, 48); 
   }
  }

  if (altSerial.available()) {
    analogWrite(ledExtGreen, 255);
    c = altSerial.read();
    Console.print(c);
    datagram += c;
    if (c == '\n') {  // CR => complete datagram received
      if (checkDate()){
         Console.println("checkDate() new value");
         // get the Day as YYYY-MM-DD format by date shellcomand for filename extention
         fileDate = "";
         Process dayToday;
         dayToday.runShellCommand(DATEFMT);
         while(dayToday.available()) {
           char c = dayToday.read();
           if (c != '\n') {
             fileDate += c;
           }
         } // filedate must not contain '\n' at the end
         fileLogfile = "";
         fileLogfile.concat(fileHost); 
         fileLogfile.concat(filePath); 
         fileLogfile.concat(fileName); 
         fileLogfile.concat(fileDate); 
         fileLogfile.concat(fileExtension); 
         fileLogfile.toCharArray(logfilename, 48); 
      }
      // open the file. note that only one file can be open at a time,
      // so you have to close this one before opening another.
      // The SD-card is mounted at "/mnt/sda1"
      //File logFile = FileSystem.open("/mnt/sd/arduino/www/vrc-monitor.log", FILE_APPEND);
      File logFile = FileSystem.open(logfilename, FILE_APPEND);
      // if the file is available, write to it:
      if (logFile) {
        //logFile.println("datagram: ");
        logFile.print(datagram);
        logFile.close();
        Console.print("datagram logged: "); 
          int j; for (j = 0; j < 50; j++) {
            Console.print(logfilename[j]);
          } Console.println(" "); 
        Console.println(datagram);
        Console.print("datagram received: "); 
        Console.print(PROGRAM); Console.print(" "); Console.println(VERSION);
        datagram = "";
      } else {
        Console.println("no logFile avialable");
      }
    } 
    analogWrite(ledExtGreen, 16);  //set to lower PWM limit indicating no receiving bytes
  }
  
}

boolean checkDate() {
  if (checkDatagram()) {
    //Console.println("checkDatagram() = true");
    #define DAYINDEX 27
    int datagramDayIndex = DAYINDEX*3-1;
    newDateChar = datagram.charAt(datagramDayIndex);
    Console.print("checkDate() Char = "); Console.println(newDateChar);
    if(newDateChar == oldDateChar) {
      return false;
    } else {
      Console.println("checkDate() = new Day"); 
      oldDateChar = newDateChar;
      return true;
    }
  } else {
    Console.println("checkDatagram() = false");
    return false;
  }
}

boolean checkDatagram() {
  #define SIZE 67
  int datagramSringSize = SIZE*3+2;
  if(datagram.length() == datagramSringSize) {
    Console.print(datagramSringSize); Console.print(" != datagram size: "); Console.println(datagram.length());
    return true;
  } else {
    Console.print(datagramSringSize); Console.print(" != datagram size: "); Console.println(datagram.length());
    return false;
  }
}
 
