# ProMacroPad
## Why can't you buy a programmer's calculator anymore?

I work in embedded software development, and fairly often I'll find that I need to convert some decimal to hexadecimal or binary. 
Sure I can open up Microsoft's Calculator, click on the hamburger menu, select programmer, and do my calculations there but I'd really
prefer to just have something on my desk always ready to go. I did some shopping around online to see if there was a cheap calculator
I could buy that could handle these basic conversion tasks, but everything I found was from the 1970's and probably contained a handfull of
leaky AA batteries.

That's where the ProMacroPad comes in.

## Off-the-shelf Components
- 20 x 4 Character LCD with I2C backpack
- 4 channel I2C logic level converter
- Adafruit NeoKey 5x6 Ortho Snap-Apart Mechanical Key Switch PCB
- 30 Cherry MX compatible switches
- 30 1u keycaps - my layout uses 0-9, A-F, arrow keys, F1-F4, and a few extras for various applications
- Raspberry Pi Zero, or a microcontroller with at least an I2C channel, and 11 gpio pins to address the key matrix, and the ability to appear as a USB HID device
- M2.5 standoffs, screws, and nuts for mounting components to the case

## Components to be built
- Laser-cut case
- Perfboard to wire up the keypad and display