from office365.runtime.auth.authentication_context import AuthenticationContext
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.file import File
import pandas as pd
url = 'https://s.'

ctx_auth = AuthenticationContext(url)
ctx_auth.acquire_token_for_user('e.com', 'xxx')
ctx = ClientContext(url, ctx_auth)
response = File.open_binary(ctx, "/veille.csv")
with open("./veille.csv", "wb") as local_file:
    local_file.write(response.content)


