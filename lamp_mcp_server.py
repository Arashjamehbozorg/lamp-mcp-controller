"""
MCP Server for Kasa Smart Lamp Control
Allows Claude or similar AI assistant (LLM) to control the lamp through natural language.

"""
#imports
import asyncio
from typing import Optional
from kasa.iot import IotBulb
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio
from auto_lamp_finder import find_lamp_using_api, choose_lamp

# Variable to store the desired lamp
current_lamp: Optional[IotBulb] = None

async def find_and_connect_lamp():
    """ Find and save the preferred lamp using the imported functions. """
    global current_lamp

    try:
        devices = await find_lamp_using_api()
        lamp = await choose_lamp(devices)

        if lamp:
            current_lamp = lamp
            return lamp
        
    except Exception as e:
        return None
    

async def ensure_lamp_connected():
    """ Ensure the lamp is connected and update the state if needed. """
    global current_lamp

    if current_lamp is None:
        lamp = await find_and_connect_lamp()
        if lamp is None:
            raise Exception("No lamp found. Make sure the lamp is powered on and connected to wifi.")
        current_lamp = lamp

    # update lamp state
    try:
        await current_lamp.update()
    except:
        #in case the update fails, try to reconnect
        current_lamp = None
        lamp = await find_and_connect_lamp()
        if lamp is None:
            raise Exception("Lost connection to lamp!")
        current_lamp = lamp

    return current_lamp

# MCP Server

# Initialize the MCP Server
app = Server("kasa-lamp-controller")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List of available lamp control tools."""
    return [
        Tool(
            name="turn_lamp_on",
            description="Turn the smart lamp ON",
            inputSchema={
                "type" : "object",
                "properties" :{},
                "required" : []
            }
        ),
        Tool(
            name="turn_lamp_off",
            description="Turn the smart lamp OFF",
            inputSchema={
                "type" : "object",
                "properties" :{},
                "required" : []
            }
        ),
        Tool(
            name="set_lamp_brightness",
            description="Set the brightness of the smart lamp (0-100%)",
            inputSchema={
                "type" : "object",
                "properties" :{
                    "brightness" : {
                        "type" : "number",
                        "description" : "Brightness level from 0 to 100",
                        "minimum" : 0,
                        "maximum" : 100
                    }
                },
                "required" : ["brightness"]
            }
        ),
        Tool(
            name="get_lamp_status",
            description="Get the current status of the smart lamp",
            inputSchema={
                "type" : "object",
                "properties" :{},
                "required" : []
            }
        )        
        
    ]

# call tool 
@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """ Handle tool calls from the AI assistant. """
    try:
        lamp = await ensure_lamp_connected()

        if name == "turn_lamp_on":
            await lamp.turn_on()
            lamp_name = getattr(lamp, "alias", "Unknown")
            return[TextContent(
                type="text",
                text = f"Lamp {lamp_name} turned ON successfully."
            )]
        elif name == "turn_lamp_off":
            await lamp.turn_off()
            lamp_name = getattr(lamp, "alias", "Unknown")
            return[TextContent(
                type="text",
                text = f"Lamp {lamp_name} turned OFF successfully."
            )]
        elif name == "set_lamp_brightness":
            brightness = int(arguments.get("brightness", 50))

            # Validate brightness
            if brightness < 0 or brightness > 100:
                return[TextContent(
                    type="text",
                    text="Error: Brightness must be between 0 and 100."
                )]
            
            # Check whether lamp supports brightness control
            if not(hasattr(lamp, "modules") and "Light" in lamp.modules):
                return[TextContent(
                    type="text",
                    text="Error: The lamp does not support brightness adjustment."
                )]
            # Set brightness
            await lamp.modules["Light"].set_brightness(brightness)
            lamp_name= getattr(lamp, "alias", "Unknown")

            return[TextContent(
                type="text",
                text=f"Lamp {lamp_name} brightness got set to {brightness}."
            )]
        elif name == "get_lamp_status":
            await lamp.update()

            lamp_name= getattr(lamp, "alias", "Unknown")
            lamp_model= getattr(lamp, "model", "Unknown")
            is_on = lamp.is_on

            status_lamp = f"Lamp Status:\n"
            status_lamp += f" Name: {lamp_name}\n"
            status_lamp += f" Model: {lamp_model}\n"
            status_lamp += f" State: {"ON" if is_on else "OFF"}\n"

            if hasattr(lamp, "modules") and "Light" in lamp.modules:
                try:
                    brightness = lamp.modules["Light"].brightness
                    status_lamp += f" Brightness: {brightness}\n"
                except:
                    pass
            return[TextContent(
                type="text",
                text=status_lamp
            )]
        else:
            return[TextContent(
                type="text",
                text = "Error: Unknown tool'{name}'"
            )]
    
    except Exception as e:
        return[TextContent(
            type="text",
            text=f"Error: {str(e)}"
        )]
    
async def main():
    """ Run the MCP Server. """
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())