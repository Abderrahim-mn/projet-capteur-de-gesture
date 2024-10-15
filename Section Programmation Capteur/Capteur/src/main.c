#include "include/board.h"
#include "lib/io.h"
#include "lib/uart.h"
#include "lib/util.h"
#include "lib/i2c.h"
#include "lib/timer.h"
#include "lib/term.h"
#include "libshield/lcd_128x32.h"
#include "libshield/leds.h"
#include "libshield/gesture.h"


#define MAIN_GLOBAL_INIT



#ifdef MAIN_GLOBAL_INIT

#define DELAY_1_SECOND      1000000
#define DELAY_10_SECONDS    10000000

#define delay_us(us)        timer_wait_us(_TIM3, us)

volatile char command;






// static void on_zigbee_command_received(char c) {
//     command = c;
//     uart_printf(_USART1, "\r\nZigbee command received : %c\r\n", c);
// }


int main(void) {
    //initialisation Liaison ST-LINK
    uart_init(_USART2, 115200, UART_8N1, NULL);

    //initialisation Liaison zigbee
    //uart_init(_USART1, 115200, UART_8N1, on_zigbee_command_received);
    
    
    i2c_master_init(_I2C1);
    // initialisation capteur
    gesture_init();




   


  

    while (1) {

    //Print  geste detectee
    print_gesture();
   

   //Liaison zigbee
    // char c = putchar_zigbee(_USART1, "hello world");
   // zigbee_printf(_USART1, c);

     

    // int geste = return_gesture();

    // switch(geste){

    //     case 1:
    //     cls();
    //     lcd_printf("**********FORWARD**********");
    //     break;

    //     case 2:
    //     cls();
    //     lcd_printf("**********BACKWARD**********");
    //     break;

    //     case 3:
    //     cls();
    //     lcd_printf("**********RIGHT**********");
    //     break;
        
    //     case 4:
    //     cls();
    //     lcd_printf("**********LEFT**********");
    //     break;


    //     case 5:
    //     cls();
    //     lcd_printf("**********UP**********");
    //     break;

    //     case 6:
    //     cls();
    //     lcd_printf("**********DOWN**********");
    //     break;

    //     case 7:
    //     cls();
    //     lcd_printf("**********CLOCKWISE**********");
    //     break;

    //     case 8:
    //     cls();
    //     lcd_printf("**********ANTI_CLOCKWISE**********");
    //     break;

    //      case 9:
    //     cls();
    //     lcd_printf("**********WAVE**********");
    //     break;

    //     default:break;
    // }
    
   delay_us(DELAY_10_SECONDS);
		   	
 
		}
              
    return 0;
}

#endif
