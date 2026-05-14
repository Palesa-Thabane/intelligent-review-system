class ReviewerManager:
    def __init__(self, database):
        self.database = database

    def getAvailableReviewers(self, submission):
        # 8. (received) SubmissionController -> ReviewerManager : getAvailableReviewers()
        # 9. ReviewerManager -> Database : fetchReviewers()
        reviewer_list = self.database.fetchReviewers()
        # 10. Database --> ReviewerManager : reviewerList (return)
        if not reviewer_list:
            # 13. return empty list
            return []
        # 11. Reviewer -> Reviewer : filterConflicts(reviewerList) (self-call inside applyFilters)
        # 12. Reviewer -> Reviewer : checkWorkload(reviewerList) (self-call inside applyFilters)
        representative = reviewer_list[0]
        # 13. ReviewerManager --> SubmissionController : filteredReviewers (return)
        return representative.applyFilters(reviewer_list)