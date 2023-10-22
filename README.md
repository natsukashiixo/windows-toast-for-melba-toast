# Usage

Set up python 3.11 venv

Install requirements.txt

link to Melba Toast is hardcoded because this is a shitpost

# Good to know

Runs as an infinite loop, send a KeyboardInterrupt to stop it. (Default ctrl+c)

Doesn't use the twitch API so may break at any moment

Saves thumbnail locally without cleaning them, to enable cleaning, open the script and change line 50

If you for some reason want to use this for other channels, you can either change the link or uncomment line 61 and change all instances of `MELBA_TOAST` in `__main__` to `twitch_link`