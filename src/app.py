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
    movie_id = values["movie_selection"]["movie_search"]["selected_option"]["value"]

    # TODO: Is there a way to source localized language that we could pass in here?
    data = MovieApis.get_movie_details(movie_id, "en-US")
    poster_path = data["poster_path"]
    poster_url = f"https://image.tmdb.org/t/p/w600_and_h900_bestv2/{poster_path}"

    new_payload = [
        {
            "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Here's is the movie info you requested!"
                    }
        },
        {
            "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": data["original_title"]
                    }
        },
        {
            "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Release date:* " + utils.convert_date(data["release_date"]) + " \n" + data["overview"]
                    },
            "accessory": {
                        "type": "image",
                        "image_url": poster_url,
                        "alt_text": "movie poster"
                    }
        }
    ]
    client.chat_postMessage(
        blocks=new_payload, channel=user, text='Movie info sent')
    payload = "Movie info sent"
    # try:
    #     client.chat_postMessage(blocks=new_payload)
    #     payload = "Movie info sent"
    # except Exception as e:
    #     payload = "something went wrong"
    # finally:
    #     client.chat_postMessage(text=payload)
    # return

# Example of responding to an external_select options request


@app.options("movie_search")
def show_options(ack):
    movie_list = MovieApis.get_list_of_movies(5)
    ack(options=movie_list)


@app.action("movie_search")
def handle_action():
    pass


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
