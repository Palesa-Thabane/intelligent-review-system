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

    def assignReview(self, submission):
        # 14. loop [assign each reviewer] : SubmissionController → Reviewer : assignReview(submission)
        self.assigned_submissions.append(submission)
        self.current_workload += 1

    def submitScore(self, evaluation_manager):
        # 16. loop [each reviewer] : Reviewer → EvaluationManager : submitScore(score)
        score_to_submit = self.score if self.score is not None else 5
        evaluation_manager.submitScore(score_to_submit)
