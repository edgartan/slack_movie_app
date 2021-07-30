from datetime import datetime


def convert_date(date):
    dt = datetime.strptime(date, "%Y-%m-%d")
    dt = dt.strftime("%b %d, %Y")
    return dt


# Start your app
if __name__ == "__main__":
    convert_date()
