class NotificationService:
    def __init__(self, ui):
        self.ui = ui
        self.notification = None

    def notifyAcceptance(self):
        # 21. [accepted] EvaluationManager -> NotificationService : notifyAcceptance()
        self.notification = "accepted"
        self.sendNotification()

    def notifyRejection(self):
        # 22. [rejected] EvaluationManager -> NotificationService : notifyRejection()
        self.notification = "rejected"
        self.sendNotification()

    def notifyRevision(self):
        # 23. [revision] EvaluationManager -> NotificationService : notifyRevision()
        self.notification = "revision"
        self.sendNotification()

    def sendNotification(self):
        # 24. NotificationService -> UI : sendNotification()
        self.ui.sendNotification(self.notification)