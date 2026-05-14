from researcher import Researcher 
from ui import UI 
from submission_controller import SubmissionController 
from validator import Validator 
from database import Database 
from reviewer_manager import ReviewerManager 
from evaluation_manager import EvaluationManager 
from notification_service import NotificationService 
from reviewer import Reviewer 






def build_system ():
    ui =UI ()
    validator =Validator ()
    database =Database ()
    notification_service =NotificationService (ui )
    evaluation_manager =EvaluationManager (database ,notification_service )
    reviewer_manager =ReviewerManager (database )
    submission_controller =SubmissionController (
    validator ,database ,reviewer_manager ,evaluation_manager ,ui 
    )
    ui .setSubmissionController (submission_controller )
    researcher =Researcher (ui )
    return researcher ,database 






def reset_reviewers (reviewers ):
    """Reset workload and assignments between scenarios."""
    for r in reviewers :
        r .current_workload =0 
        r .assigned_submissions =[]


def set_scores (reviewers ,scores ):
    """Assign a score to each reviewer (by position)."""
    for reviewer ,score in zip (reviewers ,scores ):
        reviewer .score =score 


def print_scenario_header (number ,title ,artefact_type ,author ,description ,expected ):
    print ()
    print ("="*60 )
    print (f"  SCENARIO {number }: {title }")
    print ("="*60 )
    print (f"  Artefact Type : {artefact_type }")
    print (f"  Author        : {author }")
    print (f"  Description   : {description }")
    print (f"  Expected      : {expected }")
    print ("-"*60 )






