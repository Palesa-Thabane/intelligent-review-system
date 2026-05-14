class Database:
    def __init__(self):
        self._submissions = {}
        self._scores = []
        self._reviewers = []
        self._submission_counter = 0

    def saveSubmission(self, data):
        # 6. alt [valid] : SubmissionController → Database : saveSubmission(data)
        # Step 7 (confirmation return) REMOVED – return value is not used by caller
        self._submission_counter += 1
        submission_id = self._submission_counter
        self._submissions[submission_id] = data

    def fetchReviewers(self):
        # 9. ReviewerManager → Database : fetchReviewers()
        # 10. (return) Database → ReviewerManager : reviewerList
        return self._reviewers

    def saveScores(self, scores):
        # 17. EvaluationManager → Database : saveScores(allScores)
        self._scores.extend(scores)

    def addReviewer(self, reviewer):
        self._reviewers.append(reviewer)
