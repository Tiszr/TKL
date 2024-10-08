import logging
import requests
import threading

# Set up logging to a file
logging.basicConfig(filename="thargoid_kill_logger.log", level=logging.DEBUG)

# Webhook URL for Discord (replace with your actual webhook URL)
WEBHOOK_URL = "https://discord.com/api/webhooks/1292968892607762494/vosZnzgHGjuqr86PCAfeTUMcNWfIo7agbBXR698ZIJpwlCAiodJRgIBwRPXMRUuDSkN4"

# Helper function to match fields in journal entries
def matches(entry, field, value):
    return entry.get(field) == value

# Function to send data to Discord via Webhook
def send_to_discord(cmdr, system, reward):
    payload = {
        "content": f"Commander {cmdr} has earned {reward} credits from a Thargoid kill in the {system} system."
    }
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        response.raise_for_status()
        logging.info(f"Successfully sent Thargoid kill info for cmdr {cmdr} to Discord.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to send data to Discord: {e}")

# Non-blocking submission to Discord
def send_to_discord_threaded(cmdr, system, reward):
    thread = threading.Thread(target=send_to_discord, args=(cmdr, system, reward))
    thread.start()

# Journal entry function (called by EDMC)
def journal_entry(cmdr, is_beta, system, station, entry, state):
    """
    Called when a new journal entry is received by EDMC.
    """
    logging.debug(f"Journal entry received: {entry}")
    
    # Check for FactionKillBond event and ensure the VictimFaction is either Thargoid or Guardian
    if entry.get('event') == 'FactionKillBond' and (
        matches(entry, 'VictimFaction', '$faction_Thargoid;') or
        matches(entry, 'VictimFaction', '$faction_Guardian;')
    ):
        reward = entry.get('Reward', 0)  # Get the reward value
        logging.info(f"Thargoid/Guardian kill logged for cmdr {cmdr}: {reward} credits.")
        
        # Send the reward data to Discord in a separate thread
        send_to_discord_threaded(cmdr, system, reward)
    else:
        logging.debug(f"No relevant event found in entry: {entry.get('event')}")

# Function to handle plugin startup
def plugin_start3(plugin_dir):
    """
    This function is called once when the plugin is loaded.
    """
    logging.info("Thargoid Kill Logger plugin started.")
    return "Thargoid Kill Logger v1"

# Plugin shutdown function (optional)
def plugin_stop():
    """
    Called once when EDMC shuts down.
    """
    logging.info("Thargoid Kill Logger plugin stopped.")

# Preferences window for the plugin (optional)
def plugin_prefs(parent):
    """
    Optional: create settings menu for your plugin.
    """
    pass

# Preferences changed handler (optional)
def prefs_changed():
    """
    Optional: handle changes in plugin settings.
    """
    logging.debug("Plugin preferences changed.")
