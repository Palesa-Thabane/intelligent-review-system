class NotificationService:
    def __init__(self, ui):
        self.ui = ui
        self.notification = None

    def notifyAcceptance(self):
        # 19. alt [accepted] : EvaluationManager → NotificationService : notifyAcceptance()
        self.notification = "accepted"
        # 22. NotificationService → UI : sendNotification()
        self.sendNotification()

    def notifyRejection(self):
        # 20. alt [rejected] : EvaluationManager → NotificationService : notifyRejection()
        # 13. alt [no reviewers] : SubmissionController → NotificationService : notifyRejection()
        self.notification = "rejected"
        # 22. NotificationService → UI : sendNotification()
        self.sendNotification()

    def notifyRevision(self):
        # 21. alt [revision] : EvaluationManager → NotificationService : notifyRevision()
        self.notification = "revision"
        # 22. NotificationService → UI : sendNotification()
        self.sendNotification()

    def sendNotification(self):
        # 22. NotificationService → UI : sendNotification()
        self.ui.sendNotification(self.notification)
