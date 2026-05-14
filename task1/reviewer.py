class Reviewer:
    def __init__(self, reviewer_id, name, expertise, conflict_ids=None,
                 current_workload=0, max_workload=3):
        self.reviewer_id = reviewer_id
        self.name = name
        self.expertise = expertise
        self.conflict_ids = conflict_ids if conflict_ids else []
        self.current_workload = current_workload
        self.max_workload = max_workload
        self.assigned_submissions = []
        self.score = None

    def filterConflicts(self, reviewer_list):
         # 11. Self-call on Reviewer : filterConflicts(reviewerList)
        return [r for r in reviewer_list if not r.conflict_ids]

    def checkWorkload(self, reviewer_list):
         # 12. Self-call on Reviewer : checkWorkload(reviewerList)
        return [r for r in reviewer_list if r.current_workload < r.max_workload]

    def assignReview(self, submission):
         # 14. SubmissionController -> Reviewer : assignReview() (inside loop)
        self.assigned_submissions.append(submission)
        self.current_workload += 1

    def submitScore(self, evaluation_manager):
        # 16. (loop) Reviewer -> EvaluationManager : submitScore(score)
        score_to_submit = self.score if self.score is not None else 5
        evaluation_manager.submitScore(score_to_submit)  

    def applyFilters(self, reviewer_list):
        """Self‑call sequence: filterConflicts → checkWorkload."""
        # 11. filterConflicts self-call
        filtered = self.filterConflicts(reviewer_list)
         # 12. checkWorkload self-call
        filtered = self.checkWorkload(filtered)
        return filtered