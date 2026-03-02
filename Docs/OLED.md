# Chapter 7: OLED Displays

**Author: Somtochukwu Emeka-Onwuneme**

---

This document presents the entity-relationship model of the library ```oled.py```

---

## Attribution

The OLED driver in this library is based on community MicroPython drivers:

- **SH1106 driver** by Radomir Dopieralski ([@deshipu](https://github.com/deshipu)), Robert Hammelrath ([@robert-hh](https://github.com/robert-hh)), and Tim Weber ([@scy](https://github.com/scy)). Licensed under MIT.

- **SSD1306 driver** by Adafruit and contributors. Licensed under BSD.

Both drivers were modified and integrated into the StansMicroPy package by Somtochukwu Stanislus Emeka-Onwuneme (2026). Modifications include unifying both drivers into a single module, adjusting default rotation parameters, and aligning the interface to be consistent across both chip variants.

---

## Entity Relationship

### Entity Relationship Model: ```SH1106```

**Entity: SH1106**

*Base class for SH1106-based OLED displays. Inherits from MicroPython's ```framebuf.FrameBuffer```, giving access to all standard drawing primitives.*

**Attributes (Properties / State)**

```width``` → Display width in pixels (typically 128).

```height``` → Display height in pixels (typically 64).

```external_vcc``` → Boolean indicating whether external VCC supply is used.

```flip_en``` → Boolean tracking whether display is flipped (rotation 180° or 270°).

```rotate90``` → Boolean indicating 90° or 270° rotation mode.

```pages``` → Number of pages (height ÷ 8).

```bufsize``` → Total buffer size in bytes (pages × width).

```renderbuf``` → Bytearray holding the pixel data for rendering.

```displaybuf``` → Bytearray holding the data sent to the display (same as renderbuf unless rotate90 is active).

```pages_to_update``` → Bitmask tracking which pages have changed and need refreshing.

```delay``` → Delay in ms after powering on (set by subclass).

**Methods (Behaviours)**

```__init__(width, height, external_vcc, rotate=0)``` → Constructor; initialises framebuffer, page tracking, and display.

```init_display()``` → Resets the display, clears the screen, and powers on.

```poweroff()``` → Turns the display off.

```poweron()``` → Turns the display on (with optional delay).

```flip(flag, update=True)``` → Flips the display orientation (mirror vertical/horizontal).

```sleep(value)``` → Puts the display into or out of sleep mode.

```contrast(contrast)``` → Sets display contrast (0–255).

```invert(invert)``` → Inverts the display colours (0 = normal, 1 = inverted).

```show(full_update=False)``` → Pushes changed pages to the display. If ```full_update=True```, refreshes all pages.

```pixel(x, y, color=None)``` → Gets or sets a pixel, and marks the affected page for update.

```text(text, x, y, color=1)``` → Draws text at position (x, y).

```line(x0, y0, x1, y1, color)``` → Draws a line between two points.

```hline(x, y, w, color)``` → Draws a horizontal line.

```vline(x, y, h, color)``` → Draws a vertical line.

```fill(color)``` → Fills the entire display with a colour (0 or 1).

```fill_rect(x, y, w, h, color)``` → Draws a filled rectangle.

```rect(x, y, w, h, color)``` → Draws a rectangle outline.

```ellipse(x, y, xr, yr, color)``` → Draws an ellipse.

```blit(fbuf, x, y, key, palette)``` → Copies another framebuffer onto the display.

```scroll(x, y)``` → Scrolls the display contents.

```register_updates(y0, y1=None)``` → Marks pages affected by a Y-coordinate range as needing update.

```reset(res=None)``` → Hardware reset via the reset pin (if provided).

---

### Entity Relationship Model: ```SH1106_I2C```

**Entity: SH1106_I2C**

*I2C interface subclass of SH1106.*

**Attributes (Properties / State)**

```i2c``` → I2C object for communication.

```addr``` → I2C address of the display (default 0x3C).

```res``` → Optional reset pin object.

```temp``` → 2-byte buffer for command writes.

```delay``` → Post-power-on delay in ms.

**Methods (Behaviours)**

```__init__(width, height, i2c, res=None, addr=0x3c, rotate=180, external_vcc=False, delay=0)``` → Constructor; sets up I2C communication and initialises display.

```write_cmd(cmd)``` → Sends a command byte over I2C.

```write_data(buf)``` → Sends display data over I2C.

```reset(res=None)``` → Hardware reset using the stored reset pin.

---

### Entity Relationship Model: ```SH1106_SPI```

**Entity: SH1106_SPI**

*SPI interface subclass of SH1106.*

**Attributes (Properties / State)**

```spi``` → SPI object for communication.

```dc``` → Data/Command pin object.

```res``` → Optional reset pin object.

```cs``` → Optional chip select pin object.

```delay``` → Post-power-on delay in ms.

**Methods (Behaviours)**

```__init__(width, height, spi, dc, res=None, cs=None, rotate=0, external_vcc=False, delay=0)``` → Constructor; sets up SPI communication and initialises display.

```write_cmd(cmd)``` → Sends a command byte over SPI (with D/C pin low).

```write_data(buf)``` → Sends display data over SPI (with D/C pin high).

```reset(res=None)``` → Hardware reset using the stored reset pin.

---

### Entity Relationship Model: ```SSD1306```

**Entity: SSD1306**

*Base class for SSD1306-based OLED displays. Also inherits from ```framebuf.FrameBuffer```.*

**Attributes (Properties / State)**

```width``` → Display width in pixels.

```height``` → Display height in pixels.

```external_vcc``` → Boolean indicating external VCC supply.

```pages``` → Number of pages (height ÷ 8).

```buffer``` → Bytearray holding the full display framebuffer.

**Methods (Behaviours)**

```__init__(width, height, external_vcc)``` → Constructor; initialises framebuffer and runs display init sequence.

```init_display()``` → Sends the full SSD1306 initialisation command sequence (addressing, timing, charge pump, etc.).

```poweroff()``` → Turns the display off.

```poweron()``` → Turns the display on.

```contrast(contrast)``` → Sets display contrast (0–255).

```invert(invert)``` → Inverts display colours.

```rotate(rotate)``` → Rotates the display orientation.

```show()``` → Pushes the entire framebuffer to the display.

---

### Entity Relationship Model: ```SSD1306_I2C```

**Entity: SSD1306_I2C**

*I2C interface subclass of SSD1306.*

**Attributes (Properties / State)**

```i2c``` → I2C object for communication.

```addr``` → I2C address (default 0x3C).

```temp``` → 2-byte buffer for command writes.

```write_list``` → Pre-built list for efficient data writes.

**Methods (Behaviours)**

```__init__(width, height, i2c, addr=0x3C, external_vcc=False)``` → Constructor; sets up I2C and initialises display.

```write_cmd(cmd)``` → Sends a command byte over I2C.

```write_data(buf)``` → Sends display data over I2C using ```writevto()``` for efficiency.

---

### Entity Relationship Model: ```SSD1306_SPI```

**Entity: SSD1306_SPI**

*SPI interface subclass of SSD1306.*

**Attributes (Properties / State)**

```rate``` → SPI baud rate (10 MHz).

```spi``` → SPI object for communication.

```dc``` → Data/Command pin object.

```res``` → Reset pin object.

```cs``` → Chip select pin object.

**Methods (Behaviours)**

```__init__(width, height, spi, dc, res, cs, external_vcc=False)``` → Constructor; sets up SPI, performs hardware reset, and initialises display.

```write_cmd(cmd)``` → Sends a command byte over SPI.

```write_data(buf)``` → Sends display data over SPI.

---

## Relationships

- SH1106 / SSD1306 ↔ FrameBuffer
    - Both base classes inherit from MicroPython's ```framebuf.FrameBuffer```, providing all standard drawing primitives (text, line, rect, fill, pixel, etc.).

- SH1106_I2C / SSD1306_I2C ↔ I2C
    - 1 display uses 1 ```machine.I2C``` object for communication (mandatory).

- SH1106_SPI / SSD1306_SPI ↔ SPI
    - 1 display uses 1 ```machine.SPI``` object, plus D/C, CS, and optional reset pins.

- Display ↔ Pages
    - The display is divided into pages (8 rows of pixels each). SH1106 uses dirty-page tracking via ```pages_to_update``` to minimise I2C/SPI traffic. SSD1306 pushes the full buffer on every ```show()```.
