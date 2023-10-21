# Usage

Set up python 3.11 venv

Install requirements.txt

Input twitch channel link when asked

# Good to know

Runs as an infinite loop, send a KeyboardInterrupt to stop it. (Default ctrl+c)

Doesn't use the twitch API so may break at any moment

Doesn't actually verify if its a twitch link either, so be careful :^)

Saves thumbnail locally without cleaning them, to enable cleaning, open the script and change line 50