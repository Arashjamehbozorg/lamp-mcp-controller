
#imports
import asyncio
from typing import Optional
from kasa import Discover


# Configs
PREFERRED_LAMP_NAME = "MCP Lamp" # Lamp name on kasa app
PREFERRED_MODEL = "KL110" # lamp model

def print_instantly(message):
    """ Print with immediate output. """
    print(message, flush=True)

async def find_lamp_using_api():
    """ Try to find lamps using python-kasa library. """
    print_instantly("Searching for the lamp using api...")
    print_instantly("")

    try:
        devices = await asyncio.wait_for(Discover.discover(), timeout=6.0)
        return devices if devices else {}
    except Exception as error:
        print_instantly(f"!! API search failed: {error}")
        print_instantly("")
        return {}
    
async def choose_lamp(devices):
    """ Choose the desired lamp. """
    if not devices:
        return None
    
    print_instantly(f"Found {len(devices)} deviece(s).")
    print_instantly("")

    # Update all the devices to fetch their latest info
    for device in devices.values():
        try:
            await device.update()
        except:
            continue

    # Check devices
    for device in devices.values():
        device_name = getattr(device, "alias", None)
        device_model = getattr(device, "model", None)

        # Check if the name match the preferred name
        if device_name == PREFERRED_LAMP_NAME:
            print_instantly(f"Found preferred lamp name: {device_name}")
            print_instantly("")
            return device
        # Check the model match
        if device_model == PREFERRED_MODEL:
            print_instantly(f"Found the lamp by model: {device_model}")
            print_instantly("")
            return device
        
    # Last option: Use the first device found
    first_device = next(iter(devices.values()))
    print_instantly("Using the first lamp found.")
    print_instantly("")
    return first_device

async def control_lamp(lamp):
    """ Options for controlling the lamp, which includes turn on, dim, and turn off """

    # Logging lamp info
    model = getattr(lamp, "model",  "Unknown")
    name = getattr(lamp, "alias", "Unknown")
    print_instantly(f"Connected to : {name} {model}")
    print_instantly("")

    # Testing control sequence

    #  Turn ON the lamp
    print_instantly("Turning the lamp ON... ")
    await lamp.turn_on()
    await asyncio.sleep(1)
    print_instantly("")

    # Setting the brightness to 40%
    if hasattr(lamp, "modules") and "Light" in lamp.modules:
        await lamp.modules["Light"].set_brightness(40)

    # Turn OFF the lamp
    print_instantly("Turning the lamp OFF... ")
    await lamp.turn_off()
    print_instantly("")

    # Demo is finished
    print_instantly("Demo is finished!")
    print_instantly("")
    


async def main():
    """ Main function to find and control the lamp. """
    print_instantly("=" * 50)
    print_instantly("Kasa smart lamp Controller")
    print_instantly("=" * 50)
    print_instantly("")

    try:
        # Find all devices
        devices = await find_lamp_using_api()

        # Choose the lamp
        lamp = await choose_lamp(devices)

        # if condition, for when no lamp exists
        if not lamp:
            print_instantly("!! No lamp found !!")
            print_instantly("")
            return
    
        # Control the lamp
        await control_lamp(lamp)

    finally:
        if devices:
            for device in devices.values():
                try:
                    if hasattr(device, "protocol") and device.protocol:
                        await device.protocol.close()
                except:
                    pass
    


if __name__ == "__main__":

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print_instantly("Canceled by keyboard input!")
    except Exception as error:
        print_instantly(f"Error occured: {error}")