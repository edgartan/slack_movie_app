from datetime import datetime


def convert_date(date):
    dt = datetime.strptime(date, "%Y-%m-%d")
    dt = dt.strftime("%b %d, %Y")
    return dt


def create_message_blocks(title, date, overview, poster_url):
    movie_message = [
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
                        "text": title
                    }
        },
        {
            "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Release date:* " + convert_date(date) + " \n" + overview
                    },
            "accessory": {
                        "type": "image",
                        "image_url": poster_url,
                        "alt_text": "movie poster"
                    }
        }
    ]
    return movie_message


# Start your app
if __name__ == "__main__":
    convert_date()
