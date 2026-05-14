class SubmissionController:
    def __init__(self, validator, database, reviewer_manager,
                 evaluation_manager, notification_service, ui):
        self.validator = validator
        self.database = database
        self.reviewer_manager = reviewer_manager
        self.evaluation_manager = evaluation_manager
        self.notification_service = notification_service
        self.ui = ui

    def submit(self, data):
        # 2. (received) UI → SubmissionController : submit(data)
        # 3. SubmissionController → Validator : validateFormat(data)
        result = self.validator.validateFormat(data)
        # 4. (return) Validator → SubmissionController : valid / invalid

        if result == "invalid":
            # 5. alt [invalid] : SubmissionController → UI : returnError()
            self.ui.returnError("Submission format is invalid.")
            return

        # 6. alt [valid] : SubmissionController → Database : saveSubmission(data)
        self.database.saveSubmission(data)
        # Step 7 (confirmation return) REMOVED – unused, reduces unnecessary interaction

        # 8. SubmissionController → ReviewerManager : getAvailableReviewers(submission)
        filtered_reviewers = self.reviewer_manager.getAvailableReviewers(data)
        # 12. (return) ReviewerManager → SubmissionController : filteredReviewers

        if not filtered_reviewers:
            # 13. alt [no reviewers] : SubmissionController → NotificationService : notifyRejection()
            self.notification_service.notifyRejection()
            return

        # loop [assign each reviewer]
        for reviewer in filtered_reviewers:
            # 14. SubmissionController → Reviewer : assignReview(submission)
            reviewer.assignReview(data)

        # 15. SubmissionController → EvaluationManager : startEvaluation(filteredReviewers, submission)
        self.evaluation_manager.startEvaluation(filtered_reviewers, data)
