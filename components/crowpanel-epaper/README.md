# CrowPanel E-Paper Component for ESPHome

This component provides support for 4.2" black and white e-paper displays using the SSD1683 driver chip.

## Features

- Support for 4.2" black and white e-paper displays with SSD1683 controller
- Multiple refresh modes:
  - **Full Update**: High quality, slower refresh (best for images)
  - **Partial Update**: Faster refresh with good quality (balanced)
- Non-blocking display updates
- Configurable full refresh intervals
- Rotation support

## Configuration

```yaml
display:
  - platform: crowpanel_epaper
    id: epaper_display
    model: 4.20in
    reset_pin: 47
    busy_pin: 48
    dc_pin: 46
    cs_pin: 45
    clk_pin: 12
    mosi_pin: 11
    full_update_every: 10  # Full refresh every 10 updates
    update_interval: 30s   # How often to refresh
    lambda: |-
      // Your display drawing code here
```

## Update Modes

This component supports two update modes for the SSD1683 controller:

- **Full Update**:
  - Complete refresh with high quality display
  - No ghosting/artifacts
  - Slower refresh rate (takes ~2-3 seconds)
  - Best used for initial setup or displaying images

- **Partial Update**:
  - Medium-speed refresh
  - Minimal ghosting
  - Good balance between speed and quality
  - Good for most typical updates

## Switching Modes Programmatically

You can change the update mode during runtime using the `set_update_mode` method:

```yaml
button:
  - platform: template
    name: "Full Refresh Mode"
    on_press:
      lambda: |-
        auto display = static_cast<esphome::crowpanel_epaper::CrowPanelEPaperBase*>(id(epaper_display).get());
        display->set_update_mode(esphome::crowpanel_epaper::UpdateMode::FULL);
        display->update();
```

## Implementation Details

The component implements a non-blocking state machine for display updates, ensuring the ESPHome main loop remains responsive even during large framebuffer transfers.

## References

- SSD1683 Datasheet for detailed command information
- Waveshare e-paper libraries for initialization inspiration

## License

This component is released under the MIT License. 