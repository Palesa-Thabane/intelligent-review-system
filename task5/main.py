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
    validator ,database ,reviewer_manager ,
    evaluation_manager ,notification_service ,ui 
    )
    ui .setSubmissionController (submission_controller )
    researcher =Researcher (ui )
    return researcher ,database 


def reset_reviewers (reviewers ):
    for r in reviewers :
        r .current_workload =0 
        r .assigned_submissions =[]


def set_scores (reviewers ,scores ):
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
    print ("        Optimised Implementation - Task 5")
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
    number =1 ,title ="Invalid — Missing Title (empty string)",
    artefact_type ="Conference Paper",author ="Lerato Sithole (Author ID: 102)",
    description ="Empty title field. Validator must reject immediately.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({
    "title":"","content":"Cloud computing resource allocation.","author_id":102 
    })

    researcher ,database =build_system ()
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =2 ,title ="Invalid — Missing Content (empty string)",
    artefact_type ="Technical Report",author ="Sipho Zulu (Author ID: 200)",
    description ="Valid title and author_id but empty content.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({
    "title":"A Study on Cloud Networks","content":"","author_id":200 
    })

    researcher ,database =build_system ()
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =3 ,title ="Invalid — Missing Author ID",
    artefact_type ="Research Paper",author ="Unknown",
    description ="No author_id key. Validator must reject.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({
    "title":"Deep Learning in Healthcare",
    "content":"Neural networks applied to medical imaging."
    })

    researcher ,database =build_system ()
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =4 ,title ="Invalid — Completely Empty Submission",
    artefact_type ="N/A",author ="N/A",
    description ="Empty dict submitted. Validator must reject immediately.",
    expected ="ERROR — invalid format"
    )
    researcher .submitResearchOutput ({})


    # ALT [VALID] — OUTCOME BRANCHES — Scenarios 5–8


    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =5 ,title ="Valid — High Scores → Accepted",
    artefact_type ="Research Paper",author ="Thabo Nkosi (Author ID: 999)",
    description ="reviewer3 has conflict_id=101, not author_id=999, so all three pass "
    "filterReviewers. Scores (8,9,7). Average=8.0 >= 7 → Accepted.",
    expected ="ACCEPTED"
    )
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[8 ,9 ,7 ])
    researcher .submitResearchOutput ({
    "title":"Transformer Architectures for Low-Resource NLP",
    "content":"A novel transformer-based approach.",
    "author_id":999 
    })

    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =6 ,title ="Valid — Low Scores → Rejected",
    artefact_type ="Technical Report",author ="Sipho Zulu (Author ID: 200)",
    description ="All eligible reviewers score poorly. Average < 4 → Rejected.",
    expected ="REJECTED"
    )
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[2 ,1 ,3 ])
    researcher .submitResearchOutput ({
    "title":"A Review of Deprecated Sorting Algorithms",
    "content":"Bubble sort in modern systems.",
    "author_id":200 
    })

    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =7 ,title ="Valid — No Consensus → Revision",
    artefact_type ="Research Paper",author ="Naledi Dube (Author ID: 300)",
    description ="Scores diverge by more than 3. evaluateOutcome sets revision.",
    expected ="REVISION"
    )
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[9 ,4 ,5 ])
    researcher .submitResearchOutput ({
    "title":"Quantum Computing for Cryptography",
    "content":"Survey of quantum algorithms.",
    "author_id":300 
    })

    researcher ,database =build_system ()
    reset_reviewers ([reviewer1 ,reviewer2 ,reviewer3 ])
    database .addReviewer (reviewer1 )
    database .addReviewer (reviewer2 )
    database .addReviewer (reviewer3 )

    print_scenario_header (
    number =8 ,title ="Valid — Middle-Range Average → Revision via applyRules",
    artefact_type ="Conference Paper",author ="Mpho Radebe (Author ID: 400)",
    description ="Consensus reached. Average=5.5, in [4,7) → Revision.",
    expected ="REVISION"
    )
    set_scores ([reviewer1 ,reviewer2 ,reviewer3 ],[5 ,6 ,5 ])
    researcher .submitResearchOutput ({
    "title":"Hybrid Cloud Architectures",
    "content":"Public and private cloud deployment models.",
    "author_id":400 
    })





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
    number =9 ,title ="Edge Case — Author ID Matches Conflict → No Reviewers (Early Exit)",
    artefact_type ="Research Paper",author ="Kagiso Motsepe (Author ID: 999)",
    description ="filterReviewers now checks author_id=999 against conflict_ids. "
    "Both reviewers have conflict_ids=[999]. Early exit guard fires.",
    expected ="REJECTED (early exit — no eligible reviewers)"
    )
    researcher .submitResearchOutput ({
    "title":"Privacy-Preserving Federated Learning",
    "content":"Federated approaches maintaining differential privacy.",
    "author_id":999 
    })

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
    number =10 ,title ="Edge Case — All Reviewers at Max Workload → Early Exit",
    artefact_type ="Technical Report",author ="Zanele Mokoena (Author ID: 600)",
    description ="All reviewers fail workload check. filterReviewers returns empty. Early exit fires.",
    expected ="REJECTED (early exit — workload exceeded)"
    )
    researcher .submitResearchOutput ({
    "title":"Scalable Microservice Orchestration Patterns",
    "content":"Kubernetes-based orchestration strategies.",
    "author_id":600 
    })

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
    number =11 ,title ="Edge Case — Only One Reviewer Passes Filtering",
    artefact_type ="Research Paper",author ="Bongani Sithole (Author ID: 700)",
    description ="reviewer_blocked has conflict_id=777 which matches author_id=700? No — "
    "777 != 700, so both pass conflict check. But reviewer_blocked still has "
    "conflict_ids=[777]. author_id=700 not in [777] → both pass. "
    "reviewer_solo scores 8 → Accepted.",
    expected ="ACCEPTED (solo reviewer, score=8)"
    )
    reviewer_solo .score =8 
    reviewer_blocked .score =7 
    researcher .submitResearchOutput ({
    "title":"Attention Mechanisms in Machine Translation",
    "content":"Cross-lingual transfer for under-resourced languages.",
    "author_id":700 
    })


    # SCORE BOUNDARY / LOOP EDGE CASES — Scenarios 12–15


    reviewer_a =Reviewer (reviewer_id =40 ,name ="Dr. Zero Score",
    expertise ="AI",conflict_ids =[],current_workload =0 )
    reviewer_b =Reviewer (reviewer_id =41 ,name ="Dr. Also Zero",
    expertise ="ML",conflict_ids =[],current_workload =0 )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_a )
    database .addReviewer (reviewer_b )

    print_scenario_header (
    number =12 ,title ="Boundary — Scores of Exactly 0 → Rejected",
    artefact_type ="Conference Paper",author ="Lindiwe Dube (Author ID: 800)",
    description ="Both reviewers score 0. Average=0.0. evaluateOutcome → Rejected.",
    expected ="REJECTED (average = 0)"
    )
    reviewer_a .score =0 
    reviewer_b .score =0 
    researcher .submitResearchOutput ({
    "title":"Revisiting Flat-File Databases",
    "content":"Argument for flat-file storage in modern systems.",
    "author_id":800 
    })

    reviewer_c =Reviewer (reviewer_id =50 ,name ="Dr. Perfect Score",
    expertise ="AI",conflict_ids =[],current_workload =0 )
    reviewer_d =Reviewer (reviewer_id =51 ,name ="Dr. Also Perfect",
    expertise ="ML",conflict_ids =[],current_workload =0 )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_c )
    database .addReviewer (reviewer_d )

    print_scenario_header (
    number =13 ,title ="Boundary — Scores of Exactly 10 → Accepted",
    artefact_type ="Research Paper",author ="Simphiwe Khumalo (Author ID: 900)",
    description ="Both reviewers score 10. Average=10.0. evaluateOutcome → Accepted.",
    expected ="ACCEPTED (average = 10)"
    )
    reviewer_c .score =10 
    reviewer_d .score =10 
    researcher .submitResearchOutput ({
    "title":"Breakthrough in Self-Supervised Representation Learning",
    "content":"SOTA across twelve benchmarks.",
    "author_id":900 
    })

    reviewer_e =Reviewer (reviewer_id =60 ,name ="Dr. Threshold E",
    expertise ="AI",conflict_ids =[],current_workload =0 )
    reviewer_f =Reviewer (reviewer_id =61 ,name ="Dr. Threshold F",
    expertise ="ML",conflict_ids =[],current_workload =0 )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_e )
    database .addReviewer (reviewer_f )

    print_scenario_header (
    number =14 ,title ="Boundary — Average Exactly 7.0 → Accepted",
    artefact_type ="Technical Report",author ="Thandeka Ntuli (Author ID: 1000)",
    description ="Scores of 7 and 7. Average=7.0. evaluateOutcome uses >= 7 → Accepted.",
    expected ="ACCEPTED (average = 7.0)"
    )
    reviewer_e .score =7 
    reviewer_f .score =7 
    researcher .submitResearchOutput ({
    "title":"Explainable AI for Regulatory Compliance",
    "content":"Methods for interpretable neural networks.",
    "author_id":1000 
    })

    reviewer_g =Reviewer (reviewer_id =70 ,name ="Dr. Threshold G",
    expertise ="AI",conflict_ids =[],current_workload =0 )
    reviewer_h =Reviewer (reviewer_id =71 ,name ="Dr. Threshold H",
    expertise ="ML",conflict_ids =[],current_workload =0 )

    researcher ,database =build_system ()
    database .addReviewer (reviewer_g )
    database .addReviewer (reviewer_h )

    print_scenario_header (
    number =15 ,title ="Boundary — Average Exactly 4.0 → Revision",
    artefact_type ="Conference Paper",author ="Dumisani Hlongwane (Author ID: 1100)",
    description ="Scores of 4 and 4. Average=4.0. evaluateOutcome uses >= 4 → Revision.",
    expected ="REVISION (average = 4.0)"
    )
    reviewer_g .score =4 
    reviewer_h .score =4 
    researcher .submitResearchOutput ({
    "title":"Semi-Supervised Graph Neural Networks",
    "content":"Label-efficient training of GNNs on citation networks.",
    "author_id":1100 
    })

    print ()
    print ("="*60 )
    print ("  All 15 scenarios completed.")
    print ("="*60 )


if __name__ =="__main__":
    main ()
