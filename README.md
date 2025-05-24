# Aladhan MCP Server

A Model Context Protocol (MCP) server that provides Islamic prayer times, Qibla direction, and Hijri date conversion using the [Aladhan API](http://api.aladhan.com).

## Features

- 🕌 **Prayer Times**: Get accurate Islamic prayer times for any city or coordinates
- 📅 **Date Conversion**: Convert between Gregorian and Hijri (Islamic) calendars
- 🧭 **Qibla Direction**: Find the direction to Mecca from any location
- ⚙️ **Calculation Methods**: View different prayer time calculation methods
- 🌍 **Global Coverage**: Works worldwide using the Aladhan API
- 📱 **Multiple Formats**: Support for both city names and GPS coordinates

## Installation

### Prerequisites

- Python 3.8 or higher
- Claude Desktop application

### Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:

```bash
pip install mcp requests
```

## Configuration

### For Claude Desktop

Add this to your Claude Desktop configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "aladhan-api": {
      "command": "python",
      "args": ["/path/to/aladhan_mcp_server.py"]
    }
  }
}
```

Replace `/path/to/aladhan_mcp_server.py` with the actual path to the server file.

### For Other MCP Clients

The server can be run directly:

```bash
python aladhan_mcp_server.py
```

## Available Tools

### 1. Get Prayer Times by City
Get Islamic prayer times for a specific city and date.

**Parameters:**
- `city` (required): Name of the city
- `country` (required): Name of the country
- `date` (optional): Date in YYYY-MM-DD format (defaults to today)
- `method` (optional): Calculation method ID (1-15)
- `school` (optional): Asr juristic method (0 for Shafi, 1 for Hanafi)

**Example:**
```
Get prayer times for London, UK today
Get prayer times for Cairo, Egypt for 2024-12-25
```

### 2. Get Prayer Times by Coordinates
Get Islamic prayer times for specific geographic coordinates.

**Parameters:**
- `latitude` (required): Latitude of the location
- `longitude` (required): Longitude of the location
- `date` (optional): Date in YYYY-MM-DD format (defaults to today)
- `method` (optional): Calculation method ID (1-15)
- `school` (optional): Asr juristic method (0 for Shafi, 1 for Hanafi)

**Example:**
```
Get prayer times for coordinates 40.7128, -74.0060
What are the prayer times for latitude 21.4225, longitude 39.8262?
```

### 3. Convert Gregorian to Hijri Date
Convert a Gregorian date to the Islamic (Hijri) calendar.

**Parameters:**
- `date` (required): Gregorian date in DD-MM-YYYY format

**Example:**
```
Convert 25-12-2024 to Hijri date
What is 01-01-2025 in the Islamic calendar?
```

### 4. Get Qibla Direction
Find the Qibla direction (towards Mecca) from any location.

**Parameters:**
- `latitude` (required): Latitude of the location
- `longitude` (required): Longitude of the location

**Example:**
```
What is the Qibla direction for coordinates 40.7128, -74.0060?
Show me Qibla direction for New York City coordinates
```

### 5. Get Calculation Methods
View available Islamic prayer time calculation methods.

**Example:**
```
Show me available prayer time calculation methods
What calculation methods are available for prayer times?
```

## Supported Calculation Methods

The server supports various Islamic prayer time calculation methods including:

- **Method 1**: University of Islamic Sciences, Karachi
- **Method 2**: Islamic Society of North America (ISNA)
- **Method 3**: Muslim World League (MWL)
- **Method 4**: Umm al-Qura University, Makkah
- **Method 5**: Egyptian General Authority of Survey
- And many more...

Use the `get_calculation_methods` tool to see the complete list with parameters.

## API Reference

This server uses the [Aladhan API](http://api.aladhan.com) to provide accurate Islamic prayer times and related information. All data is fetched in real-time from their public API.

## Troubleshooting

### Server doesn't start
1. Check Python installation: `python --version`
2. Verify packages are installed: `pip list | grep mcp`
3. Ensure the file path in your config is correct
4. Check file permissions

### API calls fail
- Check your internet connection
- The Aladhan API might be temporarily unavailable
- Try again after a few minutes

### Missing dependencies
Install required packages:
```bash
pip install mcp requests
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install dependencies: `pip install -r requirements.txt`
5. Make your changes
6. Test with Claude Desktop

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Aladhan API](http://api.aladhan.com) for providing the Islamic prayer times data
- [Model Context Protocol](https://modelcontextprotocol.io/) for the communication standard
- The open-source community for inspiration and support

## Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/aladhan-mcp-server/issues) section
2. Create a new issue if your problem isn't already reported
3. Provide detailed information about your setup and the error

---

**Note:** This is an unofficial implementation using the Aladhan API. Please refer to their [terms of service](http://api.aladhan.com) for usage guidelines.
