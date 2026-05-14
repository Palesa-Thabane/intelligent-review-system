class ReviewerManager:
    def __init__(self, database):
        self.database = database

    def getAvailableReviewers(self, submission):
        # 8. SubmissionController → ReviewerManager : getAvailableReviewers(submission)
        # 9. ReviewerManager → Database : fetchReviewers()
        reviewer_list = self.database.fetchReviewers()
        # 10. (return) Database → ReviewerManager : reviewerList

        # 11. self-call : ReviewerManager → ReviewerManager : filterReviewers(reviewerList, submission)
        filtered = self.filterReviewers(reviewer_list, submission)

        # 12. (return) ReviewerManager → SubmissionController : filteredReviewers
        return filtered

    def filterReviewers(self, reviewer_list, submission):
        # 11. self-call : ReviewerManager → ReviewerManager : filterReviewers(reviewerList, submission)
        author_id = submission.get("author_id") if submission else None
        return [
            r for r in reviewer_list
            if author_id not in r.conflict_ids
            and r.current_workload < r.max_workload
        ]
