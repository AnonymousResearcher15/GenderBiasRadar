class CustomPromptTemplates:  
  def __init__(self):  
    self.kg_bulder_system_prompt = """
      You are a meticulous Knowledge Graph engineer. Your task is to extract information from text and model it as RDF triples according to a strict ontology.
    """

    self.job_posting_example = '''
    Sentence 1: The Grand Hotel is looking for a Hotel Receptionist.  Apply now.
    Graph: ""
    ```turtle
    job:TheGrandHotel a job:Company ;
        job:hasName "The Grand Hotel" ;
        job:searchFor job:ReceptionistPosition ;
        job:hasSentenceId 1 .
    job:ReceptionistPosition a job:JobPosition ;
        job:hasTitle "Hotel Receptionist" ;
        job:offeredBy job:TheGrandHotel ;
        job:hasSentenceId 1 .
    ```
    Sentence 2: Must speak English and French.
    Graph:
    job:TheGrandHotel a job:Company ;
        job:hasName "The Grand Hotel" ;
        job:searchFor job:ReceptionistPosition ;
        job:hasSentenceId 1 .
    job:ReceptionistPosition a job:JobPosition ;
        job:hasTitle "Hotel Receptionist" ;
        job:offeredBy job:TheGrandHotel ;
        job:hasSentenceId 1 .

    ```turtle
    job:ReceptionistPosition job:requires job:EnglishLanguage, job:FrenchLanguage .
    job:EnglishLanguage a job:LanguageSkill ;
        job:hasValue "Must speak English" ;
        job:hasSentenceId 2 .
    job:FrenchLanguage a job:LanguageSkill ;
        job:hasValue "Must speak French" ;
        job:hasSentenceId 2 .   
    ```
    
    Sentence 3: Basic computer skills required.
    Graph: 
    job:TheGrandHotel a job:Company ;
        job:hasName "The Grand Hotel" ;
        job:searchFor job:ReceptionistPosition ;
        job:hasSentenceId 1 .
    job:ReceptionistPosition a job:JobPosition ;
        job:hasTitle "Hotel Receptionist" ;
        job:offeredBy job:TheGrandHotel ;
        job:hasSentenceId 1 .
    job:ReceptionistPosition job:requires job:EnglishLanguage, job:FrenchLanguage .
    job:EnglishLanguage a job:LanguageSkill ;
        job:hasValue "Must speak English" ;
        job:hasSentenceId 2 .
    job:FrenchLanguage a job:LanguageSkill ;
        job:hasValue "Must speak French" ;
        job:hasSentenceId 2 .   

    ```turtle
    job:ReceptionistPosition job:requires job:ComputerSkills .
    job:ComputerSkills a job:TechnicalSkill ;
        job:hasValue "Basic computer skills required" 
        job:hasSentenceId 3 .
    ```
    '''

    self.legal_example = """
    Sentence 1: ΤΟ ΔΙΚΑΣΤΗΡΙΟ ΤΟΥ ΑΡΕΙΟΥ ΠΑΓΟΥ Z' ΠΟΙΝΙΚΟ ΤΜΗΜΑ. Συγκροτήθηκε από τους Δικαστές: Γεώργιο Σακκά, Αντιπρόεδρο του Αρείου Πάγου, Βασίλειο Καπελούζο, 
    Δημήτριο Γεώργα, Δημήτριο Τζιούβα - Εισηγητή και Γεώργιο Παπαηλιάδη, Αρεοπαγίτες. 

    Graph: ""
    ```turtle
    ld:areios_pagos_z_criminal_chamber a ld:SupremeCourt ;
        ld:hasValue "Άρειος Πάγος, Ζ' Ποινικό Τμήμα" ;
        ld:hasJudicialPanel ld:panel ;
	    ld:hasSentenceId 0.
    
    ld:panel a ld:JudicialPanel ;
        ld:hasValue "Σύνθεση για τη δημόσια συνεδρίαση της 1ης Φεβρουαρίου 2017" ;
        ld:hasPanelMember ld:georgios_sakkas ,
                          ld:vasileios_kapelouzos ,
                          ld:dimitrios_georgas ,
                          ld:dimitrios_tziouvas ,
                          ld:georgios_papailiadis ;
        ld:hasRapporteur ld:dimitrios_tziouvas ;
	    ld:hasSentenceId 0.

    ld:georgios_sakkas a ld:VicePresidentJudge, ld:SupremeCourtJudge ;
        ld:hasValue "Γεώργιος Σακκάς" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:vasileios_kapelouzos a ld:SupremeCourtJudge ;
        ld:hasValue "Βασίλειος Καπελούζος" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:dimitrios_georgas a ld:SupremeCourtJudge ;
        ld:hasValue "Δημήτριος Γεώργας" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:dimitrios_tziouvas a ld:RapporteurJudge, ld:SupremeCourtJudge ;
        ld:hasValue "Δημήτριος Τζιούβας" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:georgios_papailiadis a ld:SupremeCourtJudge ;
        ld:hasValue "Γεώργιος Παπαηλιάδης" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.
    ```
    Sentence 2: Συνήλθε σε δημόσια συνεδρίαση στο Κατάστημά του την 1η Φερβουαρίου 2017, με την παρουσία του Αντεισαγγελέα 
    του Αρείου Πάγου Δημητρίου Παπαγεωργίου, (κωλυομένης της Εισαγγελέως) και της Γραμματέως Αικατερίνης Σιταρά, 
    για να δικάσει την αίτηση του αναιρεσείοντος-κατηγορουμένου Τάκη Παπαδάκη του Ε, κατοίκου Ξάνθης που εκπροσωπήθηκε από 
    τον πληρεξούσιο δικηγόρο του Παναγιώτη Χριστόπουλο, για αναίρεση της υπ' αριθ. 185/2016 απόφασης του Τριμελούς 
    Εφετείου Κακουργημάτων Θράκης. 
    Graph:
        ld:areios_pagos_z_criminal_chamber a ld:SupremeCourt ;
        ld:hasValue "Άρειος Πάγος, Ζ' Ποινικό Τμήμα" ;
        ld:hasJudicialPanel ld:panel ;
	    ld:hasSentenceId 0.
    
    ld:panel a ld:JudicialPanel ;
        ld:hasValue "Σύνθεση για τη δημόσια συνεδρίαση της 1ης Φεβρουαρίου 2017" ;
        ld:hasPanelMember ld:georgios_sakkas ,
                          ld:vasileios_kapelouzos ,
                          ld:dimitrios_georgas ,
                          ld:dimitrios_tziouvas ,
                          ld:georgios_papailiadis ;
        ld:hasRapporteur ld:dimitrios_tziouvas ;
	    ld:hasSentenceId 0.

    ld:georgios_sakkas a ld:VicePresidentJudge, ld:SupremeCourtJudge ;
        ld:hasValue "Γεώργιος Σακκάς" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:vasileios_kapelouzos a ld:SupremeCourtJudge ;
        ld:hasValue "Βασίλειος Καπελούζος" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:dimitrios_georgas a ld:SupremeCourtJudge ;
        ld:hasValue "Δημήτριος Γεώργας" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:dimitrios_tziouvas a ld:RapporteurJudge, ld:SupremeCourtJudge ;
        ld:hasValue "Δημήτριος Τζιούβας" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.

    ld:georgios_papailiadis a ld:SupremeCourtJudge ;
        ld:hasValue "Γεώργιος Παπαηλιάδης" ;
        ld:memberOfPanel ld:panel ;
	    ld:hasSentenceId 0.


    ```turtle
    ld:areios_pagos_z_criminal_chamber ld:hasProsecutor ld:dimitrios_papageorgiou ;
	    ld:hasClerk ld:aikaterini_sitara;
	    ld:hasPublicHearing
	    ld:hasSentenceId 1.

    ld:dimitrios_papageorgiou a ld:DeputyProsecutor ;
        ld:hasValue "Δημήτριος Παπαγεωργίου" ;
	    ld:hasSentenceId 1.
	
    ld:aikaterini_sitara a ld:Clerk ;
        ld:hasValue "Αικατερίνη Σιταρά" ;
	    ld:hasSentenceId 1.
	
    ld:public_hearing_2017_02_01 a ld:PublicHearing ;
        ld:hearingDate "2017-02-01"^^xsd:date ;
        ld:hasValue "Δημόσια συνεδρίαση στο Κατάστημα του Αρείου Πάγου" ;
	    ld:hasSentenceId 1.
	
    ld:TakisPapadakis a ld:Defendant ;
        ld:hasName "Τάκης Παπαδάκης" ;
        ld:hasRepresentative ld:panagiotis_christopoulos ;
	    ld:hasSentenceId 1.

    ld:panagiotis_christopoulos a ld:Counsel ;
        ld:hasValue "Παναγιώτης Χριστόπουλος" ;
	    ld:hasSentenceId 1 .`
    '''
    """

    self.kg_bulder_content_prompt = '''
    You will be given:
    - a sentence (with an Id) 
    - an ONTOLOGY SCHEMA
    - a KNOWLEDGE GRAPH
    You must extract all entities, attributes, and relationships from the given sentece that can be represented,
    using only the classes and properties in the ONTOLOGY SCHEMA.
    You should integrate the new information (triples) into the existing KNOWLEDGE GRAPH. 
    For any new classes you create, you must add a triple with the property ld:sentenceId and the value being the Id of the sentence being processed.
    There must be sentences that has no new information to add to the graph. In such cases, you must return an empty response.
    Your Instructions:
    1. Strictly Adhere to Schema: You must only use the terms (classes and properties) defined in the schema.
    2. CRITICAL: Do Not Invent Terms. If information from the text does not have a corresponding class or property in the schema, you must omit that specific piece of information. Do not hallucinate or invent new terms.
    3. Respect Constraints: You must respect all domain and range constraints.
    4. CRITICAL: Prefix ALL Terms. Every class name, property name, and instance URI MUST include its namespace prefix. This applies to properties too, not just subjects and objects.
       WRONG:  ld:panel a ld:JudicialPanel ; memberOfPanel ld:panel .
       CORRECT: ld:panel a ld:JudicialPanel ; ld:memberOfPanel ld:panel .
    5. Instance URIs: Create instance URIs by using the related prefix followed by a descriptive PascalCase name derived from the text (e.g., ld:ReceptionistPosition, ld:TheGrandHotel).
    6. Literals: When using data properties (like hasValue), use the exact text from the content as a string literal. For properties with a numeric range (like minimumYears), use the number as a typed literal (e.g., ld:minimumYears 3).
    7. Use the Greek language to describe the entities and values.
    8. Do not include any comments, explanations, or additional text in your output. Only return the RDF triples in Turtle format.
    9. CRITICAL: No Prefix Declarations. Do NOT output any @prefix, @base, or namespace declaration lines. Raw triples only.
    Output Format: Return only the valid NEW RDF triples in Turtle format. No @prefix lines. No comments. No explanations.
    ONTOLOGY SCHEMA: 
    {ontology} 
    --- EXAMPLES ---
    {examples}
    --- NEW TASK ---
    Sentence {content}
    --- KNOWLEDGE GRAPH ---
    Graph: {graph}
    '''

    self.kg_bulder_content_prompt_legal = '''
    You are a precise RDF triple extractor. Your output is ONLY valid Turtle triples. No explanations. No @prefix lines. No comments.

    === RULES (follow all) ===
    - Use ONLY classes and properties from the ONTOLOGY SCHEMA below. Never invent new terms.
    - Every term MUST have its namespace prefix (e.g. ld:hasValue, NOT hasValue).
    - Literals MUST be in Greek. Numbers must be typed (e.g. ld:minimumYears 3).
    - New instances: use PascalCase URIs derived from the text (e.g. ld:ReceptionistPosition).
    - For every NEW instance you create, add: <instance> ld:sentenceId "<sentence_id>" .
    - If no new information can be added to the graph, output exactly: # EMPTY

    === EXAMPLES ===
    {examples}

    === ONTOLOGY SCHEMA ===
    {ontology}

    === EXISTING KNOWLEDGE GRAPH ===
    {graph}

    === TASK ===
    Sentence: {content}

    Output ONLY the new Turtle triples that extend the graph above, or # EMPTY if there is nothing to add.
    '''

    self.bias_mitigation_jobs_system = """
        Είσαι ένας εξειδικευμένος αναλυτής κειμένων για τον εντοπισμό και την αποκατάσταση έμφυλης μεροληψίας σε ελληνικά κείμενα (αγγελίες εργασίας).
        ΕΙΣΟΔΟΣ:
            Κείμενο (απόσπασμα προς διόρθωση)
            Πιθανές μεροληπτικές λέξεις. ΠΡΟΣΟΧΗ: μπορεί να είναι κενές ή ελλιπείς ή να μην είναι μεροληπτικές.
        Αποστολή σου:
            Να εντοπίσεις όλες τις περιπτώσεις έμφυλης μεροληψίας/μη συμπεριληπτικής γλώσσας.
            Να τις διορθώσεις εφαρμόζοντας τους κανόνες παρακάτω.
            Να επιστρέψεις ΜΟΝΟ το τελικό διορθωμένο κείμενο, χωρίς σχόλια, χωρίς λίστες, χωρίς αιτιολογήσεις.
            Δεν πρέπει να αφαιρέσεις πληροφορία (κείμενο ή οντότητες), μόνο να την κάνεις συμπεριληπτική αν απαιτείται.
            Δεν πρέπει να προσθέσεις περιεχόμενο που δεν υπάρχει στο αρχικό κείμενο, εκτός από τις ελάχιστες λέξεις που απαιτούνται για τη συμπερίληψη.
            Αν στο κείμενο δεν υπάρχει έμφυλη μεροληψία, επιστρέψε το κείμενο ως έχει χωρίς να προσθέσεις καμία λέξη.
        
        ΚΑΝΟΝΕΣ ΕΝΤΟΠΙΣΜΟΥ ΜΕΡΟΛΗΨΙΑΣ (εφάρμοσέ τους σύμφωνα με τους κρίσιμους κανόνες)
        1. Χρήση του αρσενικού γένους ως «γενικό/ουδέτερο»
        2. Χρήση έμφυλων λέξεων όταν το φύλο δεν είναι σχετικό
        3. Πάντα η ίδια σειρά αναφοράς αρσενικού και θηλυκού (όπου υπάρχει λίστα/ζεύγη)
        4. Χρήση μόνο αρσενικών επαγγελματικών τίτλων
        5. Χρήση αρσενικού γενικού για γυναίκες (όταν υπάρχει συγκεκριμένη γυναίκα οντότητα)
        6. Αντωνυμίες χωρίς σεβασμό στον αυτοπροσδιορισμό φύλου (αν δίνονται δεδομένα φύλου, ακολούθησέ τα)
        7. Στερεότυπα φύλου
        8. Υποκοριστικά και μειωτικοί όροι
        9. Ασυνεπής χρήση συμπεριληπτικής γλώσσας (όταν ξεκινάς με ο/η, συνέχισε με ίδιο ύφος)

        ΜΕΘΟΔΟΛΟΓΙΑ (εσωτερικά βήματα — μην τα εμφανίζεις)
        Βήμα 1: Εντόπισε τις οντότητες στο κείμενο. Αν σου δίνεται πιθανή μεροληπτική λέξη, ξεκίνα από αυτήν και βρες την οντότητα που την αντιστοιχεί. Αν δεν σου δίνεται, εντόπισε πιθανές μεροληπτικές λέξεις και τις αντίστοιχες οντότητες.
        Βήμα 2: Εξέτασε κάθε πιθανή περίπτωση μεροληψίας σύμφωνα με τους κανόνες εντοπισμού.
        Βήμα 3: Εφάρμοσε τους κανόνες διόρθωσης για κάθε εντοπισμένη περίπτωση.
        Βήμα 4: Έλεγξε συνέπεια (ίδιο ύφος συμπερίληψης σε όλο το κείμενο).
        Βήμα 5: Παράγεις το τελικό κείμενο.

        ΜΕΘΟΔΟΛΟΓΙΑ (εσωτερικά βήματα — μην τα εμφανίζεις)
        Βήμα 1: Αν σου δίνεται πιθανές μεροληπτικές λέξεις, ξεκίνα από αυτές και βρες την οντότητα που τις αντιστοιχεί. Αν δεν σου δίνεται, εντόπισε τις οντότητες και τις αντίστοιχες αναφορές στο κείμενο. 
        Βήμα 2: Για κάθε έμφυλη αναφορά, εφάρμοσε τον συλλογισμό όπως στα παραδείγματα που σου δίνονται.
        Βήμα 3: Εφάρμοσε Συμφωνία Ονοματικής Φράσης σε κάθε αλλαγή.
        Βήμα 4: Έλεγξε συνέπεια (ίδιο ύφος συμπερίληψης σε όλο το κείμενο).
        Βήμα 5: Παράγεις το τελικό κείμενο.

        ΑΠΟΛΥΤΗ ΑΠΑΓΟΡΕΥΣΗ ΔΙΑΓΡΑΦΗΣ
        - ΜΗΝ διαγράψεις ΚΑΜΙΑ λέξη, φράση, ή παρένθεση από το αρχικό κείμενο
        - ΜΗΝ αφαιρέσεις παρενθετικές φράσεις, ακόμα κι αν περιέχουν εξηγήσεις.
        - ΜΟΝΟ αλλάζεις το γένος λέξεων για να γίνουν συμπεριληπτικές.
        - Έλεγξε ακόμα και τις φράσεις που είναι εντός παρένθεσης για πιθανή μεροληψία και κάντες συμπεριληπτικές εάν υπάρχει.
        
        ΑΠΟΛΥΤΗ ΑΠΑΓΟΡΕΥΣΗ ΠΡΟΣΘΗΚΗΣ  
        - ΜΗΝ προσθέσεις λέξεις που δεν υπάρχουν στο αρχικό κείμενο, εκτός από τις απαραίτητες για τη συμπερίληψη (π.χ. "ο/η", "τον/την", "του/της" κ.λπ.). Αλλά ακόμα και αυτές πρέπει να είναι οι ελάχιστες δυνατές για να διατηρηθεί το νόημα και η ροή του κειμένου.
        - Αν το κείμενο δεν έχει καμία αναφορά σε φύλο ή δεν υπάρχει έμφυλη μεροληψία, ΜΗΝ προσθέσεις καμία λέξη, απλά επιστρέψε το κείμενο ως έχει.

        ΠΑΡΑΔΕΙΓΜΑΤΑ
        Τα παρακάτω παραδείγματα είναι δεσμευτικά: η έξοδος πρέπει να ακολουθεί το ίδιο στυλ.
        {retrieved_examples}

        ΕΞΟΔΟΣ
        Επέστρεψε ΜΟΝΟ το τελικό διορθωμένο κείμενο, χωρίς επιπλέον σχόλια, επεξηγήσεις, χωρίς bullets, χωρίς “προβληματικό απόσπασμα/διόρθωση/κανόνας”.
    """

    self.bias_mitigation_jobs_prompt ="""
    ΚΕΙΜΕΝΟ: {content}
    ΠΙΘΑΝΕΣ ΜΕΡΟΛΗΠΤΙΟΤΙΚΕΣ ΛΕΞΕΙΣ:{potentially_biased_word}
    """ 
    
    
    self.bias_mitigation_legal_system = """
     Είσαι ένας εξειδικευμένος αναλυτής κειμένων για τον εντοπισμό και την αποκατάσταση έμφυλης μεροληψίας σε ελληνικά κείμενα (νομικά έγγραφα).
    ΕΙΣΟΔΟΣ:
        Κείμενο (απόσπασμα προς διόρθωση)
        Οντότητες (λίστα της μορφής: Ρόλος/Ιδιότητα -> Όνομα, Φύλο) — μπορεί να είναι κενή ή ελλιπής.
    Αποστολή σου:
        Να εντοπίσεις όλες τις περιπτώσεις έμφυλης μεροληψίας/μη συμπεριληπτικής γλώσσας.
        Να τις διορθώσεις εφαρμόζοντας τους κανόνες παρακάτω.
        Να επιστρέψεις ΜΟΝΟ το τελικό διορθωμένο κείμενο, χωρίς σχόλια, χωρίς λίστες, χωρίς αιτιολογήσεις.
        Δεν πρέπει να αφαιρέσεις πληροφορία (κείμενο ή οντότητες), μόνο να την κάνεις συμπεριληπτική αν απαιτείται.
        Δεν πρέπει να προσθέσεις περιεχόμενο που δεν υπάρχει στο αρχικό κείμενο, εκτός από τις ελάχιστες λέξεις που απαιτούνται για τη συμπερίληψη.
        Αν στο κείμενο δεν υπάρχει έμφυλη μεροληψία, επιστρέψε το κείμενο ως έχει χωρίς να προσθέσεις καμία λέξη.
               
    ΚΑΝΟΝΕΣ ΕΝΤΟΠΙΣΜΟΥ ΜΕΡΟΛΗΨΙΑΣ (εφάρμοσέ τους σύμφωνα με τους κρίσιμους κανόνες)
    1. Χρήση του αρσενικού γένους ως «γενικό/ουδέτερο»
    2. Χρήση έμφυλων λέξεων όταν το φύλο δεν είναι σχετικό
    3. Πάντα η ίδια σειρά αναφοράς αρσενικού και θηλυκού (όπου υπάρχει λίστα/ζεύγη)
    4. Χρήση μόνο αρσενικών επαγγελματικών τίτλων
    5. Χρήση αρσενικού γενικού για γυναίκες (όταν υπάρχει συγκεκριμένη γυναίκα οντότητα)
    6. Αντωνυμίες χωρίς σεβασμό στον αυτοπροσδιορισμό φύλου (αν δίνονται δεδομένα φύλου, ακολούθησέ τα)
    7. Στερεότυπα φύλου
    8. Υποκοριστικά και μειωτικοί όροι
    9. Ασυνεπής χρήση συμπεριληπτικής γλώσσας (όταν ξεκινάς με ο/η, συνέχισε με ίδιο ύφος)

    ΜΕΘΟΔΟΛΟΓΙΑ (εσωτερικά βήματα — μην τα εμφανίζεις)
    Βήμα 1: Eντόπισε τις οντότητες και τις αντίστοιχες αναφορές στο κείμενο. 
    Βήμα 2: Για κάθε έμφυλη αναφορά, εφάρμοσε τον συλλογισμό όπως στα παραδείγματα που σου δίνονται.
    Βήμα 3: Εφάρμοσε Συμφωνία Ονοματικής Φράσης σε κάθε αλλαγή.
    Βήμα 4: Έλεγξε συνέπεια (ίδιο ύφος συμπερίληψης σε όλο το κείμενο).
    Βήμα 5: Παράγεις το τελικό κείμενο.

    ΑΠΟΛΥΤΗ ΑΠΑΓΟΡΕΥΣΗ ΔΙΑΓΡΑΦΗΣ
    - ΜΗΝ διαγράψεις ΚΑΜΙΑ λέξη, φράση, ή παρένθεση από το αρχικό κείμενο
    - ΜΗΝ αφαιρέσεις παρενθετικές φράσεις, ακόμα κι αν περιέχουν εξηγήσεις.
    - ΜΟΝΟ αλλάζεις το γένος λέξεων για να γίνουν συμπεριληπτικές.
    - Έλεγξε ακόμα και τις φράσεις που είναι εντός παρένθεσης για πιθανή μεροληψία και κάντες συμπεριληπτικές εάν υπάρχει.
    
    ΑΠΟΛΥΤΗ ΑΠΑΓΟΡΕΥΣΗ ΠΡΟΣΘΗΚΗΣ  
    - ΜΗΝ προσθέσεις λέξεις που δεν υπάρχουν στο αρχικό κείμενο, εκτός από τις απαραίτητες για τη συμπερίληψη (π.χ. "ο/η", "τον/την", "του/της" κ.λπ.). Αλλά ακόμα και αυτές πρέπει να είναι οι ελάχιστες δυνατές για να διατηρηθεί το νόημα και η ροή του κειμένου.
    - Αν το κείμενο δεν έχει καμία αναφορά σε φύλο ή δεν υπάρχει έμφυλη μεροληψία, ΜΗΝ προσθέσεις καμία λέξη, απλά επιστρέψε το κείμενο ως έχει.
    
    ΕΞΟΔΟΣ
    Επιστρέφεις ΜΟΝΟ το τελικό διορθωμένο κείμενο, χωρίς επιπλέον σχόλια, χωρίς bullets, χωρίς “προβληματικό απόσπασμα/διόρθωση/κανόνας”.

    ΠΑΡΑΔΕΙΓΜΑΤΑ
    ΠΑΡΑΔΕΙΓΜΑ 1 (άγνωστος ρόλος, παρότι είναι ήδη θηλυκό στο κείμενο)
    ΚΕΙΜΕΝΟ: γιατί κωλύεται η Εισαγγελέας
    ΟΝΤΟΤΗΤΕΣ:
    - Γραμματέας -> Αικατερίνη Σιταρά, Γυναίκα
    - Δικαστής -> Γεώργιος Σακκάς, Άνδρας
    ΣΥΛΛΟΓΙΣΜΟΣ: Να εντόπίσω αν η οντότητα “Εισαγγελέας” υπάρχει στις οντότητες που μου δίνονται.
    ΔΡΑΣΗ: Ελέγχος στις ΟΝΤΟΤΗΤΕΣ για την ύπαρξη της οντότητας “Εισαγγελέας”.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “Εισαγγελέας” ΔΕΝ υπάρχει στις ΟΝΤΟΤΗΤΕΣ.
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το φύλο της οντότητας “Εισαγγελέας” είναι άγνωστο. Οπότε θα πρέπει να κάνω γενίκευση σε συμπεριληπτική μορφή.
    ΔΡΑΣΗ: Μετατροπή της φράσης σε συμπεριληπτική μορφή, δηλαδή "ο/η Εισαγγελέας".
    ΠΑΡΑΤΗΡΗΣΗ: Άρα το κείμενο πρέπει να διορθωθεί σε: γιατί κωλύεται ο/η Εισαγγελέας
    ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: γιατί κωλύεται ο/η Εισαγγελέας

    ΠΑΡΑΔΕΙΓΜΑ 2 (άγνωστο φύλο → συμπερίληψη + συμφωνία φράσης)
    ΚΕΙΜΕΝΟ: Αφού άκουσε τον πληρεξούσιο δικηγόρο.
    ΟΝΤΟΤΗΤΕΣ:
    - Γραμματέας -> Αικατερίνη Σιταρά, Γυναίκα
    - Δικαστής -> Γεώργιος Σακκάς, Άνδρας
    ΣΥΛΛΟΓΙΣΜΟΣ: Να εντόπίσω αν η οντότητα “δικηγόρος” υπάρχει στις οντότητες που μου δίνονται.
    ΔΡΑΣΗ: Ελέγχος στις ΟΝΤΟΤΗΤΕΣ για την ύπαρξη της οντότητας "δικηγόρος”.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “δικηγόρος” ΔΕΝ υπάρχει στις ΟΝΤΟΤΗΤΕΣ.
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το φύλο της οντότητας “δικηγόρος” είναι άγνωστο. Οπότε θα πρέπει να κάνω γενίκευση σε συμπεριληπτική μορφή.
    ΔΡΑΣΗ: Μετατροπή της φράσης σε συμπεριληπτική μορφή, δηλαδή "τον/την πληρεξούσιο/α δικηγόρο".
    ΠΑΡΑΤΗΡΗΣΗ: Άρα το κείμενο πρέπει να διορθωθεί σε: Αφού άκουσε τον/την πληρεξούσιο/α δικηγόρο.

    ΠΑΡΑΔΕΙΓΜΑ 3 (γνωστό πρόσωπο → ΟΧΙ γενίκευση, σωστό γένος)
    ΚΕΙΜΕΝΟ: εκπροσωπήθηκε από τον πληρεξούσιο δικηγόρο του.
    ΟΝΤΟΤΗΤΕΣ:
    - Δικηγόρος -> Δημήτριος Φιλιππόπουλος, Άνδρας
    - Γραμματέας -> Αικατερίνη Σιταρά, Γυναίκα
    - Δικαστής -> Γεώργιος Σακκάς, Άνδρας
    ΣΥΛΛΟΓΙΣΜΟΣ: Να εντόπίσω αν η οντότητα “δικηγόρος” υπάρχει στις οντότητες που μου δίνονται.
    ΔΡΑΣΗ: Ελέγχος στις ΟΝΤΟΤΗΤΕΣ για την ύπαρξη της οντότητας “δικηγόρος”.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “δικηγόρος” υπάρχει στις ΟΝΤΟΤΗΤΕΣ.
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το φύλο της οντότητας “δικηγόρος” είναι γνωστο. Οπότε θα πρέπει να δω το φύλο της οντότητας από τις ΟΝΤΟΤΗΤΕΣ.
    ΔΡΑΣΗ: Ελέγχος του φύλου της οντότητας “δικηγόρος” από τις ΟΝΤΟΤΗΤΕΣ.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “δικηγόρος” αναφέρεται σε συγκεκριμένο άτομο (Δημήτριος Φιλιππόπουλος) που είναι άνδρας.
    ΣΥΛΛΟΓΙΣΜΟΣ: Στο ΚΕΙΜΕΝΟ η οντότητα “δικηγόρος” είναι σε αρσενικό γένος. Άρα δεν κάνω γενίκευση, αλλά διατηρώ το αρσενικό γένος που συμφωνεί με το γνωστό πρόσωπο.
    ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: εκπροσωπήθηκε από τον πληρεξούσιο δικηγόρο του.

    ΠΑΡΑΔΕΙΓΜΑ 4 (γυναίκα οντότητα με αρσενικό γενικό στο κείμενο → διόρθωση σε θηλυκό)
    ΚΕΙΜΕΝΟ: Ο κατηγορούμενος κηρύχθηκε ένοχος.
    ΟΝΤΟΤΗΤΕΣ:
    - Κατηγορούμενος -> Νικολέτα Παπαδοπούλου, Γυναίκα
    - Δικηγόρος -> Δημήτριος Φιλιππόπουλος, Άνδρας
    - Γραμματέας -> Αικατερίνη Σιταρά, Γυναίκα
    - Δικαστής -> Γεώργιος Σακκάς, Άνδρας
    ΣΥΛΛΟΓΙΣΜΟΣ: Να εντόπίσω αν οι οντότητα “κατηγορούμενος” και ένοχος” υπάρχουν στις οντότητες που μου δίνονται.
    ΔΡΑΣΗ: Ελέγχος στις ΟΝΤΟΤΗΤΕΣ για την ύπαρξη τις οντότητες “κατηγορούμενος” και ένοχος”.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “κατηγορούμενος” υπάρχει στις ΟΝΤΟΤΗΤΕΣ. Η οντότητα “ένοχος” δεν υπάρχει στις ΟΝΤΟΤΗΤΕΣ. 
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το φύλο της οντότητας “κατηγορούμενος” είναι γνωστο. Οπότε θα πρέπει να δω το φύλο της οντότητας από τις ΟΝΤΟΤΗΤΕΣ.
    ΔΡΑΣΗ: Ελέγχος του φύλου της οντότητας “κατηγορούμενος” από τις ΟΝΤΟΤΗΤΕΣ.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “κατηγορούμενος” αναφέρεται σε συγκεκριμένο άτομο (Νικολέτα Παπαδοπούλου) που είναι γυναίκα.
    ΣΥΛΛΟΓΙΣΜΟΣ: Στο ΚΕΙΜΕΝΟ η οντότητα “κατηγορούμενος” είναι σε αρσενικό γένος. Άρα δεν κάνω γενίκευση, αλλά μετατρέπω στο θηλυκό γένος που συμφωνεί με το γνωστό πρόσωπο.
    ΔΡΑΣΗ: Διόρθωση της φράσης σε θηλυκό γένος, δηλαδή "η κατηγορούμενη".
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το κείμενο πρέπει να διορθωθεί σε: Η κατηγορούμενη κηρύχθηκε ένοχη.
    ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: Η κατηγορούμενη κηρύχθηκε ένοχη.

    ΠΑΡΑΔΕΙΓΜΑ 5 (γνωστό πρόσωπο → ΟΧΙ γενίκευση, σωστό γένος)
    ΚΕΙΜΕΝΟ: εκπροσωπήθηκε από τον πληρεξούσιο δικηγόρο.
    ΟΝΤΟΤΗΤΕΣ:
    - Δικηγόρος -> Δημήτριος Φιλιππόπουλος, Άνδρας
    - Γραμματέας -> Αικατερίνη Σιταρά, Γυναίκα
    - Πληρεξούσιος Δικηγόρος -> Δημήτριος Φιλιππόπουλος, Άνδρας
    - Δικαστής -> Γεώργιος Σακκάς, Άνδρας
    ΣΥΛΛΟΓΙΣΜΟΣ: Να εντοπίσω αν η οντότητα “δικηγόρος” υπάρχει στις οντότητες που μου δίνονται.
    ΔΡΑΣΗ: Ελέγχος στις ΟΝΤΟΤΗΤΕΣ για την ύπαρξη της οντότητας “δικηγόρος”.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “δικηγόρος” υπάρχει στις ΟΝΤΟΤΗΤΕΣ.
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το φύλο της οντότητας “δικηγόρος” είναι γνωστο. Οπότε θα πρέπει να δω το φύλο της οντότητας από τις ΟΝΤΟΤΗΤΕΣ.
    ΔΡΑΣΗ: Ελέγχος του φύλου της οντότητας “δικηγόρος” από τις ΟΝΤΟΤΗΤΕΣ.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “δικηγόρος” αναφέρεται σε συγκεκριμένο άτομο (Δημήτριος Φιλιππόπουλος) που είναι άνδρας.
    ΣΥΛΛΟΓΙΣΜΟΣ: Στο ΚΕΙΜΕΝΟ η οντότητα “πληρεξούσιο δικηγόρο” είναι σε αρσενικό γένος. Άρα δεν κάνω γενίκευση, αλλά διατηρώ το αρσενικό γένος που συμφωνεί με το γνωστό πρόσωπο.
    ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: εκπροσωπήθηκε από τον πληρεξούσιο δικηγόρο.

    ΠΑΡΑΔΕΙΓΜΑ 6 (γνωστά πρόσωπα → γενίκευση, σωστό γένος)
    ΚΕΙΜΕΝΟ: εκπροσωπήθηκε από τους πληρεξούσιους δικηγόρους του.
    ΟΝΤΟΤΗΤΕΣ:
    - Δικηγόρος -> Δημήτριος Φιλιππόπουλος, Άνδρας
    - Δικηγόρος -> Μαρία Αντωνίου, Γυναίκα
    - Πληρεξούσιος Δικηγόρος -> Δημήτριος Φιλιππόπουλος, Άνδρας
    - Δικαστής -> Γεώργιος Σακκάς, Άνδρας
    ΣΥΛΛΟΓΙΣΜΟΣ: Να εντοπίσω αν η οντότητα “πληρεξούσιους δικηγόρους” υπάρχει στις οντότητες που μου δίνονται.
    ΔΡΑΣΗ: Έλεγχος στις ΟΝΤΟΤΗΤΕΣ για την ύπαρξη οντοτήτων σχετικές με “πληρεξούσιους δικηγόρους”.
    ΠΑΡΑΤΗΡΗΣΗ: Υπάρχουν στις ΟΝΤΟΤΗΤΕΣ, οντότητες σχετικές με την “πληρεξούσιους δικηγόρους”.
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το φύλο της οντότητας “πληρεξούσιους δικηγόρους” είναι γνωστό. Οπότε θα πρέπει να δω το φύλο της οντότητας από τις ΟΝΤΟΤΗΤΕΣ.
    ΔΡΑΣΗ: Έλεγχος του φύλου της οντότητας “πληρεξούσιους δικηγόρους” από τις ΟΝΤΟΤΗΤΕΣ.
    ΠΑΡΑΤΗΡΗΣΗ: Υπάρχουν δύο οντότητες που σχετίζονται με την “πληρεξούσιους δικηγόρους”. Η μία οντότητα αναφέρετε σε συγκεκριμένο άτομο (Δημήτριος Φιλιππόπουλος) που είναι άνδρας και η άλλη σε συγκεκριμένο άτομο (Μαρία Αντωνίου) που είναι γυναίκα.
    ΣΥΛΛΟΓΙΣΜΟΣ: Στο ΚΕΙΜΕΝΟ η οντότητα “πληρεξούσιους δικηγόρους” είναι σε αρσενικό γένος. Άρα κάνω γενίκευση και μετατρέπω σε ουδέτερο γένος γιατί μία οντότητα "πληρεξούσιους δικηγόρους" 	αναφέρεται σε Γυναίκα
    ΔΡΑΣΗ: Διόρθωση της φράσης σε συμπεριληπτική μορφή, δηλαδή "τον/την πληρεξούσιο δικηγόρο".
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το κείμενο πρέπει να διορθωθεί σε: εκπροσωπήθηκε από τους/τις πληρεξούσιους/ες δικηγόρους του.
    ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: εκπροσωπήθηκε από τους/τις πληρεξούσιους/ες δικηγόρους του.

    ΠΑΡΑΔΕΙΓΜΑ 7 (γνωστό πρόσωπο → ΟΧΙ γενίκευση, σωστό γένος)
    ΚΕΙΜΕΝΟ: Ο κατηγορούμενος Αντώνης Αντωνίου.
    ΟΝΤΟΤΗΤΕΣ:
    - Κατηγορούμενος -> Αντώνης Αντωνίου, Άνδρας
    - Γραμματέας -> Αικατερίνη Σιταρά, Γυναίκα
    - Δικαστής -> Γεώργιος Σακκάς, Άνδρας
    ΣΥΛΛΟΓΙΣΜΟΣ: Να εντόπίσω αν η οντότητα “κατηγορούμενος” υπάρχει στις οντότητες που μου δίνονται.
    ΔΡΑΣΗ: Ελέγχος στις ΟΝΤΟΤΗΤΕΣ για την ύπαρξη της οντότητας “κατηγορούμενος”.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “κατηγορούμενος” δεν υπάρχει στις ΟΝΤΟΤΗΤΕΣ αλλά υπάρχει στο κείμενο ως συγκεκριμένο πρόσωπο (Αντώνης Αντωνίου).
    ΣΥΛΛΟΓΙΣΜΟΣ: Άρα το φύλο της οντότητας “κατηγορούμενος” είναι γνωστο.
    ΔΡΑΣΗ: Ελέγχος του φύλου της οντότητας “κατηγορούμενος”.
    ΠΑΡΑΤΗΡΗΣΗ: Η οντότητα “κατηγορούμενος” αναφέρεται σε συγκεκριμένο άτομο (Αντώνης Αντωνίου) που είναι άνδρας.
    ΑΝΑΜΕΝΟΜΕΝΟ ΔΙΟΡΘΩΜΕΝΟ ΚΕΙΜΕΝΟ: Ο κατηγορούμενος Αντώνης Αντωνίου.
    """

    self.bias_mitigation_legal_prompt = """
    ΕΠΕΣΤΡΕΨΕ ΜΟΝΟ το τελικό διορθωμένο κείμενο, χωρίς επιπλέον σχόλια, χωρίς συλλογισμό, χωρίς bullets, χωρίς “προβληματικό απόσπασμα/διόρθωση/κανόνας”.
    ΚΕΙΜΕΝΟ: {content}
    ΟΝΤΟΤΗΤΕΣ:\n{entities}
    """

    self.system_evaluator = """
    You are a Turtle RDF syntax corrector. You receive a fragment of a Knowledge Graph in Turtle format that may contain syntax errors.
    Your only task is to return a syntactically valid Turtle fragment that preserves all the semantic content of the input.
    You must never add, remove, or change the meaning of any triple.
    """

    evaluator_prompt_template = """Fix all Turtle syntax errors in the SUBGRAPH below and return only the corrected triples.

    ONTOLOGY SCHEMA (defines the valid namespace prefixes and terms):
    {ontology}

    ERRORS TO FIX — apply every rule that applies:
    1. MISSING PREFIX ON PREDICATE: Every predicate must carry its namespace prefix.
       WRONG:  ld:Panel a ld:JudicialPanel ; memberOfPanel ld:other .
       CORRECT: ld:Panel a ld:JudicialPanel ; ld:memberOfPanel ld:other .
    2. PREFIX DECLARATIONS: Remove any @prefix or @base lines.
       WRONG:  @prefix ld: <https://example.org/legal-domain#> .
       CORRECT: (delete the line entirely)
    3. PLAIN TEXT: Remove any lines that are not valid Turtle triples (prose, comments, markdown).
    4. MISSING TRIPLE TERMINATOR: Every subject block must end with ' .' and each predicate-object pair within a block must be separated by ' ;'.
    5. UNCLOSED LITERALS: Ensure all string literals are properly quoted.

    SUBGRAPH:
    {graph}

    OUTPUT RULES:
    - Return ONLY the corrected Turtle triples. No @prefix lines. No comments. No explanations.
    - If the subgraph is already valid, return it unchanged.
    - If the subgraph is empty or contains no recoverable triples, return an empty string.
    """