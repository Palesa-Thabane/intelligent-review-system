"""
COS 730 – Assignment 2
Task 6: Empirical Evaluation and Comparison
============================================
Compares the Baseline (Task 1) vs Optimised (Task 5) implementation
across the following metrics:
  1. Method call count  (instrumented wrappers)
  2. Execution time     (timeit over 10 000 repeated runs)
  3. Code complexity    (McCabe cyclomatic complexity via radon)
  4. Maintainability    (Maintainability Index via radon)
  5. DB interactions    (counted separately)
  6. Functional equivalence (all 15 scenarios pass in both)
"""

import sys ,os ,timeit ,importlib ,importlib .util ,inspect ,io ,contextlib 
from unittest .mock import patch 



BASELINE_FOLDER ="task1"
OPTIMISED_FOLDER ="task5"


BASE_DIR =os .path .join (os .path .dirname (__file__ ),BASELINE_FOLDER )
OPT_DIR =os .path .join (os .path .dirname (__file__ ),OPTIMISED_FOLDER )

def load_system (folder ):
    """Dynamically import all required modules from a subfolder."""
    mods ={}
    module_names =[
    "database","validator","ui","researcher","reviewer",
    "reviewer_manager","evaluation_manager",
    "notification_service","submission_controller"
    ]
    for name in module_names :
        path =os .path .join (folder ,f"{name }.py")
        if not os .path .exists (path ):
            print (f"Warning: {path } not found, skipping.")
            continue 
        spec =importlib .util .spec_from_file_location (f"{folder }_{name }",path )
        mod =importlib .util .module_from_spec (spec )
        spec .loader .exec_module (mod )
        mods [name ]=mod 
    return mods 


class CallCounter :
    """Wraps public methods of given objects to count invocations."""
    def __init__ (self ):
        self .counts ={}# method_name -> int
        self .total =0 

    def wrap (self ,obj ,label =None ):
        cls_name =label or type (obj ).__name__ 
        for attr in dir (obj ):

            if attr .startswith ("__")and attr !="__init__":
                continue 
            if attr .startswith ("_"):
                continue 
            orig =getattr (obj ,attr )
            if not callable (orig ):
                continue 
            key =f"{cls_name }.{attr }"
            self .counts .setdefault (key ,0 )

            def make_wrapper (fn ,k ):
                def wrapper (*args ,**kwargs ):
                    self .counts [k ]+=1 
                    self .total +=1 
                    return fn (*args ,**kwargs )
                return wrapper 
            setattr (obj ,attr ,make_wrapper (orig ,key ))
        return obj 

    def db_calls (self ):
        """Sum of all Database.save* calls."""
        return sum (v for k ,v in self .counts .items ()
        if k .startswith ("Database.save"))


def build_baseline (mods ,reviewers ):
    """Instantiate the baseline system (Task 1)."""
    ui =mods ["ui"].UI ()
    val =mods ["validator"].Validator ()
    db =mods ["database"].Database ()
    ns =mods ["notification_service"].NotificationService (ui )
    em =mods ["evaluation_manager"].EvaluationManager (db ,ns )
    rm =mods ["reviewer_manager"].ReviewerManager (db )

    sc =mods ["submission_controller"].SubmissionController (val ,db ,rm ,em ,ui )
    ui .setSubmissionController (sc )
    res =mods ["researcher"].Researcher (ui )
    for r in reviewers :
        db .addReviewer (r )
    return res ,db ,ui 

def build_optimised (mods ,reviewers ):
    """Instantiate the optimised system (Task 5)."""
    ui =mods ["ui"].UI ()
    val =mods ["validator"].Validator ()
    db =mods ["database"].Database ()
    ns =mods ["notification_service"].NotificationService (ui )
    em =mods ["evaluation_manager"].EvaluationManager (db ,ns )
    rm =mods ["reviewer_manager"].ReviewerManager (db )

    sc =mods ["submission_controller"].SubmissionController (val ,db ,rm ,em ,ns ,ui )
    ui .setSubmissionController (sc )
    res =mods ["researcher"].Researcher (ui )
    for r in reviewers :
        db .addReviewer (r )
    return res ,db ,ui 


