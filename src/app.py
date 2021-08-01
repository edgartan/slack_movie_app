import os
import json
import logging
from typing import Callable
from slack_bolt.async_app import AsyncApp
from slack_sdk import WebClient
from slack_bolt.adapter.aws_lambda import SlackRequestHandler
from api import MovieApis
import utils

# Initializes app
logging.basicConfig(filename='application.log', level=logging.DEBUG)
app = AsyncApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET",
                                  process_before_response=True)
)


@app.event("app_home_opened")
async def update_home_tab(client: WebClient, event: dict, logger: logging.Logger) -> None:
    try:
        with open('./views/home.json') as f:
            home = json.load(f)
        await client.views_publish(user_id=event["user"], view=home)

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("button_click")
async def action_button_click(ack: Callable, client: WebClient, body: dict, logger: logging.Logger) -> None:
    try:
        await ack()
        with open('./views/movie_modal.json') as f:
            movie_modal = json.load(f)
        await client.views_open(trigger_id=body["trigger_id"], view=movie_modal)

    except Exception as e:
        logger.error(f"Error loading movie search window: {e}")


# https://slack.dev/bolt-python/concepts#view_submissions
@app.view("movie_modal")
async def handle_movie_submission(ack: Callable, body: dict, client: WebClient, logger: logging.Logger) -> None:

    await ack()
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
        await client.chat_postMessage(blocks=movie_message,
                                      channel=user, text=payload)
    except Exception as e:
        payload = "💩 something went wrong. Try again!"
        logger.error("Couldn't send movie details to user")
        await client.chat_postMessage(text=payload, channel=user)


@app.options("movie_search")
async def show_list_of_movies(ack: Callable) -> None:
    # BUG: typeahead doesnt seem to be filtering on my external list
    movie_list = MovieApis.get_list_of_movies(5)
    await ack(options=movie_list)


@app.action("movie_search")
async def handle_action(ack: Callable) -> None:
    await ack()


# # Start your app
# if __name__ == "__main__":
#     app.start(port=int(os.environ.get("PORT", 3000)))
def handler(event, context):
    slack_handler = SlackRequestHandler(app=app)
    return slack_handler.handle(event, context)
