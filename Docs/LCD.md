# Chapter 4: Liquid Crystal Display (LCD)
**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model  of the library ```LiquidCrystal.py```

--- 

**Attributes (Properties / State)**

```i2c``` – I2C object used to communicate with the LCD

```i2c_addr``` – Address of the I2C LCD module

```num_lines / num_columns``` – LCD dimensions

```cursor_x / cursor_y```– Cursor position (column, row)

```backlight``` – State of the LCD backlight (True/False)

```implied_newline``` – Used internally to handle auto-wrapping behavior

**Methods (Behaviours)**

```clear()``` – Clears the display and resets cursor to (0,0)

```move_to(x, y)``` – Moves cursor to given column and row

```putchar(char)``` – Prints a single character to LCD

```putstr(string)``` – Writes a full string to LCD with auto-wrapping

```display_on()``` – Turns on the display (unblanks screen)

```display_off()``` – Turns off the display (blanks screen)

```show_cursor()``` – Makes the cursor visible

```hide_cursor()``` – Hides the cursor

```blink_cursor_on() / blink_cursor_off()``` – Toggles blinking cursor

```backlight_on() / backlight_off()``` – Controls backlight

```custom_char(location, charmap)``` – Defines a custom character (0–7)

```hal_write_command(cmd)``` – Sends command to LCD (implemented in I2cLcd)

```hal_write_data(data)``` – Sends character data to LCD (implemented in I2cLcd)

```hal_sleep_us(us)``` – Microsecond delay (used internally)

**Relationships**

` I2cLcd inherits from LcdApi

- Depends on machine.I2C for I²C communication

- Communicates via PCF8574 I/O expander

- Uses gc.collect() to manage memory on constrained boards