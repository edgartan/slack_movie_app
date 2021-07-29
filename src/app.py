import os
# Use the package we installed
from slack_bolt import App
from api import MovieApis

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
            # the user that opened your app's app home
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
                        "block_id": "section678",
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
                            "min_query_length": 2
                        }
                    }
                ]
            }
        )

    except Exception as e:
        logger.error(f"Error loading search window: {e}")


# https://slack.dev/bolt-python/concepts#view_submissions
@app.view('movie_modal')
def handle_movie_submission(ack, body, client, logger):
    ack()

    user = body["user"]["id"]
    values = body['view']['state']['values']
    movie_name = values['movie_input']['plain_text_input_action']

    #channel_id = values['channel']['id']['selected_channel']
    #message = values['custom']['message']['value']
    sender = body['user']

    new_payload = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "Hello! You've gotten a kudos :cherry_blossom:"
            }
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": movie_name
            },
        },
        {
            "type": "image",
            "image_url": "https://media.giphy.com/media/3oz8xEw5k7ae09nFFm/giphy.gif",
            "alt_text": "yayy"
        }
    ]
    try:
        client.chat_postMessage(blocks=new_payload)
        payload = "Hello Kudo-er! Your kudos has been delivered. "
    except Exception as e:
        payload = "something went wrong"
    finally:
        client.chat_postMessage(text=payload, channel=sender['id'])
    return

# Example of responding to an external_select options request


@app.options("movie_search")
def show_options(ack):
    movie_list = MovieApis.get_list_of_movies('en-US', 4)
    ack(options=movie_list)


# Start your app
if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
