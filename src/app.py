import os
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
        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_publish(
            # the user that opened your app"s app home
            user_id=event["user"],
            # the view object that appears in the app home
            view={
                "type": "home",
                "callback_id": "home_view",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Welcome to Movie Info! :tada:*"
                        }
                    },
                    {
                        "type": "divider"
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Click the button below to pick a movie."
                        }
                    },
                    {
                        "type": "actions",
                        "elements": [
                            {
                                "type": "button",
                                "text": {
                                    "type": "plain_text",
                                    "text": "Select a Movie!"
                                },
                                "action_id": "button_click"
                            }
                        ]
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error publishing home tab: {e}")


@app.action("button_click")
def action_button_click(ack, client, body, logger):
    try:
        ack()

        # views.publish is the method that your app uses to push a view to the Home tab
        client.views_open(
            trigger_id=body["trigger_id"],
            # the view object that appears in the app home
            view={
                "type": "modal",
                "callback_id": "movie_modal",
                "title": {
                    "type": "plain_text",
                    "text": "Movie Info"
                },
                "submit": {
                    "type": "plain_text",
                    "text": "Submit"
                },
                "close": {
                    "type": "plain_text",
                    "text": "Cancel"
                },
                "blocks": [
                    {
                        "type": "section",
                        "block_id": "movie_selection",
                        "text": {
                            "type": "mrkdwn",
                            "text": "Pick an item from the dropdown list"
                        },
                        "accessory": {
                            "action_id": "movie_search",
                            "type": "external_select",
                            "placeholder": {
                                    "type": "plain_text",
                                "text": "Select an item"
                            },
                            "min_query_length": 3
                        }
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error loading search window: {e}")


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
    client.chat_postMessage(blocks=new_payload, channel=user)
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
def handle_some_action(ack, body, logger):
    ack()
    logger.info(body)


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
