class EvaluationManager:
    def __init__(self, database, notification_service):
        self.database = database
        self.notification_service = notification_service
        self.scores = []
        self.outcome = None

    def submitScore(self, score):
        # 16. (received) Reviewer → EvaluationManager : submitScore(score)
        self.scores.append(score)

    def startEvaluation(self, reviewers, submission):
        # 15. (received) SubmissionController → EvaluationManager : startEvaluation(filteredReviewers, submission)
        self.scores = []
        self.outcome = None

        # loop [each reviewer] : Reviewer → EvaluationManager : submitScore(score)
        for reviewer in reviewers:
            reviewer.submitScore(self)

        # 17. EvaluationManager → Database : saveScores(allScores)
        self.database.saveScores(self.scores)

        # 18. self-call : EvaluationManager → EvaluationManager : evaluateOutcome()
        self.evaluateOutcome()

        if self.outcome == "accepted":
            # 19. alt [accepted] : EvaluationManager → NotificationService : notifyAcceptance()
            self.notification_service.notifyAcceptance()
        elif self.outcome == "rejected":
            # 20. alt [rejected] : EvaluationManager → NotificationService : notifyRejection()
            self.notification_service.notifyRejection()
        else:
            # 21. alt [revision] : EvaluationManager → NotificationService : notifyRevision()
            self.notification_service.notifyRevision()

    def evaluateOutcome(self):
        # 18. self-call : EvaluationManager → EvaluationManager : evaluateOutcome()
        if not self.scores:
            self.outcome = "rejected"
            return
        average = sum(self.scores) / len(self.scores)
        score_range = max(self.scores) - min(self.scores)
        if score_range > 3:
            self.outcome = "revision"
        elif average >= 7:
            self.outcome = "accepted"
        elif average >= 4:
            self.outcome = "revision"
        else:
            self.outcome = "rejected"
