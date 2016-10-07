import os
import time
from slackclient import SlackClient
from zomato_api import get_categories, get_random_restaurant
import json
from dotenv import load_dotenv
load_dotenv(".env")

# adapted from https://www.fullstackpython.com/blog/build-first-slack-bot-python.html


BOT_ID = os.environ.get("BOT_ID")
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
# constants
AT_BOT = "<@" + BOT_ID + ">"
# instantiate Slack & Twilio clients
slack_client = SlackClient(SLACK_BOT_TOKEN)


def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response ='Not sure what you mean. Available commands: \n `random` to get a random restaurant \n `random _number_` to get a random restaurant from a category \n `categories` to list available restaurant categories'

    if command.startswith('categories'):
        response = get_categories()
        print response

    elif command.startswith('random'):
        if len(command)==6:
            response = get_random_restaurant()

        elif command[7:].isdigit():
            response = get_random_restaurant(category=command[7:])

        else:
            response = get_random_restaurant(location=command[7:])
            
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    print slack_rtm_output
    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                   output['channel']

    return None, None


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("zomato-bot connected and running!")
        while True:
            command, channel = parse_slack_output(slack_client.rtm_read())

            if command and channel:
                handle_command(command, channel)
            time.sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
