class EvaluationManager :
    def __init__ (self ,database ,notification_service ):
        self .database =database 
        self .notification_service =notification_service 
        self .scores =[]
        self .average =None 
        self .outcome =None 

    def submitScore (self ,score ):
    # 16. (received via loop) Reviewer -> EvaluationManager : submitScore(score)
    # 17. EvaluationManager -> Database : saveScore(score)
        self .database .saveScore (score )

        self .scores .append (score )

    def startEvaluation (self ,reviewers ,submission ):
    # 15. (received) SubmissionController -> EvaluationManager : startEvaluation()
        self .scores =[]
        self .average =None 
        self .outcome =None 

        # 16. loop [each reviewer] : Reviewer -> EvaluationManager : submitScore(score)
        for reviewer in reviewers :
            reviewer .submitScore (self )

            # 18. Self-call : calculateAverage()
        self .calculateAverage ()
        # 19. Self-call : checkConsensus()
        self .checkConsensus ()
        # 20. Self-call : applyRules()
        self .applyRules ()

        # 21–23. inner alt based on outcome
        if self .outcome =="accepted":
        # 21. [accepted] EvaluationManager -> NotificationService : notifyAcceptance()
            self .notification_service .notifyAcceptance ()
        elif self .outcome =="rejected":
        # 22. [rejected] EvaluationManager -> NotificationService : notifyRejection()
            self .notification_service .notifyRejection ()
        else :
        # 23. [revision] EvaluationManager -> NotificationService : notifyRevision()
            self .notification_service .notifyRevision ()

    def calculateAverage (self ):
    # 18. Self-call : calculateAverage()
        if self .scores :
            self .average =sum (self .scores )/len (self .scores )
        else :
            self .average =0 

    def checkConsensus (self ):
    # 19. Self-call : checkConsensus()
        if not self .scores :
            self .outcome ="rejected"
            return 
        if (max (self .scores )-min (self .scores ))>3 :
            self .outcome ="revision"

    def applyRules (self ):
    # 20. Self-call : applyRules()

        if self .outcome =="revision":
            return 
        if self .average >=7 :
            self .outcome ="accepted"
        elif self .average >=4 :
            self .outcome ="revision"
        else :
            self .outcome ="rejected"