class Database:
    def __init__(self):
        self._submissions = {}
        self._scores = []
        self._reviewers = []
        self._submission_counter = 0

    def saveSubmission(self, data):
        # 6. (received) SubmissionController -> Database : saveSubmission(data)
        # 7. (return) Database --> SubmissionController : confirmation
        self._submission_counter += 1
        submission_id = self._submission_counter
        self._submissions[submission_id] = data
        return {"status": "confirmed", "submission_id": submission_id}

    def fetchReviewers(self):
         # 9. ReviewerManager -> Database : fetchReviewers()
        # 10. Database --> ReviewerManager : reviewerList (return)
        return self._reviewers

    def saveScore(self, score):
        # 17. EvaluationManager -> Database : saveScore(score)
        self._scores.append(score)

    def addReviewer(self, reviewer):
        self._reviewers.append(reviewer)
