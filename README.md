# Discord Log Parser

## Overview
This script is designed to work with `.txt` logs produced by [DiscordChatExporter](https://github.com/Tyrrrz/DiscordChatExporter).

This script parses a Discord chat log, extracts useful metadata, and saves the parsed data into a JSON file. It also computes user-specific statistics such as the number of messages sent, as well as the shortest, longest, and average message lengths for each user in the chat.


## Features
- **Parse Discord Logs**: Extracts messages along with timestamps and usernames.
- **Metadata Collection**:
  - Total messages.
  - Unique speakers.
  - Shortest, longest, and average message lengths (overall and per user).
  - Top speakers by message count.
- **Output**: Saves parsed data and metadata to a JSON file.

## Usage
Run the script from the command line as follows:
```bash
python discord_log_parser.py <input_file> <output_file>
```

### Arguments
- `<input_file>`: Path to the `.txt` chat log.
- `<output_file>`: Path to the output JSON file where the parsed data will be saved.

### Example
```bash
python discord_log_parser.py chat_log.txt parsed_data.json
```

## Output JSON Structure
The output JSON file contains the following structure:

```json
{
  "metadata": {
    "total_messages": 100,
    "unique_speakers": 10,
    "processed_at": "YYYY-MM-DDTHH:MM:SS",
    "source_file": "chat_log.txt",
    "user_metadata": {
      "username1": {
        "total_messages": 20,
        "shortest_message_length": 5,
        "longest_message_length": 150,
        "average_message_length": 45.6
      },
      "username2": {
        "total_messages": 15,
        "shortest_message_length": 8,
        "longest_message_length": 120,
        "average_message_length": 30.2
      }
    }
  },
  "messages": [
    {
      "timestamp": "12/25/2024 10:00 AM",
      "speaker": "username1",
      "message": "Hello, everyone!"
    },
    {
      "timestamp": "12/25/2024 10:05 AM",
      "speaker": "username2",
      "message": "Hi there!"
    }
  ]
}
```