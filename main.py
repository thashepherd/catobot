import os
import time
from secrets import SLACK_BOT_TOKEN
from slackclient import SlackClient

BOT_NAME = 'catobot'
SLACK_BOT_ID='U3ATS8F8T'
SLACK_BOT_TOKEN=SLACK_BOT_TOKEN
AT_BOT = "<@" + SLACK_BOT_ID + ">"
READ_WEBSOCKET_DELAY = 1

slack_client = SlackClient(SLACK_BOT_TOKEN)

def rubicon(_=None):
  return "Iacta alea est"

def delenda(thing):
  return "Cetero censeo {0} delenda est!".format(thing)

def handle_command(channel, command, arg):
  response = command(arg)
  #response = delenda(command)
  slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
  output_list = slack_rtm_output
  if output_list and len(output_list) > 0:
    for output in output_list:
      if output and 'text' in output:
        if AT_BOT in output['text']:
          return delenda, output['text'].split(AT_BOT)[1].strip(), output['channel']
        elif "rubicon" in output['text'].lower():
          return rubicon, None, output['channel']
  return None, None

if __name__ == "__main__":
  if slack_client.rtm_connect():
    print(BOT_NAME + " has connected.")
    while True:
      command, arg, channel = parse_slack_output(slack_client.rtm_read())
      if command and channel:
        handle_command(command, channel)
        time.sleep(READ_WEBSOCKET_DELAY)
  else:
    print("Connection failed. Invalid slack token (" + SLACK_BOT_TOKEN + ") or bot ID (" + SLACK_BOT_ID + ")?")
