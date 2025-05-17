import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import display
from esphome.const import (
    CONF_ID,
    CONF_LAMBDA,
    CONF_MODEL,
    CONF_RESET_PIN,
    CONF_BUSY_PIN,
    CONF_DC_PIN,
    CONF_CS_PIN,
    CONF_CLK_PIN,
    CONF_MOSI_PIN,
    CONF_UPDATE_INTERVAL,
    CONF_FULL_UPDATE_EVERY,
    CONF_ROTATION,
)

DEPENDENCIES = []
CODEOWNERS = ["@YourGithubUsername"]

crowpanel_epaper_ns = cg.esphome_ns.namespace("crowpanel_epaper")
CrowPanelEPaperBase = crowpanel_epaper_ns.class_(
    "CrowPanelEPaperBase", cg.Component, display.DisplayBuffer
)
CrowPanelEPaper4P2In = crowpanel_epaper_ns.class_(
    "CrowPanelEPaper4P2In", CrowPanelEPaperBase
)

UpdateMode = crowpanel_epaper_ns.enum("UpdateMode")
UPDATE_MODES = {
    "full": UpdateMode.FULL,
    "partial": UpdateMode.PARTIAL,
    "fast": UpdateMode.FAST,
}

CONF_UPDATE_MODE = "update_mode"

MODELS = {
    "4.2in": CrowPanelEPaper4P2In,
}

CONFIG_SCHEMA = display.BASIC_DISPLAY_SCHEMA.extend(
    {
        cv.GenerateID(): cv.declare_id(CrowPanelEPaperBase),
        cv.Required(CONF_MODEL): cv.enum(MODELS, lower=True),
        cv.Required(CONF_DC_PIN): cv.gpio_output_pin_schema,
        cv.Required(CONF_CS_PIN): cv.gpio_output_pin_schema,
        cv.Required(CONF_CLK_PIN): cv.gpio_output_pin_schema,
        cv.Required(CONF_MOSI_PIN): cv.gpio_output_pin_schema,
        cv.Optional(CONF_RESET_PIN): cv.gpio_output_pin_schema,
        cv.Optional(CONF_BUSY_PIN): cv.gpio_input_pin_schema,
        cv.Optional(CONF_FULL_UPDATE_EVERY, default=10): cv.positive_int,
        cv.Optional(CONF_UPDATE_MODE, default="full"): cv.enum(UPDATE_MODES, lower=True),
        cv.Optional(CONF_LAMBDA): cv.lambda_,
    }
).extend(cv.polling_component_schema("60s"))

async def to_code(config):
    model_type = MODELS[config[CONF_MODEL]]
    var = cg.new_Pvariable(config[CONF_ID], model_type)
    await cg.register_component(var, config)
    await display.register_display(var, config)

    dc = await cg.gpio_pin_expression(config[CONF_DC_PIN])
    cg.add(var.set_dc_pin(dc))
    cs = await cg.gpio_pin_expression(config[CONF_CS_PIN])
    cg.add(var.set_cs_pin(cs))
    clk = await cg.gpio_pin_expression(config[CONF_CLK_PIN])
    cg.add(var.set_clk_pin(clk))
    mosi = await cg.gpio_pin_expression(config[CONF_MOSI_PIN])
    cg.add(var.set_mosi_pin(mosi))

    if CONF_RESET_PIN in config:
        reset = await cg.gpio_pin_expression(config[CONF_RESET_PIN])
        cg.add(var.set_reset_pin(reset))
    if CONF_BUSY_PIN in config:
        busy = await cg.gpio_pin_expression(config[CONF_BUSY_PIN])
        cg.add(var.set_busy_pin(busy))

    if CONF_LAMBDA in config:
        lambda_ = await cg.process_lambda(
            config[CONF_LAMBDA], [(display.DisplayBufferRef, "it")], return_type=cg.void
        )
        cg.add(var.set_writer(lambda_))

    cg.add(var.set_full_update_every(config[CONF_FULL_UPDATE_EVERY]))
    
    # Set the update mode (full, partial, or fast)
    update_mode = config[CONF_UPDATE_MODE]
    if update_mode != "full": # Only set if not default
        cg.add(var.force_update_mode(UPDATE_MODES[update_mode])) 