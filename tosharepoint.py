from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.file import File
import pandas as pd
url = 'https://saegus.sharepoint.com/sites/teamdata'

ctx_auth = AuthenticationContext(url)
ctx_auth.acquire_token_for_user('eliot.moll@saegus.com', 'xxx')
ctx = ClientContext(url, ctx_auth)
response = File.open_binary(ctx, "/Documents%20partages/Forms/AllItems.aspx?viewid=92b75299%2D2a3a%2D49a2%2Daa0e%2D99d89fb976a7&id=%2Fsites%2Fteamdata%2FDocuments%20partages%2FVeille%2FVeille%20Slack/veille.csv")
with open("./veille.csv", "wb") as local_file:
    local_file.write(response.content)


