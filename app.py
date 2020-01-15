import os
import slack
import ssl as ssl_lib
import certifi
import re

APP_NAME = '<@URAAZBY57>'


@slack.RTMClient.run_on(event='message')
def capitalise(**payload):
    # Get dict with all info
    data = payload['data']

    # Un try serait plus adapté ?
    if 'text' in data and 'user' in data:
        text = str(data['text'])

        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        if text.startswith(APP_NAME):
            if 'capitalise' in text:

                # Get info from text
                text_clean = re.sub(APP_NAME, '', text)
                text_clean = re.sub('capitalise', '', text_clean)

                # Extract first link
                link = re.search("<https?://[^\s]+>", text_clean)

                # Check link presence
                if link:
                    url = link.group()
                    text_clean = re.sub(url, '', text_clean)

                    tags = text_clean.split()

                    # Writing into file
                    tags_for_file = ';'.join(tags)
                    row = thread_ts + ',' + str(url) + ',' + tags_for_file + '\n'
                    with open('savedlinks.csv', 'a') as fd:
                        fd.write(row)

                    # Answer to user
                    webclient = payload['web_client']
                    webclient.chat_postMessage(
                        channel=channel_id,
                        text="Merci <@{}>, '{}' enregistré avec les tags suivants: {}".format(user, url, tags),
                        thread_ts=thread_ts)

                else:
                    webclient = payload['web_client']
                    webclient.chat_postMessage(channel=channel_id,
                                               text="Désolé <@{}>, une bonne structure est: '@jean-michel-sauvegarde capitalise http://tonlien.com tag1 tag2 ... tagX'.".format(
                                                   user),
                                               thread_ts=thread_ts)

            else:
                webclient = payload['web_client']
                webclient.chat_postMessage(channel=channel_id,
                        text="Désolé <@{}>, une bonne structure est: '@jean-michel-sauvegarde capitalise http://tonlien.com tag1 tag2 ... tagX'.".format(user),
                        thread_ts=thread_ts)


if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())
    slack_token = 'xoxb-790886708917-860373406177-Tsc5FXkEJJVv10HZUcaJ9DJm'  # os.environ['SLACK_BOT_TOKEN']
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
#
