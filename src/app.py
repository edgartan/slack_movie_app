import os
import json
from slack_bolt import App
from api import MovieApis
import utils

# Initializes your app with your bot token and signing secret
app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)


@app.event("app_home_opened")
def update_home_tab(client, event, logger):
    try:
        with open('./views/home.json') as f:
            home = json.load(f)
        client.views_publish(user_id=event["user"], view=home)

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("button_click")
def action_button_click(ack, client, body, logger):
    try:
        ack()
        with open('./views/movie_modal.json') as f:
            movie_modal = json.load(f)
        client.views_open(trigger_id=body["trigger_id"], view=movie_modal)

    except Exception as e:
        logger.error(f"Error loading movie search window: {e}")


# https://slack.dev/bolt-python/concepts#view_submissions
@app.view("movie_modal")
def handle_movie_submission(ack, body, client, logger):

    ack()
    user = body["user"]["id"]
    values = body["view"]["state"]["values"]
    movie_id = values["movie_selection"]["movie_search"]["movie_search"]["value"]

    # TODO: Is there a way to source localized language that we could pass in here?
    data = MovieApis.get_movie_details(movie_id, "en-US")
    poster_path = data["poster_path"]
    poster_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster_path}"
    movie_message = utils.create_message_block(
        data["original_title"], data["release_date"], data["overview"], poster_url)

    try:
        payload = "Movie info sent"
        client.chat_postMessage(blocks=movie_message,
                                channel=user, text=payload)
    except Exception as e:
        payload = "💩 something went wrong. Try again!"
        logger.error("Couldn't send movie details to user")
        client.chat_postMessage(text=payload, channel=user)


@app.options("movie_search")
def show_list_of_movies(ack):
    movie_list = MovieApis.get_list_of_movies(5)
    ack(options=movie_list)


@app.action("movie_search")
def handle_action(ack):
    ack()


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
