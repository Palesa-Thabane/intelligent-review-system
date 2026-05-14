class UI:
    def __init__(self):
        self.submission_controller = None
        self.last_notification = None
    def setSubmissionController(self, controller):
        self.submission_controller = controller


    def submitResearchOutput(self, data):
        # 1. (received) UI receives from Researcher
        # 2. UI -> SubmissionController : submit(data)
        print(f"  [UI] submitResearchOutput called with title: '{data.get('title', '')}'")
        self.submission_controller.submit(data)

    def returnError(self, message):
        # 5. [invalid] SubmissionController -> UI : return error
        print(f"  [UI] Error returned: {message}")

    def sendNotification(self, message):
        # 24. NotificationService -> UI : sendNotification()  (final return)
        self.last_notification = message
        print(f"  [UI] Notification received: {message.upper()}")