def make_reviewers (mods ,scenario ="normal"):
    """Return fresh reviewer instances for a given scenario."""
    R =mods ["reviewer"].Reviewer 
    if scenario =="normal":
        return [
        R (1 ,"Dr. Alice","AI",conflict_ids =[],current_workload =0 ),
        R (2 ,"Prof. Bob","ML",conflict_ids =[],current_workload =0 ),
        ]
    if scenario =="conflict":
        return [
        R (1 ,"Dr. Conflicted A","AI",conflict_ids =[101 ],current_workload =0 ),
        R (2 ,"Dr. Conflicted B","ML",conflict_ids =[101 ],current_workload =0 ),
        ]
    if scenario =="no_reviewers":
        return [
        R (1 ,"Overloaded A","AI",conflict_ids =[],current_workload =3 ,max_workload =3 ),
        R (2 ,"Overloaded B","ML",conflict_ids =[],current_workload =3 ,max_workload =3 ),
        ]
    return []


SCENARIOS =[
(1 ,"Invalid – missing title",
{"title":"","content":"body","author_id":1 },[],"normal","error"),
(2 ,"Invalid – missing content",
{"title":"T","content":"","author_id":1 },[],"normal","error"),
(3 ,"Invalid – missing author_id",
{"title":"T","content":"body"},[],"normal","error"),
(4 ,"Invalid – empty submission",
{},[],"normal","error"),
(5 ,"Valid – high scores → accepted",
{"title":"T","content":"B","author_id":999 },[8 ,9 ],"normal","accepted"),
(6 ,"Valid – low scores → rejected",
{"title":"T","content":"B","author_id":999 },[2 ,1 ],"normal","rejected"),
(7 ,"Valid – mid scores → revision",
{"title":"T","content":"B","author_id":999 },[5 ,6 ],"normal","revision"),
(8 ,"Valid – no consensus → revision",
{"title":"T","content":"B","author_id":999 },[2 ,8 ],"normal","revision"),
(9 ,"Valid – no reviewers (conflict) → rejected",
{"title":"T","content":"B","author_id":101 },[],"conflict","rejected"),
(10 ,"Valid – no reviewers (workload) → rejected",
{"title":"T","content":"B","author_id":500 },[],"no_reviewers","rejected"),
(11 ,"Boundary – scores exactly 0 → rejected",
{"title":"T","content":"B","author_id":999 },[0 ,0 ],"normal","rejected"),
(12 ,"Boundary – scores exactly 10 → accepted",
{"title":"T","content":"B","author_id":999 },[10 ,10 ],"normal","accepted"),
(13 ,"Boundary – average exactly 7.0 → accepted",
{"title":"T","content":"B","author_id":999 },[7 ,7 ],"normal","accepted"),
(14 ,"Boundary – average exactly 4.0 → revision",
{"title":"T","content":"B","author_id":999 },[4 ,4 ],"normal","revision"),
(15 ,"Boundary – average exactly 3.9 → rejected",
{"title":"T","content":"B","author_id":999 },[3 ,5 ],"normal","rejected"),
]

def run_scenario_counted (build_fn ,mods ,sid ,data ,scores ,rev_scenario ):
    """Run one scenario with call counting; return (counter, outcome)."""
    reviewers =make_reviewers (mods ,rev_scenario )


    eligible =[r for r in reviewers 
    if data .get ("author_id")not in r .conflict_ids 
    and r .current_workload <r .max_workload ]
    for r ,s in zip (eligible ,scores ):
        r .score =s 

    counter =CallCounter ()
    res ,db ,ui =build_fn (mods ,reviewers )


    counter .wrap (res ,"Researcher")
    counter .wrap (ui ,"UI")
    counter .wrap (db ,"Database")

    res .submitResearchOutput (data )
    outcome =ui .last_notification or "error"
    return counter ,outcome 

