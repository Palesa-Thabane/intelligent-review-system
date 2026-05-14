class SubmissionController:

    def __init__(self, validator, database, reviewer_manager, evaluation_manager, ui):
        self.validator = validator
        self.database = database
        self.reviewer_manager = reviewer_manager
        self.evaluation_manager = evaluation_manager
        self.ui = ui

    def submit(self, data):
        # 2. (received) UI -> SubmissionController : submit(data)
        # 3. SubmissionController -> Validator : validateFormat(data)
        result = self.validator.validateFormat(data)

        # 4. Validator --> SubmissionController : valid/invalid (return)
        if result == "invalid":
            # 5. [invalid] SubmissionController -> UI : return error
            self.ui.returnError("Submission format is invalid.")
            return

        # 6. [valid] SubmissionController -> Database : saveSubmission(data)
        confirmation = self.database.saveSubmission(data)
        # 7. Database --> SubmissionController : confirmation (return)
        print(f"  [SubmissionController] Submission saved: {confirmation}")

        # 8. SubmissionController -> ReviewerManager : getAvailableReviewers()
        filtered_reviewers = self.reviewer_manager.getAvailableReviewers(data)
        # 13. ReviewerManager --> SubmissionController : filteredReviewers (return)
        print(f"  [SubmissionController] Filtered reviewers: {[r.name for r in filtered_reviewers]}")

        # 14. loop [each reviewer] : SubmissionController -> Reviewer : assignReview()
        for reviewer in filtered_reviewers:
            reviewer.assignReview(data)

        # 15. SubmissionController -> EvaluationManager : startEvaluation()
        self.evaluation_manager.startEvaluation(filtered_reviewers, data)