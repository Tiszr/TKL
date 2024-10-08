import logging
import requests

# Webhook URL for your Discord channel
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1292968892607762494/vosZnzgHGjuqr86PCAfeTUMcNWfIo7agbBXR698ZIJpwlCAiodJRgIBwRPXMRUuDSkN4"

def send_to_discord(message):
    """Send a message to the Discord channel via webhook."""
    data = {"content": message}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        if response.status_code == 204:
            logging.info("Message successfully sent to Discord.")
        else:
            logging.error(f"Failed to send message to Discord: {response.status_code}, {response.text}")
    except Exception as e:
        logging.error(f"Error sending message to Discord: {e}")

def plugin_start3(plugin_dir):
    """Called once when EDMC starts up, compatible with Python 3.x."""
    print("Thargoid Kill Logger plugin started")
    return "Thargoid Kill Logger v1"

def plugin_stop():
    """Called once when EDMC shuts down."""
    pass

def journal_entry(cmdr, is_beta, system, station, entry, state):
    """Called whenever a journal entry is received from Elite Dangerous."""
    # Only process if it's a Thargoid kill
    if entry.get("event") == "FactionKillBond" and "VictimFaction_Localised" in entry:
        if "Thargoid" in entry["VictimFaction_Localised"]:
            thargoid_kills = entry.get("Reward", 0)
            # Construct the message including the commander's name and reward
            message = f"{cmdr} killed a Thargoid, reward: {thargoid_kills:,} credits!"
            print(message)
            send_to_discord(message)  # Send the message to Discord

def plugin_prefs(parent):
    """Optional: create settings menu for your plugin."""
    pass

def prefs_changed():
    """Optional: handle changes in settings."""
    pass

# webhook for discord: https://discord.com/api/webhooks/1292968892607762494/vosZnzgHGjuqr86PCAfeTUMcNWfIo7agbBXR698ZIJpwlCAiodJRgIBwRPXMRUuDSkN4