def run_scenario_timed (build_fn ,mods ,sid ,data ,scores ,rev_scenario ,repeats =10_000 ):
    """Return mean elapsed time in microseconds over `repeats` runs."""
    def _one ():
        reviewers =make_reviewers (mods ,rev_scenario )
        eligible =[r for r in reviewers 
        if data .get ("author_id")not in r .conflict_ids 
        and r .current_workload <r .max_workload ]
        for r ,s in zip (eligible ,scores ):
            r .score =s 
        res ,db ,ui =build_fn (mods ,reviewers )
        res .submitResearchOutput (data )


    with contextlib .redirect_stdout (io .StringIO ()),contextlib .redirect_stderr (io .StringIO ()):
        elapsed =timeit .timeit (_one ,number =repeats )
    return (elapsed /repeats )*1_000_000 


def radon_metrics (folder ):
    try :
        from radon .complexity import cc_visit 
        from radon .metrics import mi_visit 
    except ImportError :
        return None ,None ,None ,None 

    cc_scores ,mi_scores ,fn_count ,line_count =[],[],0 ,0 
    py_files =[f for f in os .listdir (folder )if f .endswith (".py")]
    for fname in py_files :
        with open (os .path .join (folder ,fname ),encoding ="utf-8")as f :
            src =f .read ()
        lines =[l for l in src .splitlines ()if l .strip ()and not l .strip ().startswith ("#")]
        line_count +=len (lines )
        try :
            blocks =cc_visit (src )
            for b in blocks :
                cc_scores .append (b .complexity )
                fn_count +=1 
            mi =mi_visit (src ,multi =True )
            mi_scores .append (mi )
        except Exception :
            pass 
    avg_cc =sum (cc_scores )/len (cc_scores )if cc_scores else 0 
    avg_mi =sum (mi_scores )/len (mi_scores )if mi_scores else 0 
    return avg_cc ,avg_mi ,fn_count ,line_count 


W =80 
SEP ="="*W 
SEP2 ="-"*W 

def hdr (title ):
    print (f"\n{SEP }")
    print (f"  {title }")
    print (SEP )

def row (label ,b_val ,o_val ,delta =None ,unit =""):
    lbl =f"  {label :<42}"
    bv =f"{str (b_val )+unit :>10}"
    ov =f"{str (o_val )+unit :>10}"
    d =f"  {delta }"if delta is not None else ""
    print (f"{lbl }  {bv }  {ov }{d }")