def main ():
    print ("="*60 )
    print ("     Intelligent Submission & Review System")
    print ("         Baseline Implementation - Task 1")
    print ("         Full 15-Scenario Test Suite")
    print ("="*60 )





    reviewer1 =Reviewer (
    reviewer_id =1 ,name ="Dr. Alice Mokoena",
    expertise ="Artificial Intelligence",conflict_ids =[],current_workload =0 
    )
    reviewer2 =Reviewer (
    reviewer_id =2 ,name ="Prof. Bob Nkosi",
    expertise ="Machine Learning",conflict_ids =[],current_workload =0 
    )
    reviewer3 =Reviewer (
    reviewer_id =3 ,name ="Dr. Charlie Dlamini",
    expertise ="Natural Language Processing",conflict_ids =[101 ],current_workload =0 
    )


    # ALT [INVALID] BRANCH — Scenarios 1–4



    researcher ,database =build_system ()
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =1 ,
    title ="Invalid — Missing Title (empty string)",
    artefact_type ="Conference Paper",
    author ="Lerato Sithole (Author ID: 102)",
    description ="Submission has an empty title field. "
    "Validator must catch it and return an error immediately.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({
    "title":"",
    "content":"This paper discusses cloud computing resource allocation.",
    "author_id":102 
    })


    researcher ,database =build_system ()
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =2 ,
    title ="Invalid — Missing Content (empty string)",
    artefact_type ="Technical Report",
    author ="Sipho Zulu (Author ID: 200)",
    description ="Submission has a valid title and author_id but an empty content field.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({
    "title":"A Study on Cloud Networks",
    "content":"",
    "author_id":200 
    })


    researcher ,database =build_system ()
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =3 ,
    title ="Invalid — Missing Author ID",
    artefact_type ="Research Paper",
    author ="Unknown",
    description ="Submission dict has no author_id key at all. "
    "Validator must reject it.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({
    "title":"Deep Learning in Healthcare",
    "content":"This paper explores neural networks applied to medical imaging."
    })


    researcher ,database =build_system ()
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =4 ,
    title ="Invalid — Completely Empty Submission",
    artefact_type ="N/A",
    author ="N/A",
    description ="An empty dict is submitted. Validator must reject it immediately.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({})


    # ALT [VALID] — OUTCOME BRANCHES — Scenarios 5–8


    # Scenario 5 — All reviewers available, high scores → ACCEPTED
    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =5 ,
    title ="Valid — All Reviewers Available, High Scores → Accepted",
    artefact_type ="Research Paper",
    author ="Thabo Nkosi (Author ID: 999)",
    description ="All three reviewers are eligible. Scores are high (8, 9, 7). "
    "Average >= 7, consensus reached → Accepted.",
    expected ="ACCEPTED"
    )

    # only reviewer1 & reviewer2 score. avg = (8+9)/2 = 8.5 → accepted.
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[8 ,9 ,7 ])
    researcher .submitResearchOutput ({
    "title":"Transformer Architectures for Low-Resource NLP",
    "content":"This paper proposes a novel transformer-based approach.",
    "author_id":999 
    })

    # Scenario 6 — All reviewers available, low scores → REJECTED
    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =6 ,
    title ="Valid — All Reviewers Available, Low Scores → Rejected",
    artefact_type ="Technical Report",
    author ="Sipho Zulu (Author ID: 200)",
    description ="All eligible reviewers score poorly (2, 1). "
    "Average < 4 → Rejected.",
    expected ="REJECTED"
    )
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[2 ,1 ,3 ])
    researcher .submitResearchOutput ({
    "title":"A Review of Deprecated Sorting Algorithms",
    "content":"This report examines bubble sort in modern systems.",
    "author_id":200 
    })

    # Scenario 7 — No consensus (scores too far apart) → REVISION
    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =7 ,
    title ="Valid — No Consensus (Scores Too Far Apart) → Revision",
    artefact_type ="Research Paper",
    author ="Naledi Dube (Author ID: 300)",
    description ="Scores diverge by more than 3 (e.g. 9 and 4). "
    "checkConsensus sets outcome to revision before applyRules.",
    expected ="REVISION"
    )
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[9 ,4 ,5 ])
    researcher .submitResearchOutput ({
    "title":"Emerging Trends in Quantum Computing for Cryptography",
    "content":"An exploratory survey of quantum algorithms.",
    "author_id":300 
    })

    # Scenario 8 — Middle-range average (4–6) → REVISION via applyRules
    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =8 ,
    title ="Valid — Middle-Range Average → Revision via applyRules",
    artefact_type ="Conference Paper",
    author ="Mpho Radebe (Author ID: 400)",
    description ="Scores are close enough for consensus (5, 6). "
    "Average = 5.5, which falls in [4, 7) → Revision via applyRules.",
    expected ="REVISION"
    )
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[5 ,6 ,5 ])
    researcher .submitResearchOutput ({
    "title":"Hybrid Cloud Architectures in Enterprise Settings",
    "content":"A comparative study of public and private cloud deployment models.",
    "author_id":400 
    })





    # Scenario 9 — All reviewers have conflicts → no reviewers assigned

    # Make all three have conflicts → empty filtered list.
    reviewer_all_conflict1 =Reviewer (
    reviewer_id =10 ,name ="Dr. Conflict A",
    expertise ="AI",conflict_ids =[999 ],current_workload =0 
    )
    reviewer_all_conflict2 =Reviewer (
    reviewer_id =11 ,name ="Dr. Conflict B",
    expertise ="ML",conflict_ids =[999 ],current_workload =0 
    )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_all_conflict1 )
    database .addReviewer (reviewer_all_conflict2 )

    print_scenario_header (
    number =9 ,
    title ="Edge Case — All Reviewers Have Conflicts → No Reviewers Assigned",
    artefact_type ="Research Paper",
    author ="Kagiso Motsepe (Author ID: 500)",
    description ="Every reviewer in the database has a conflict_id. "
    "filterConflicts returns an empty list. "
    "startEvaluation receives no reviewers; scores list is empty. "
    "checkConsensus immediately sets outcome to rejected.",
    expected ="REJECTED (no reviewers — empty scores list)"
    )
    researcher .submitResearchOutput ({
    "title":"Privacy-Preserving Federated Learning",
    "content":"Investigating federated approaches that maintain differential privacy.",
    "author_id":500 
    })

    # Scenario 10 — All reviewers at max workload → no reviewers assigned
    reviewer_full1 =Reviewer (
    reviewer_id =20 ,name ="Dr. Overloaded A",
    expertise ="AI",conflict_ids =[],current_workload =3 ,max_workload =3 
    )
    reviewer_full2 =Reviewer (
    reviewer_id =21 ,name ="Dr. Overloaded B",
    expertise ="ML",conflict_ids =[],current_workload =3 ,max_workload =3 
    )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_full1 )
    database .addReviewer (reviewer_full2 )

    print_scenario_header (
    number =10 ,
    title ="Edge Case — All Reviewers at Max Workload → No Reviewers Assigned",
    artefact_type ="Technical Report",
    author ="Zanele Mokoena (Author ID: 600)",
    description ="All reviewers pass conflict filtering but fail the workload check. "
    "checkWorkload returns an empty list. "
    "startEvaluation receives no reviewers → rejected.",
    expected ="REJECTED (no reviewers — workload exceeded)"
    )
    researcher .submitResearchOutput ({
    "title":"Scalable Microservice Orchestration Patterns",
    "content":"A review of Kubernetes-based orchestration strategies.",
    "author_id":600 
    })

    # Scenario 11 — Only one reviewer passes filtering → single-reviewer evaluation
    reviewer_solo =Reviewer (
    reviewer_id =30 ,name ="Dr. Solo Reviewer",
    expertise ="NLP",conflict_ids =[],current_workload =0 
    )
    reviewer_blocked =Reviewer (
    reviewer_id =31 ,name ="Dr. Blocked",
    expertise ="CV",conflict_ids =[777 ],current_workload =0 
    )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_solo )
    database .addReviewer (reviewer_blocked )

    print_scenario_header (
    number =11 ,
    title ="Edge Case — Only One Reviewer Passes Filtering",
    artefact_type ="Research Paper",
    author ="Bongani Sithole (Author ID: 700)",
    description ="One reviewer has no conflicts and is under workload limit. "
    "The other has a conflict. Single score (8) → average = 8.0 → Accepted.",
    expected ="ACCEPTED (single reviewer, score=8)"
    )
    reviewer_solo .score =8 
    researcher .submitResearchOutput ({
    "title":"Attention Mechanisms in Low-Resource Machine Translation",
    "content":"This paper investigates cross-lingual transfer for under-resourced languages.",
    "author_id":700 
    })


    # SCORE BOUNDARY / LOOP EDGE CASES — Scenarios 12–15



    reviewer_a =Reviewer (
    reviewer_id =40 ,name ="Dr. Zero Score",
    expertise ="AI",conflict_ids =[],current_workload =0 
    )
    reviewer_b =Reviewer (
    reviewer_id =41 ,name ="Dr. Also Zero",
    expertise ="ML",conflict_ids =[],current_workload =0 
    )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_a )
    database .addReviewer (reviewer_b )

    print_scenario_header (
    number =12 ,
    title ="Boundary — Scores of Exactly 0 → Rejected",
    artefact_type ="Conference Paper",
    author ="Lindiwe Dube (Author ID: 800)",
    description ="Both reviewers submit the minimum possible score (0). "
    "Average = 0.0, consensus holds (diff = 0). applyRules → Rejected.",
    expected ="REJECTED (average = 0)"
    )
    reviewer_a .score =0 
    reviewer_b .score =0 
    researcher .submitResearchOutput ({
    "title":"Revisiting Flat-File Databases in 2024",
    "content":"An argument for returning to flat-file storage in modern systems.",
    "author_id":800 
    })


    reviewer_c =Reviewer (
    reviewer_id =50 ,name ="Dr. Perfect Score",
    expertise ="AI",conflict_ids =[],current_workload =0 
    )
    reviewer_d =Reviewer (
    reviewer_id =51 ,name ="Dr. Also Perfect",
    expertise ="ML",conflict_ids =[],current_workload =0 
    )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_c )
    database .addReviewer (reviewer_d )

    print_scenario_header (
    number =13 ,
    title ="Boundary — Scores of Exactly 10 → Accepted",
    artefact_type ="Research Paper",
    author ="Simphiwe Khumalo (Author ID: 900)",
    description ="Both reviewers give the maximum score (10). "
    "Average = 10.0, consensus holds (diff = 0). applyRules → Accepted.",
    expected ="ACCEPTED (average = 10)"
    )
    reviewer_c .score =10 
    reviewer_d .score =10 
    researcher .submitResearchOutput ({
    "title":"Breakthrough in Self-Supervised Representation Learning",
    "content":"A landmark study achieving SOTA across twelve benchmarks.",
    "author_id":900 
    })

    # Scenario 14 — Average exactly on accepted threshold (7.0)
    reviewer_e =Reviewer (
    reviewer_id =60 ,name ="Dr. Threshold E",
    expertise ="AI",conflict_ids =[],current_workload =0 
    )
    reviewer_f =Reviewer (
    reviewer_id =61 ,name ="Dr. Threshold F",
    expertise ="ML",conflict_ids =[],current_workload =0 
    )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_e )
    database .addReviewer (reviewer_f )

    print_scenario_header (
    number =14 ,
    title ="Boundary — Average Exactly 7.0 → Accepted (>= 7 threshold)",
    artefact_type ="Technical Report",
    author ="Thandeka Ntuli (Author ID: 1000)",
    description ="Scores of 7 and 7 give an average of exactly 7.0. "
    "applyRules uses >= 7, so outcome must be Accepted, not Revision.",
    expected ="ACCEPTED (average = 7.0, on the >= 7 boundary)"
    )
    reviewer_e .score =7 
    reviewer_f .score =7 
    researcher .submitResearchOutput ({
    "title":"Explainable AI Techniques for Regulatory Compliance",
    "content":"Methods for making neural networks interpretable in high-stakes domains.",
    "author_id":1000 
    })

    # Scenario 15 — Average exactly on revision threshold (4.0)
    reviewer_g =Reviewer (
    reviewer_id =70 ,name ="Dr. Threshold G",
    expertise ="AI",conflict_ids =[],current_workload =0 
    )
    reviewer_h =Reviewer (
    reviewer_id =71 ,name ="Dr. Threshold H",
    expertise ="ML",conflict_ids =[],current_workload =0 
    )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_g )
    database .addReviewer (reviewer_h )

    print_scenario_header (
    number =15 ,
    title ="Boundary — Average Exactly 4.0 → Revision (>= 4 threshold)",
    artefact_type ="Conference Paper",
    author ="Dumisani Hlongwane (Author ID: 1100)",
    description ="Scores of 4 and 4 give an average of exactly 4.0. "
    "applyRules uses >= 4 for revision, so outcome must be Revision, not Rejected.",
    expected ="REVISION (average = 4.0, on the >= 4 boundary)"
    )
    reviewer_g .score =4 
    reviewer_h .score =4 
    researcher .submitResearchOutput ({
    "title":"Semi-Supervised Graph Neural Networks",
    "content":"An investigation into label-efficient training of GNNs on citation networks.",
    "author_id":1100 
    })

    print ()
    print ("="*60 )
    print ("  All 15 scenarios completed.")
    print ("="*60 )


if __name__ =="__main__":
    main ()