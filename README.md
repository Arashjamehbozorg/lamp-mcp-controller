# Kasa Smart Lamp MCP Server

A Model Context Protocol (MCP) server that enables AI assistants like Claude Desktop Version to control TP-Link Kasa smart lamps through natural language commands.

## Overview

This project provides an MCP server that bridges AI assistants with TP-Link Kasa smart lamps (KL110 and compatible models). It allows you to control your smart lamp using natural language through Claude or other MCP-compatible AI assistants.

## Features

- **Automatic Lamp Discovery**: Automatically finds and connects to Kasa smart lamps on your network
- **Natural Language Control**: Control your lamp through conversational commands
- **Brightness Control**: Adjust lamp brightness from 0-100%
- **Status Monitoring**: Check current lamp state and settings
- **Auto-reconnection**: Handles connection issues gracefully

## Available Commands

The MCP server provides the following tools:

- `turn_lamp_on` - Turn the smart lamp ON
- `turn_lamp_off` - Turn the smart lamp OFF
- `set_lamp_brightness` - Set brightness level (0-100%)
- `get_lamp_status` - Get current lamp status and information

## Requirements

- Python 3.7+
- TP-Link Kasa smart lamp (tested with KL110)
- Lamp connected to the same WiFi network as your computer

## Installation

1. Clone this repository:

```bash
git clone https://github.com/Arashjamehbozorg/lamp-mcp-controller/
cd lamp-mcp-controller
```

2. Install required dependencies:

```bash
pip install python-kasa mcp
```

3. Ensure your Kasa smart lamp is:
   - Powered on
   - Connected to your WiFi network
   - Set up through the Kasa mobile app

## Configuration

Edit the configuration variables in `auto_lamp_finder.py`:

```python
PREFERRED_LAMP_NAME = "MCP Lamp"  # Your lamp's name in Kasa app
PREFERRED_MODEL = "KL110"          # Your lamp's model number
```

## Usage

### Testing the Lamp Connection

Run the standalone lamp finder to test your connection:

```bash
python3 auto_lamp_finder.py
```

This will:

1. Search for lamps on your network
2. Connect to your preferred lamp
3. Run a demo sequence (turn on, dim to 40%, turn off)

### Running the MCP Server

Start the MCP server:

```bash
python3 lamp_mcp_server.py
```

The server will run in stdio mode, ready to receive commands from an MCP-compatible AI assistant.

### Using with Claude Desktop

Add this configuration to your Claude Desktop config file:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "kasa-lamp": {
      "command": "python",
      "args": ["/path/to/your/lamp_mcp_server.py"]
    }
  }
}
```

Replace `/path/to/your/` with the actual path to your project directory.

## Example Interactions

Once connected through Claude, you can use natural language commands:

- "Turn on my lamp"
- "Set the brightness to 50 percent"
- "Turn off the lamp"
- "What's the status of my lamp?"

## Project Structure

```
.
├── auto_lamp_finder.py      # Lamp discovery and testing script
├── lamp_mcp_server.py        # Main MCP server implementation
├── .gitignore                # Git ignore rules for Python
└── README.md                 # This file
```

## How It Works

1. **Discovery Phase**: The server uses the `python-kasa` library to discover Kasa devices on your local network
2. **Lamp Selection**: Prioritizes lamps by preferred name, then model, then uses the first available device
3. **MCP Integration**: Exposes lamp controls as MCP tools that AI assistants can call
4. **Command Execution**: Translates natural language requests into specific lamp control commands

## Troubleshooting

### Lamp Not Found

- Ensure the lamp is powered on
- Verify the lamp is connected to WiFi (check the Kasa app)
- Make sure your computer and lamp are on the same network
- Try running `auto_lamp_finder.py` to test connectivity

### Connection Lost

The server automatically attempts to reconnect if the connection is lost. If issues persist:

1. Restart the lamp
2. Restart the MCP server
3. Check your network connection

### Brightness Control Not Working

Some Kasa models don't support brightness control. Verify your model supports dimming in the Kasa app.

## Compatible Devices

Tested with:

- TP-Link Kasa KL110 (Dimmable Smart Bulb)

Should work with other Kasa smart bulbs that support the TP-Link smart home protocol.

## Dependencies

- [python-kasa](https://github.com/python-kasa/python-kasa) - Python library for TP-Link Kasa devices
- [mcp](https://github.com/modelcontextprotocol/python-sdk) - Model Context Protocol SDK

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## Acknowledgments

- Built using the [Model Context Protocol](https://modelcontextprotocol.io/)
- Uses the [python-kasa](https://github.com/python-kasa/python-kasa) library

## Support

For issues or questions:

1. Check the troubleshooting section above
2. Review the [python-kasa documentation](https://python-kasa.readthedocs.io/)
3. Open an issue in this repository

---

Made with ❤️ for smart home automation
