import sys
sys.path.insert(1, "lib/")

import utils
from api import MovieApis
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from slack_sdk import WebClient
from slack_bolt import App
from typing import Callable
import logging
import json
import os



# Initializes app
SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(level=logging.DEBUG)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"),
          signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
          process_before_response=True)


@app.event("app_home_opened")
def update_home_tab(client: WebClient, event: dict, logger: logging.Logger) -> None:
    try:
        with open('./views/home.json') as f:
            home = json.load(f)
        client.views_publish(user_id=event["user"], view=home)

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("button_click")
def action_button_click(ack: Callable, client: WebClient, body: dict, logger: logging.Logger) -> None:
    try:
        ack()
        with open('./views/movie_modal.json') as f:
            movie_modal = json.load(f)
        client.views_open(trigger_id=body["trigger_id"], view=movie_modal)

    except Exception as e:
        logger.error(f"Error loading movie search window: {e}")


# https://slack.dev/bolt-python/concepts#view_submissions
@app.view("movie_modal")
def handle_movie_submission(ack: Callable, body: dict, client: WebClient, logger: logging.Logger) -> None:

    ack()
    user = body["user"]["id"]
    values = body["view"]["state"]["values"]
    movie_id = values["movie_selection"]["movie_search"]["selected_option"]["value"]
    # TODO: Is there a way to source localized language that we could pass in here?
    data = MovieApis.get_movie_details(movie_id, "en-US")
    poster_path = data["poster_path"]
    poster_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster_path}"
    movie_message = utils.create_message_blocks(
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
def show_list_of_movies(ack: Callable) -> None:
    # BUG: typeahead doesnt seem to be filtering on my external list
    movie_list = MovieApis.get_list_of_movies(5)
    ack(options=movie_list)


@app.action("movie_search")
def handle_action(ack: Callable) -> None:
    ack()


def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)

# # Start your app
# if __name__ == "__main__":
#     app.start(port=int(os.environ.get("PORT", 3000)))
