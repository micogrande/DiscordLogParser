import re
import json
import argparse
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter

class DiscordLogParser:
    """A class to handle parsing and cleaning of Discord chat logs from https://github.com/Tyrrrz/DiscordChatExporter"""
    def __init__(self, input_file, output_file):
        self.input_file = Path(input_file)
        self.output_file = Path(output_file)
        self.log_pattern = r'\[(\d{1,2}/\d{1,2}/\d{4} \d{1,2}:\d{2} [APM]{2})\] (.*?)\n(.*?)(?=\n\[|\n{2,}|\Z)'
        self.chat_data = []
        self.user_message_lengths = defaultdict(list)
        self.speaker_counts = Counter()

    def process_line(self, line):
        """Process a single line of the chat log."""
        if "{Embed}" in line or "{Attachments}" in line:
            return  # Skip lines with embeds or attachments

        match = re.match(self.log_pattern, line.strip(), re.DOTALL)
        if match:
            timestamp = match.group(1).strip()
            speaker = match.group(2).strip()
            message = match.group(3).strip()

            if message.startswith("```") or "(pinned)" in speaker:
                return  # Skip messages with triple backticks or '(pinned)' usernames

            if message:  # Only add if there's actually a message
                self.chat_data.append({
                    "timestamp": timestamp,
                    "speaker": speaker,
                    "message": message
                })
                self.user_message_lengths[speaker].append(len(message))
                self.speaker_counts[speaker] += 1

    def process_file(self):
        """Process the entire chat log file and save as JSON."""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")

        with open(self.input_file, "r", encoding="utf-8") as file:
            content = file.read()
            matches = re.findall(self.log_pattern, content, re.DOTALL)
            for match in matches:
                timestamp, speaker, message = match
                if message.strip().startswith("```") or "{Embed}" in message or "(pinned)" in speaker:
                    continue
                self.chat_data.append({
                    "timestamp": timestamp.strip(),
                    "speaker": speaker.strip(),
                    "message": message.strip()
                })
                self.user_message_lengths[speaker.strip()].append(len(message.strip()))
                self.speaker_counts[speaker.strip()] += 1

        # Calculate user-specific metadata
        user_metadata = {}
        for user, lengths in self.user_message_lengths.items():
            user_metadata[user] = {
                "total_messages": self.speaker_counts[user],
                "shortest_message_length": min(lengths),
                "longest_message_length": max(lengths),
                "average_message_length": sum(lengths) / len(lengths)
            }

        # General metadata
        output_data = {
            "metadata": {
                "total_messages": len(self.chat_data),
                "unique_speakers": len(set(msg["speaker"] for msg in self.chat_data)),
                "processed_at": datetime.now().isoformat(),
                "source_file": str(self.input_file.name),
                "user_metadata": user_metadata
            },
            "messages": self.chat_data
        }

        # Save JSON
        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.output_file, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)

def main():
    """Handle command-line arguments and run the parser."""
    parser = argparse.ArgumentParser(
        description="Parse a Discord chat log and save it as a JSON file."
    )
    parser.add_argument(
        "input_file",
        help="Path to the input Discord chat log file."
    )
    parser.add_argument(
        "output_file",
        help="Path to the output JSON file where the parsed data will be saved."
    )

    args = parser.parse_args()

    try:
        parser = DiscordLogParser(args.input_file, args.output_file)
        parser.process_file()
        print(f"Successfully processed chat log to: {args.output_file}")
    except Exception as e:
        print(f"Error: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()