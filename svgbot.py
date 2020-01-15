import os
import slack  # package name : slackclient (version 2+)
import ssl as ssl_lib
import certifi
import re
#

APP_NAME = '<@URAAZBY57>'  # ID code for Jean-Michel-Sauvegarde
KEY_WORD_SAVE = 'capitalise'


@slack.RTMClient.run_on(event='message')
def capitalise(**payload):

    try:
        # Get dict with all elements to have in json response
        webclient = payload['web_client']
        data = payload['data']
        # Sub elements in data
        text = str(data['text'])
        channel_id = data['channel']
        thread_ts = data['ts']
        user = data['user']

        # Check if jean-michel have been called
        if text.startswith(APP_NAME):

            # If yes, check the key word (for now only 'capitalise')
            if KEY_WORD_SAVE in text:

                # Get info from text
                text_clean = re.sub(APP_NAME, '', text)
                text_clean = re.sub(KEY_WORD_SAVE, '', text_clean)

                # Extract first link
                link = re.search("<https?://[^\s]+>", text_clean)

                # Check link presence
                if link:
                    url = link.group()
                    text_clean = re.sub(url, '', text_clean)
                    text_clean = text_clean.lower()  # lowercase for tags
                    tags = text_clean.split()

                    # Prepare row to write
                    tags_for_file = ';'.join(tags)
                    row = thread_ts + ',' + channel_id + str(url) + ',' + tags_for_file + '\n'

                    #  Writing into file
                    with open('savedlinks.csv', 'a') as fd:
                        fd.write(row)

                    # Answer to user
                    webclient.chat_postMessage(channel=channel_id,
                                               text="Merci <@{}>, '{}' enregistré avec les tags suivants : {}"
                                               .format(user, url, tags),
                                               thread_ts=thread_ts)

                else:
                    webclient.chat_postMessage(channel=channel_id,
                                               text="""Désolé <@{}>, une bonne structure est : '@jean-michel-sauvegarde capitalise http://lien.com tag1 tag2 ... tagX'."""
                                               .format(user),
                                               thread_ts=thread_ts)

            else:
                webclient.chat_postMessage(channel=channel_id,
                                           text="""Désolé <@{}>, une bonne structure est : '@jean-michel-sauvegarde capitalise http://lien.com tag1 tag2 ... tagX'."""
                                           .format(user),
                                           thread_ts=thread_ts)

    except KeyError:
        pass


if __name__ == "__main__":
    ssl_context = ssl_lib.create_default_context(cafile=certifi.where())  # for SSL connexion
    slack_token = os.environ.get('SLACK_BOT_TOKEN')  # export SLACK_BOT_TOKEN='Bot User Token' in venv terminal
    rtm_client = slack.RTMClient(token=slack_token, ssl=ssl_context)
    rtm_client.start()
#