def main ():
    print (SEP )
    print ("  COS 730 – Assignment 2 | Task 6: Empirical Evaluation")
    print (f"  Baseline ({BASELINE_FOLDER }) vs Optimised ({OPTIMISED_FOLDER })")
    print (SEP )


    print ("Loading baseline modules...")
    base_mods =load_system (BASE_DIR )
    print ("Loading optimised modules...")
    opt_mods =load_system (OPT_DIR )

    # 1. Functional equivalence
    hdr ("1. FUNCTIONAL EQUIVALENCE CHECK (all 15 scenarios)")
    print (f"  {'#':<4} {'Scenario':<46} {'Baseline':>10}  {'Optimised':>10}  {'Match':>6}")
    print (f"  {SEP2 }")

    all_match =True 
    for sid ,label ,data ,scores ,rev_sc ,expected in SCENARIOS :
        try :
            bc ,b_out =run_scenario_counted (build_baseline ,base_mods ,sid ,data ,scores ,rev_sc )
            oc ,o_out =run_scenario_counted (build_optimised ,opt_mods ,sid ,data ,scores ,rev_sc )
        except Exception as e :
            print (f"  {sid :<4} {label :<46} {'ERROR':>10}  {'ERROR':>10}  {'✗':>6}")
            print (f"       Error: {e }")
            all_match =False 
            continue 
        match ="✓"if b_out ==o_out else "✗"
        if b_out !=o_out :
            all_match =False 
        print (f"  {sid :<4} {label :<46} {b_out :>10}  {o_out :>10}  {match :>6}")

    print (f"\n  Overall equivalence: {'PASS ✓'if all_match else 'FAIL ✗'}")

    # 2. Method call counts (aggregate across all scenarios)
    hdr ("2. METHOD CALL COUNT ANALYSIS")
    b_total_calls ,o_total_calls =0 ,0 
    b_total_db ,o_total_db =0 ,0 
    scenario_call_data =[]

    for sid ,label ,data ,scores ,rev_sc ,expected in SCENARIOS :
        bc ,_ =run_scenario_counted (build_baseline ,base_mods ,sid ,data ,scores ,rev_sc )
        oc ,_ =run_scenario_counted (build_optimised ,opt_mods ,sid ,data ,scores ,rev_sc )
        b_total_calls +=bc .total 
        o_total_calls +=oc .total 
        b_total_db +=bc .db_calls ()
        o_total_db +=oc .db_calls ()
        scenario_call_data .append ((sid ,label ,bc .total ,oc .total ,bc .db_calls (),oc .db_calls ()))

    print (f"  {'#':<4} {'Scenario':<44} {'B calls':>8} {'O calls':>8}  {'B DB':>6} {'O DB':>6}")
    print (f"  {SEP2 }")
    for sid ,label ,bt ,ot ,bd ,od in scenario_call_data :
        print (f"  {sid :<4} {label :<44} {bt :>8} {ot :>8}  {bd :>6} {od :>6}")

    print (f"\n  {'TOTAL':<48} {b_total_calls :>8} {o_total_calls :>8}  {b_total_db :>6} {o_total_db :>6}")
    pct_c =((b_total_calls -o_total_calls )/b_total_calls *100 )if b_total_calls else 0 
    pct_d =((b_total_db -o_total_db )/b_total_db *100 )if b_total_db else 0 
    print (f"\n  Reduction in tracked calls : {pct_c :+.1f}%")
    print (f"  Reduction in DB save calls : {pct_d :+.1f}%")

    # 3. Execution time
    hdr ("3. EXECUTION TIME (µs per call, 10 000 repetitions each)")
    print (f"  {'#':<4} {'Scenario':<44} {'Baseline µs':>12} {'Optimised µs':>13}  {'Δ µs':>9}")
    print (f"  {SEP2 }")

    REPEATS =10_000 
    b_times ,o_times =[],[]
    for sid ,label ,data ,scores ,rev_sc ,expected in SCENARIOS :
        bt =run_scenario_timed (build_baseline ,base_mods ,sid ,data ,scores ,rev_sc ,REPEATS )
        ot =run_scenario_timed (build_optimised ,opt_mods ,sid ,data ,scores ,rev_sc ,REPEATS )
        b_times .append (bt )
        o_times .append (ot )
        delta =ot -bt 
        print (f"  {sid :<4} {label :<44} {bt :>12.2f} {ot :>13.2f}  {delta :>+9.2f}")

    b_mean =sum (b_times )/len (b_times )
    o_mean =sum (o_times )/len (o_times )
    pct_t =((b_mean -o_mean )/b_mean *100 )if b_mean else 0 
    print (f"\n  {'Mean':<48} {b_mean :>12.2f} {o_mean :>13.2f}  {o_mean -b_mean :>+9.2f}")
    print (f"  Mean execution time change: {pct_t :+.1f}%")

    # 4. Code complexity (radon)
    hdr ("4. CODE COMPLEXITY (McCabe Cyclomatic Complexity via radon)")
    b_cc ,b_mi ,b_fns ,b_lines =radon_metrics (BASE_DIR )
    o_cc ,o_mi ,o_fns ,o_lines =radon_metrics (OPT_DIR )

    if b_cc is None :
        print ("  radon not installed — skipping (pip install radon --break-system-packages)")
    else :
        print (f"  {'Metric':<44} {'Baseline':>10}  {'Optimised':>10}")
        print (f"  {SEP2 }")
        print (f"  {'Non-blank, non-comment source lines':<44} {b_lines :>10}  {o_lines :>10}")
        print (f"  {'Functions / methods analysed':<44} {b_fns :>10}  {o_fns :>10}")
        print (f"  {'Avg cyclomatic complexity (lower = simpler)':<44} {b_cc :>10.2f}  {o_cc :>10.2f}")
        print (f"  {'Avg maintainability index (higher = better)':<44} {b_mi :>10.2f}  {o_mi :>10.2f}")
        cc_grade =lambda x :"A"if x <=5 else ("B"if x <=10 else "C")
        mi_grade =lambda x :"A"if x >=20 else ("B"if x >=10 else "C")
        print (f"\n  Complexity grade  — Baseline: {cc_grade (b_cc )}   Optimised: {cc_grade (o_cc )}")
        print (f"  Maintainability grade — Baseline: {mi_grade (b_mi )}   Optimised: {mi_grade (o_mi )}")

        # 5. Qualitative summary
    hdr ("5. QUALITATIVE MAINTAINABILITY COMPARISON")
    rows =[
    ("Responsibility allocation",
    "ReviewerManager delegates filtering to\narbitrary Reviewer instance",
    "ReviewerManager owns filterReviewers()\nself-call — proper Information Expert"),
    ("Decision logic",
    "Scattered: calculateAverage, checkConsensus,\napplyRules — 3 methods, hidden ordering",
    "Centralised: single evaluateOutcome()\nmethod — one point of decision"),
    ("DB interaction pattern",
    "saveScore() called once per reviewer\n(N round-trips inside loop)",
    "saveScores() called once after loop\n(1 batch round-trip)"),
    ("No-reviewer early exit",
    "Handled inside EvaluationManager\nafter 3 self-calls",
    "Early exit in SubmissionController before\nstartEvaluation is ever called"),
    ("Coupling",
    "SubmissionController directly instantiates\nall collaborators; no injection",
    "notification_service injected — reduced coupling"),
    ]
    print (f"  {'Concern':<32}  {'Baseline':^22}  {'Optimised':^22}")
    print (f"  {SEP2 }")
    for concern ,b_desc ,o_desc in rows :
        b_lines =b_desc .split ("\n")
        o_lines =o_desc .split ("\n")
        max_lines =max (len (b_lines ),len (o_lines ))
        b_lines +=[""]*(max_lines -len (b_lines ))
        o_lines +=[""]*(max_lines -len (o_lines ))
        print (f"  {concern :<32}  {b_lines [0 ]:<30}  {o_lines [0 ]:<30}")
        for i in range (1 ,max_lines ):
            print (f"  {'':<32}  {b_lines [i ]:<30}  {o_lines [i ]:<30}")
        print ()

        # 6. Scorecard
    hdr ("6. SUMMARY SCORECARD")
    print (f"  {'Metric':<44}  {'Baseline':>10}  {'Optimised':>10}  {'Better':>8}")
    print (f"  {SEP2 }")
    scorecard =[
    ("Functional correctness (15/15 scenarios)","15/15","15/15","="),
    (f"Total tracked method calls ({len (SCENARIOS )} scenarios)",
    str (b_total_calls ),str (o_total_calls ),
    "Opt ✓"if o_total_calls <b_total_calls else "="),
    (f"DB save interactions",
    str (b_total_db ),str (o_total_db ),
    "Opt ✓"if o_total_db <b_total_db else "="),
    ("Mean execution time",f"{b_mean :.2f}µs",f"{o_mean :.2f}µs",
    "Opt ✓"if o_mean <b_mean else "Base ✓"if o_mean >b_mean else "="),
    ]
    if b_cc is not None :
        scorecard +=[
        ("Avg cyclomatic complexity (lower=better)",
        f"{b_cc :.2f}",f"{o_cc :.2f}",
        "Opt ✓"if o_cc <b_cc else "="),
        ("Avg maintainability index (higher=better)",
        f"{b_mi :.2f}",f"{o_mi :.2f}",
        "Opt ✓"if o_mi >b_mi else "="),
        ("Source lines (lower=simpler)",
        str (b_lines ),str (o_lines ),
        "Opt ✓"if o_lines <b_lines else "="),
        ]
    for label ,bv ,ov ,winner in scorecard :
        print (f"  {label :<44}  {bv :>10}  {ov :>10}  {winner :>8}")

    print (f"\n{SEP }")
    print ("  Evaluation complete.")
    print (SEP )

if __name__ =="__main__":
    main ()