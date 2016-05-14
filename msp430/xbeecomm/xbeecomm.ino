// Simple XBee Communication Test
// Using code from http://www.simplyembedded.org/tutorials/msp430-uart/
// Author: Ron Smith, That Ain't Working

int uart_init() {
    P1IES |= 0x08;                            // Set P1.3 interrupt to active-low edge
    P1IE |= 0x08;                             // Enable interrupt on P1.3
    P1SEL |= 0x6;                             // Configure P1.1 for UART (USCI_A0)
    P1SEL2 |= 0x6;                            // Configure P1.2 for UART (USCI_A0)
    __enable_interrupt();                     // Global interrupt enable
    watchdog_enable();
    if (UCA0CTL1 & UCSWRST) {                 // USCI should be in reset before configuring - only configure once
        UCA0CTL1 |= UCSSEL_2;                 // Set clock source to SMCLK
        UCA0BR0 = 104;                        // Next 3 set the baud rate to 9600 (max for msp430)
        UCA0BR1 = 0;
        UCA0MCTL = 0x2;
        UCA0CTL1 &= ~UCSWRST;                 // Enable the USCI peripheral (take it out of reset)
        return 0;
    }
    return -1;
}

int uart_getchar(void) {
    int chr = -1;
    if (IFG2 & UCA0RXIFG)
        chr = UCA0RXBUF;
    return chr;
}

int uart_putchar(int c) {
    while (!(IFG2 & UCA0TXIFG));             // Wait for the transmit buffer to be ready
    UCA0TXBUF = (char ) c;                   // Transmit data
    return 0;
}

int uart_puts(const char *str) 
    if (str != NULL) {
        while (*str != '\0') {
            while (!(IFG2 & UCA0TXIFG));     // Wait for the transmit buffer to be ready
            UCA0TXBUF = *str;                // Transmit data
            if (*str == '\n') {              // If there is a line-feed, add a carriage return
                while (!(IFG2 & UCA0TXIFG)); // Wait for the transmit buffer to be ready
                UCA0TXBUF = '\r'; 
            }
            str++;
        }
        return 0;
    }
    return -1;
}

void setup() {
    uart_init();
}

unsigned long next_time = 0L;

void loop() {
    unsigned long this_time = millis();
}


