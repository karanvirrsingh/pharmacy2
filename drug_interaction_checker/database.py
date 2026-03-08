"""Drug interaction knowledge base.

Contains 50+ well-known drug–drug interactions across major pharmacological
categories: anticoagulants, NSAIDs, antibiotics, antidepressants,
antihypertensives, statins, opioids, and more.

Each entry maps a frozenset of two drug names to an :class:`Interaction`
object that includes description, mechanism, severity, and clinical
recommendation.
"""

from typing import Dict, FrozenSet, List

from drug_interaction_checker.models import Drug, Interaction, Severity

# ---------------------------------------------------------------------------
# Drug alias registry – maps every recognised name to a canonical drug name.
# ---------------------------------------------------------------------------
DRUG_ALIASES: List[Drug] = [
    # Anticoagulants
    Drug("Warfarin", ["Coumadin", "Jantoven"]),
    Drug("Heparin", ["Calciparin"]),
    Drug("Apixaban", ["Eliquis"]),
    Drug("Rivaroxaban", ["Xarelto"]),
    Drug("Dabigatran", ["Pradaxa"]),
    Drug("Clopidogrel", ["Plavix"]),
    Drug("Aspirin", ["ASA", "Acetylsalicylic acid", "Bayer", "Ecotrin"]),
    # NSAIDs
    Drug("Ibuprofen", ["Advil", "Motrin", "Nurofen"]),
    Drug("Naproxen", ["Aleve", "Naprosyn", "Anaprox"]),
    Drug("Indomethacin", ["Indocin"]),
    Drug("Celecoxib", ["Celebrex"]),
    Drug("Diclofenac", ["Voltaren", "Cambia"]),
    # Antibiotics
    Drug("Metronidazole", ["Flagyl", "Metrogel"]),
    Drug("Ciprofloxacin", ["Cipro", "Ciloxan"]),
    Drug("Clarithromycin", ["Biaxin"]),
    Drug("Erythromycin", ["Erythrocin", "EES"]),
    Drug("Rifampicin", ["Rifampin", "Rifadin", "Rimactane"]),
    Drug("Fluconazole", ["Diflucan"]),
    Drug("Trimethoprim", ["Primsol"]),
    Drug("Doxycycline", ["Vibramycin", "Doryx"]),
    # Antidepressants / Psychiatric
    Drug("Fluoxetine", ["Prozac", "Sarafem"]),
    Drug("Sertraline", ["Zoloft"]),
    Drug("Paroxetine", ["Paxil", "Pexeva"]),
    Drug("Citalopram", ["Celexa"]),
    Drug("Escitalopram", ["Lexapro"]),
    Drug("Venlafaxine", ["Effexor"]),
    Drug("Duloxetine", ["Cymbalta"]),
    Drug("Phenelzine", ["Nardil"]),
    Drug("Tranylcypromine", ["Parnate"]),
    Drug("Lithium", ["Lithobid", "Eskalith"]),
    Drug("Clozapine", ["Clozaril"]),
    Drug("Haloperidol", ["Haldol"]),
    Drug("Quetiapine", ["Seroquel"]),
    # Antihypertensives / Cardiovascular
    Drug("Lisinopril", ["Prinivil", "Zestril"]),
    Drug("Enalapril", ["Vasotec"]),
    Drug("Ramipril", ["Altace"]),
    Drug("Amlodipine", ["Norvasc"]),
    Drug("Metoprolol", ["Lopressor", "Toprol-XL"]),
    Drug("Atenolol", ["Tenormin"]),
    Drug("Carvedilol", ["Coreg"]),
    Drug("Digoxin", ["Lanoxin"]),
    Drug("Amiodarone", ["Cordarone", "Pacerone"]),
    Drug("Verapamil", ["Calan", "Verelan", "Isoptin"]),
    Drug("Diltiazem", ["Cardizem", "Tiazac"]),
    Drug("Spironolactone", ["Aldactone"]),
    Drug("Furosemide", ["Lasix"]),
    Drug("Hydrochlorothiazide", ["HCTZ", "Microzide"]),
    # Statins
    Drug("Simvastatin", ["Zocor"]),
    Drug("Atorvastatin", ["Lipitor"]),
    Drug("Rosuvastatin", ["Crestor"]),
    Drug("Lovastatin", ["Mevacor", "Altoprev"]),
    # Opioids / CNS
    Drug("Morphine", ["MS Contin", "Roxanol"]),
    Drug("Oxycodone", ["OxyContin", "Percocet"]),
    Drug("Codeine", ["Tylenol with Codeine"]),
    Drug("Tramadol", ["Ultram", "ConZip"]),
    Drug("Fentanyl", ["Duragesic", "Actiq"]),
    Drug("Methadone", ["Dolophine", "Methadose"]),
    Drug("Buprenorphine", ["Suboxone", "Subutex", "Buprenex"]),
    # Benzodiazepines
    Drug("Diazepam", ["Valium"]),
    Drug("Lorazepam", ["Ativan"]),
    Drug("Alprazolam", ["Xanax"]),
    Drug("Clonazepam", ["Klonopin"]),
    Drug("Midazolam", ["Versed"]),
    # Diabetes
    Drug("Metformin", ["Glucophage", "Glumetza"]),
    Drug("Glipizide", ["Glucotrol"]),
    Drug("Glyburide", ["DiaBeta", "Micronase"]),
    Drug("Insulin", ["Humulin", "Novolin", "Lantus", "Humalog"]),
    Drug("Sitagliptin", ["Januvia"]),
    # Immunosuppressants
    Drug("Cyclosporine", ["Sandimmune", "Neoral", "Gengraf"]),
    Drug("Tacrolimus", ["Prograf", "Astagraf"]),
    Drug("Mycophenolate", ["CellCept", "Myfortic"]),
    # Miscellaneous
    Drug("Phenytoin", ["Dilantin", "Phenytek"]),
    Drug("Carbamazepine", ["Tegretol", "Carbatrol"]),
    Drug("Valproate", ["Depakote", "Depakene", "Valproic acid"]),
    Drug("Theophylline", ["Theo-Dur", "Uniphyl"]),
    Drug("Allopurinol", ["Zyloprim", "Lopurin"]),
    Drug("Sildenafil", ["Viagra", "Revatio"]),
    Drug("Tadalafil", ["Cialis", "Adcirca"]),
    Drug("Nitroglycerin", ["Nitrates", "GTN", "Isosorbide mononitrate", "Isosorbide dinitrate", "Glyceryl trinitrate"]),
    Drug("Omeprazole", ["Prilosec"]),
    Drug("Cimetidine", ["Tagamet"]),
    Drug("Colchicine", ["Colcrys"]),
    Drug("Dexamethasone", ["Decadron"]),
    Drug("Prednisolone", ["Millipred"]),
    Drug("Prednisone", ["Deltasone"]),
    Drug("St. John's Wort", ["Hypericum perforatum"]),
    Drug("Alcohol", ["Ethanol"]),
]

# ---------------------------------------------------------------------------
# Interaction database
# ---------------------------------------------------------------------------
_RAW_INTERACTIONS: List[Interaction] = [
    # ── Anticoagulants ───────────────────────────────────────────────────────
    Interaction(
        drug1="Warfarin",
        drug2="Aspirin",
        description=(
            "Concurrent use significantly increases the risk of bleeding. "
            "Aspirin inhibits platelet aggregation while Warfarin impairs "
            "clotting-factor synthesis, producing a synergistic haemorrhagic effect."
        ),
        mechanism=(
            "Aspirin irreversibly acetylates COX-1, reducing thromboxane A2-mediated "
            "platelet aggregation. Warfarin inhibits vitamin K epoxide reductase, "
            "depleting clotting factors II, VII, IX and X."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid combination unless clearly indicated (e.g. mechanical heart valve). "
            "If used together, monitor INR closely and watch for signs of bleeding."
        ),
    ),
    Interaction(
        drug1="Warfarin",
        drug2="Ibuprofen",
        description=(
            "NSAIDs such as ibuprofen increase anticoagulant effect of Warfarin "
            "and cause GI mucosal damage, raising haemorrhage risk."
        ),
        mechanism=(
            "Ibuprofen displaces Warfarin from plasma-protein binding sites, "
            "transiently raising free Warfarin levels. COX inhibition impairs "
            "platelet function and damages the gastric mucosa."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid co-administration. Use paracetamol/acetaminophen as an alternative "
            "analgesic. If NSAID is necessary, monitor INR frequently."
        ),
    ),
    Interaction(
        drug1="Warfarin",
        drug2="Metronidazole",
        description=(
            "Metronidazole markedly potentiates the anticoagulant effect of "
            "Warfarin, increasing INR and bleeding risk."
        ),
        mechanism=(
            "Metronidazole inhibits CYP2C9, the primary enzyme responsible for "
            "metabolising S-Warfarin (the more potent enantiomer), leading to "
            "elevated Warfarin plasma levels."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Monitor INR closely during and for several days after the antibiotic "
            "course. Consider reducing Warfarin dose proactively."
        ),
    ),
    Interaction(
        drug1="Warfarin",
        drug2="Fluconazole",
        description=(
            "Fluconazole substantially increases Warfarin exposure, causing "
            "supratherapeutic INR and haemorrhage."
        ),
        mechanism=(
            "Fluconazole is a potent inhibitor of CYP2C9 and CYP3A4, both of "
            "which metabolise Warfarin, leading to dramatically increased "
            "drug concentrations."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Reduce Warfarin dose empirically by ~25–50% when starting fluconazole. "
            "Monitor INR every 2–3 days."
        ),
    ),
    Interaction(
        drug1="Warfarin",
        drug2="Amiodarone",
        description=(
            "Amiodarone greatly enhances Warfarin anticoagulation; the interaction "
            "is delayed (onset 1–4 weeks) and prolonged."
        ),
        mechanism=(
            "Amiodarone and its active metabolite desethylamiodarone inhibit "
            "CYP2C9 and CYP3A4. The long half-life of amiodarone means the "
            "interaction persists for weeks after discontinuation."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Reduce Warfarin dose by 30–50% when amiodarone is started. Monitor "
            "INR weekly initially, then monthly."
        ),
    ),
    Interaction(
        drug1="Warfarin",
        drug2="Rifampicin",
        description=(
            "Rifampicin dramatically reduces Warfarin efficacy, risking "
            "thromboembolic complications."
        ),
        mechanism=(
            "Rifampicin is a potent inducer of CYP2C9 and CYP3A4, markedly "
            "accelerating Warfarin metabolism and reducing its plasma levels "
            "by up to 80%."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid this combination if possible. If unavoidable, monitor INR "
            "very frequently and expect large Warfarin dose increases."
        ),
    ),
    Interaction(
        drug1="Warfarin",
        drug2="St. John's Wort",
        description=(
            "St. John's Wort reduces Warfarin plasma levels and anticoagulant "
            "effect, increasing the risk of thrombosis."
        ),
        mechanism=(
            "Hyperforin, the active constituent of St. John's Wort, strongly "
            "induces CYP3A4, CYP2C9, and P-glycoprotein, accelerating Warfarin "
            "metabolism and reducing absorption."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid concurrent use. Patients on Warfarin should be counselled to "
            "disclose all herbal supplements."
        ),
    ),
    Interaction(
        drug1="Warfarin",
        drug2="Clopidogrel",
        description=(
            "Triple-therapy risk: combining antiplatelet and anticoagulant agents "
            "substantially increases major and fatal bleeding events."
        ),
        mechanism=(
            "Clopidogrel irreversibly inhibits ADP-mediated platelet aggregation "
            "(P2Y12 receptor), while Warfarin inhibits coagulation cascade factors, "
            "together producing additive haemostatic impairment."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Use only when clearly indicated (e.g. ACS with AF). Limit duration, "
            "use a PPI, and monitor closely for bleeding."
        ),
    ),
    Interaction(
        drug1="Clopidogrel",
        drug2="Omeprazole",
        description=(
            "Omeprazole reduces the antiplatelet effect of clopidogrel, potentially "
            "increasing cardiovascular event risk."
        ),
        mechanism=(
            "Clopidogrel is a prodrug requiring CYP2C19 activation. Omeprazole "
            "inhibits CYP2C19, reducing formation of the active thiol metabolite."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Prefer pantoprazole or famotidine as gastroprotection in patients "
            "taking clopidogrel. Avoid omeprazole and esomeprazole."
        ),
    ),
    Interaction(
        drug1="Aspirin",
        drug2="Ibuprofen",
        description=(
            "Ibuprofen competitively antagonises the antiplatelet effect of "
            "low-dose aspirin, potentially reducing its cardioprotective benefit."
        ),
        mechanism=(
            "Both drugs compete for the same serine residue (Ser530) on COX-1. "
            "If ibuprofen occupies the site first, aspirin cannot irreversibly "
            "acetylate it, negating its sustained antiplatelet action."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Take aspirin at least 30 minutes before or 8 hours after ibuprofen. "
            "Consider paracetamol as an alternative analgesic."
        ),
    ),
    # ── ACE Inhibitors / Antihypertensives ────────────────────────────────────
    Interaction(
        drug1="Lisinopril",
        drug2="Spironolactone",
        description=(
            "Co-administration can cause dangerous hyperkalaemia, "
            "potentially leading to cardiac arrhythmias."
        ),
        mechanism=(
            "Lisinopril (ACE inhibitor) reduces aldosterone secretion, thereby "
            "decreasing potassium excretion. Spironolactone further blocks "
            "aldosterone receptors, compounding potassium retention."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Monitor serum potassium frequently. Avoid in patients with "
            "renal impairment or baseline hyperkalaemia."
        ),
    ),
    Interaction(
        drug1="Lisinopril",
        drug2="Ibuprofen",
        description=(
            "NSAIDs blunt the antihypertensive effect of ACE inhibitors and "
            "increase risk of acute kidney injury."
        ),
        mechanism=(
            "NSAIDs inhibit prostaglandin-mediated afferent arteriolar dilation; "
            "when combined with ACE inhibitor-induced efferent dilation, this "
            "reduces glomerular filtration and raises blood pressure."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Avoid long-term NSAID use in patients on ACE inhibitors. "
            "Monitor blood pressure and renal function."
        ),
    ),
    Interaction(
        drug1="Lisinopril",
        drug2="Potassium",
        description=(
            "ACE inhibitors combined with potassium supplements markedly "
            "increase hyperkalaemia risk."
        ),
        mechanism=(
            "ACE inhibitors reduce aldosterone secretion, decreasing renal "
            "potassium excretion. Adding exogenous potassium further elevates "
            "serum potassium levels."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Avoid potassium supplements unless documented deficiency exists. "
            "Monitor serum electrolytes regularly."
        ),
    ),
    # ── Beta-blockers ─────────────────────────────────────────────────────────
    Interaction(
        drug1="Metoprolol",
        drug2="Verapamil",
        description=(
            "Concurrent use of a beta-blocker and a non-dihydropyridine calcium "
            "channel blocker can cause severe bradycardia and heart block."
        ),
        mechanism=(
            "Both drugs independently slow AV conduction. Metoprolol decreases "
            "heart rate via β1 blockade; verapamil inhibits L-type calcium "
            "channels in SA and AV nodes, producing additive negative chronotropy."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Avoid IV verapamil in patients receiving beta-blockers. "
            "Use only with extreme caution in oral form; monitor ECG closely."
        ),
    ),
    Interaction(
        drug1="Metoprolol",
        drug2="Diltiazem",
        description=(
            "Combination may cause excessive bradycardia, AV block or cardiac "
            "failure due to additive cardiac depression."
        ),
        mechanism=(
            "Diltiazem inhibits L-type calcium channels in the SA and AV nodes "
            "and additionally inhibits CYP2D6, the main enzyme metabolising "
            "metoprolol, raising its plasma levels."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Use with extreme caution if at all. Closely monitor ECG, heart rate "
            "and blood pressure. Consider alternative antihypertensive."
        ),
    ),
    Interaction(
        drug1="Atenolol",
        drug2="Insulin",
        description=(
            "Beta-blockers mask the adrenergic warning signs of hypoglycaemia "
            "and may prolong hypoglycaemic episodes."
        ),
        mechanism=(
            "Catecholamine-mediated symptoms of hypoglycaemia (tremor, tachycardia, "
            "anxiety) are suppressed by β-blockade. Glycogenolysis is also reduced, "
            "delaying recovery from low blood glucose."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Educate patients to monitor blood glucose more frequently. "
            "Sweating remains an unmasked symptom of hypoglycaemia."
        ),
    ),
    # ── Digoxin ───────────────────────────────────────────────────────────────
    Interaction(
        drug1="Digoxin",
        drug2="Amiodarone",
        description=(
            "Amiodarone substantially increases digoxin plasma levels, "
            "leading to digoxin toxicity."
        ),
        mechanism=(
            "Amiodarone inhibits P-glycoprotein (renal tubular efflux) and "
            "CYP3A4, both involved in digoxin elimination, resulting in "
            "significantly elevated digoxin concentrations."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Reduce digoxin dose by 30–50% when amiodarone is initiated. "
            "Monitor digoxin levels and ECG closely."
        ),
    ),
    Interaction(
        drug1="Digoxin",
        drug2="Verapamil",
        description=(
            "Verapamil increases digoxin levels and both drugs slow the "
            "heart, creating risk of severe bradycardia and AV block."
        ),
        mechanism=(
            "Verapamil reduces renal and non-renal clearance of digoxin by "
            "inhibiting P-glycoprotein, raising plasma digoxin by 50–75%."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Reduce digoxin dose when initiating verapamil. Monitor digoxin "
            "levels and ECG. Consider a dihydropyridine calcium channel blocker "
            "as an alternative."
        ),
    ),
    Interaction(
        drug1="Digoxin",
        drug2="Furosemide",
        description=(
            "Furosemide-induced hypokalaemia potentiates digoxin toxicity, "
            "as low serum potassium increases digoxin binding to Na+/K+-ATPase."
        ),
        mechanism=(
            "Loop diuretics increase renal potassium excretion. Hypokalaemia "
            "enhances sensitivity of the Na+/K+-ATPase pump to digoxin, "
            "increasing the risk of arrhythmias."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Monitor serum potassium regularly. Supplement potassium as needed. "
            "Monitor ECG for digoxin toxicity signs."
        ),
    ),
    # ── Statins ───────────────────────────────────────────────────────────────
    Interaction(
        drug1="Simvastatin",
        drug2="Amiodarone",
        description=(
            "Amiodarone increases simvastatin exposure, raising the risk of "
            "myopathy and potentially fatal rhabdomyolysis."
        ),
        mechanism=(
            "Amiodarone inhibits CYP3A4, the primary enzyme metabolising "
            "simvastatin, leading to markedly elevated plasma statin levels "
            "and increased skeletal-muscle toxicity."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Do not exceed simvastatin 20 mg/day with amiodarone. "
            "Consider switching to pravastatin or rosuvastatin (not CYP3A4-dependent)."
        ),
    ),
    Interaction(
        drug1="Simvastatin",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin dramatically increases simvastatin levels, "
            "greatly elevating rhabdomyolysis risk."
        ),
        mechanism=(
            "Clarithromycin is a potent CYP3A4 inhibitor. Simvastatin undergoes "
            "extensive first-pass CYP3A4 metabolism; inhibition raises AUC "
            "by up to 10-fold."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Suspend simvastatin during clarithromycin therapy. "
            "Consider azithromycin as the antibiotic alternative."
        ),
    ),
    Interaction(
        drug1="Atorvastatin",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin increases atorvastatin exposure and risk of "
            "myopathy/rhabdomyolysis."
        ),
        mechanism=(
            "Clarithromycin inhibits CYP3A4 and P-glycoprotein, both involved "
            "in atorvastatin metabolism and efflux."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Limit atorvastatin to 20 mg/day during clarithromycin therapy or "
            "temporarily suspend statin. Monitor for muscle pain/weakness."
        ),
    ),
    Interaction(
        drug1="Simvastatin",
        drug2="Verapamil",
        description=(
            "Verapamil raises simvastatin plasma concentrations, increasing "
            "the risk of myopathy."
        ),
        mechanism=(
            "Verapamil inhibits CYP3A4 and P-glycoprotein-mediated efflux, "
            "impairing simvastatin metabolism and increasing its bioavailability."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Do not exceed simvastatin 10 mg/day when combined with verapamil. "
            "Consider switching to a non-CYP3A4-metabolised statin."
        ),
    ),
    Interaction(
        drug1="Atorvastatin",
        drug2="Rifampicin",
        description=(
            "Rifampicin markedly reduces atorvastatin efficacy through potent "
            "enzyme induction."
        ),
        mechanism=(
            "Rifampicin is a potent CYP3A4 and CYP2C9 inducer as well as a "
            "P-glycoprotein inducer, drastically reducing atorvastatin AUC."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Avoid co-administration. If unavoidable, monitor LDL cholesterol "
            "and consider dose adjustment."
        ),
    ),
    Interaction(
        drug1="Lovastatin",
        drug2="Cyclosporine",
        description=(
            "Cyclosporine greatly increases lovastatin exposure, raising risk "
            "of severe myopathy and rhabdomyolysis."
        ),
        mechanism=(
            "Cyclosporine inhibits CYP3A4 and OATP1B1 uptake transporter, "
            "dramatically reducing lovastatin hepatic elimination."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Avoid lovastatin (and simvastatin) in patients on cyclosporine. "
            "Use pravastatin or fluvastatin at lowest effective doses."
        ),
    ),
    # ── SSRIs / Antidepressants ────────────────────────────────────────────────
    Interaction(
        drug1="Fluoxetine",
        drug2="Tramadol",
        description=(
            "Combination increases serotonin syndrome risk and reduces tramadol "
            "analgesic efficacy."
        ),
        mechanism=(
            "Fluoxetine inhibits CYP2D6, impairing conversion of tramadol to its "
            "active μ-opioid metabolite (O-desmethyltramadol). Serotonergic "
            "synergy between SSRI and tramadol's SNRI-like action raises "
            "serotonin syndrome risk."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid combination. Consider alternative opioid analgesic that does "
            "not rely on CYP2D6. Monitor for serotonin syndrome symptoms."
        ),
    ),
    Interaction(
        drug1="Fluoxetine",
        drug2="Warfarin",
        description=(
            "SSRIs increase bleeding risk, particularly GI haemorrhage, and "
            "fluoxetine may raise Warfarin plasma levels."
        ),
        mechanism=(
            "Fluoxetine inhibits CYP2C9 and CYP2C19, the primary Warfarin "
            "metabolising enzymes. SSRIs also reduce platelet serotonin stores, "
            "impairing platelet aggregation."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor INR closely after starting or changing SSRI dose. "
            "Educate patient on signs of bleeding."
        ),
    ),
    Interaction(
        drug1="Sertraline",
        drug2="Tramadol",
        description=(
            "Serotonin syndrome risk is increased when sertraline and tramadol "
            "are co-administered."
        ),
        mechanism=(
            "Both sertraline (SSRI) and tramadol (serotonin/noradrenaline reuptake "
            "inhibitor) increase serotonergic transmission, producing additive "
            "or synergistic serotonin toxicity."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid combination. If both are required, use lowest effective doses "
            "and monitor carefully for serotonin syndrome."
        ),
    ),
    Interaction(
        drug1="Phenelzine",
        drug2="Fluoxetine",
        description=(
            "This combination can cause potentially fatal serotonin syndrome "
            "with hyperthermia, rigidity, and cardiovascular collapse."
        ),
        mechanism=(
            "MAO inhibitors (phenelzine) prevent serotonin breakdown. "
            "Fluoxetine blocks serotonin reuptake. Together they cause extreme "
            "accumulation of synaptic serotonin."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Absolutely contraindicated. Allow a 14-day washout after stopping "
            "MAOIs before starting SSRIs, and a 5-week washout after fluoxetine "
            "before starting an MAOI."
        ),
    ),
    Interaction(
        drug1="Phenelzine",
        drug2="Sertraline",
        description=(
            "Combining MAOI with any SSRI risks life-threatening serotonin syndrome."
        ),
        mechanism=(
            "Inhibition of MAO by phenelzine prevents serotonin degradation; "
            "sertraline blocks serotonin reuptake, causing extreme serotonergic "
            "excess."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Absolutely contraindicated. Allow a 14-day washout after stopping "
            "MAOI before starting sertraline."
        ),
    ),
    Interaction(
        drug1="Lithium",
        drug2="Ibuprofen",
        description=(
            "NSAIDs raise lithium plasma levels, risking lithium toxicity."
        ),
        mechanism=(
            "NSAIDs reduce renal prostaglandin synthesis, decreasing renal "
            "blood flow and glomerular filtration, impairing lithium excretion "
            "and raising serum lithium concentrations."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid NSAIDs in patients on lithium. Use paracetamol if an "
            "analgesic is needed. Monitor lithium levels closely."
        ),
    ),
    Interaction(
        drug1="Lithium",
        drug2="Hydrochlorothiazide",
        description=(
            "Thiazide diuretics decrease renal lithium clearance, causing "
            "lithium toxicity."
        ),
        mechanism=(
            "Thiazides induce sodium depletion, prompting the proximal tubule "
            "to reabsorb both sodium and lithium (as lithium follows sodium), "
            "thus reducing lithium excretion."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Reduce lithium dose when adding thiazide diuretics. Monitor "
            "serum lithium levels closely."
        ),
    ),
    Interaction(
        drug1="Valproate",
        drug2="Aspirin",
        description=(
            "Aspirin inhibits valproate metabolism, increasing plasma levels "
            "and risk of valproate toxicity."
        ),
        mechanism=(
            "Aspirin competes for plasma protein binding and inhibits β-oxidation "
            "of valproate, raising free drug levels and the risk of sedation, "
            "tremor, and hepatotoxicity."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor for signs of valproate toxicity (drowsiness, tremor). "
            "Use paracetamol instead of aspirin."
        ),
    ),
    Interaction(
        drug1="Phenytoin",
        drug2="Carbamazepine",
        description=(
            "Combination results in complex, unpredictable changes in plasma "
            "levels of both anticonvulsants, potentially causing toxicity or "
            "loss of seizure control."
        ),
        mechanism=(
            "Carbamazepine induces CYP3A4 and CYP2C9, accelerating phenytoin "
            "metabolism. Phenytoin in turn induces carbamazepine metabolism. "
            "The net effect on each drug level is unpredictable."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor plasma levels of both drugs frequently. Be alert for toxicity "
            "or breakthrough seizures when adjusting doses."
        ),
    ),
    # ── Opioids / CNS ─────────────────────────────────────────────────────────
    Interaction(
        drug1="Morphine",
        drug2="Alcohol",
        description=(
            "Concurrent use of opioids and alcohol profoundly depresses the "
            "central nervous system, risking respiratory depression and death."
        ),
        mechanism=(
            "Both substances depress CNS activity: opioids via μ-receptor agonism, "
            "alcohol via GABA-A potentiation and NMDA antagonism. Together, "
            "they produce supra-additive respiratory depression."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Patients on opioids must be counselled to avoid alcohol completely. "
            "Extended-release opioid formulations are especially dangerous with "
            "alcohol due to dose-dumping."
        ),
    ),
    Interaction(
        drug1="Tramadol",
        drug2="Alcohol",
        description=(
            "Alcohol enhances sedation and respiratory depression of tramadol."
        ),
        mechanism=(
            "Additive CNS depression through complementary mechanisms (GABA "
            "potentiation by alcohol, μ-opioid and SNRI activity by tramadol). "
            "Risk of dangerous sedation and impaired psychomotor performance."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid alcohol during tramadol therapy. Warn patients about sedation "
            "and driving impairment."
        ),
    ),
    Interaction(
        drug1="Buprenorphine",
        drug2="Diazepam",
        description=(
            "Co-prescription of buprenorphine and benzodiazepines substantially "
            "increases risk of fatal respiratory depression."
        ),
        mechanism=(
            "Benzodiazepines potentiate GABA-A-mediated CNS depression. "
            "When combined with the opioid agonist/partial-agonist buprenorphine, "
            "additive respiratory depression occurs."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid co-prescription where possible. If unavoidable, use lowest "
            "effective doses, monitor closely, and ensure naloxone is accessible."
        ),
    ),
    Interaction(
        drug1="Methadone",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin increases methadone plasma levels, causing QTc "
            "prolongation and potentially fatal torsades de pointes."
        ),
        mechanism=(
            "Clarithromycin inhibits CYP3A4, which metabolises methadone. "
            "Both drugs independently prolong the QTc interval, producing an "
            "additive effect on cardiac repolarisation."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid co-administration. Monitor ECG carefully if combination is "
            "necessary. Consider alternative antibiotic."
        ),
    ),
    Interaction(
        drug1="Fentanyl",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin increases fentanyl exposure, markedly raising risk "
            "of opioid toxicity and respiratory depression."
        ),
        mechanism=(
            "Fentanyl is primarily metabolised by CYP3A4. Clarithromycin inhibits "
            "CYP3A4 and intestinal P-glycoprotein, raising fentanyl bioavailability "
            "and reducing its clearance."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Monitor for opioid toxicity (respiratory depression, sedation). "
            "Reduce fentanyl dose and consider alternative antibiotic."
        ),
    ),
    Interaction(
        drug1="Oxycodone",
        drug2="Alcohol",
        description=(
            "Alcohol markedly enhances the CNS depressant effects of oxycodone, "
            "increasing risk of respiratory depression and death."
        ),
        mechanism=(
            "Additive CNS depression. Alcohol also inhibits CYP3A4, raising "
            "oxycodone plasma levels."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Patients on oxycodone must avoid alcohol entirely. Extended-release "
            "oxycodone with alcohol can release the full dose immediately "
            "(dose-dumping)."
        ),
    ),
    # ── Antibiotics ───────────────────────────────────────────────────────────
    Interaction(
        drug1="Ciprofloxacin",
        drug2="Theophylline",
        description=(
            "Ciprofloxacin raises theophylline levels, potentially causing "
            "serious toxicity (nausea, seizures, arrhythmias)."
        ),
        mechanism=(
            "Ciprofloxacin inhibits CYP1A2, the principal enzyme metabolising "
            "theophylline, causing accumulation."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Reduce theophylline dose by 50% when ciprofloxacin is started. "
            "Monitor serum theophylline levels closely."
        ),
    ),
    Interaction(
        drug1="Ciprofloxacin",
        drug2="Warfarin",
        description=(
            "Fluoroquinolones can potentiate Warfarin anticoagulation and increase "
            "bleeding risk."
        ),
        mechanism=(
            "Ciprofloxacin inhibits CYP1A2 (which metabolises R-Warfarin) and "
            "may reduce gut flora that produce vitamin K2."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor INR closely during and shortly after ciprofloxacin therapy. "
            "Adjust Warfarin dose as needed."
        ),
    ),
    Interaction(
        drug1="Clarithromycin",
        drug2="Carbamazepine",
        description=(
            "Clarithromycin markedly increases carbamazepine levels, causing "
            "neurotoxicity."
        ),
        mechanism=(
            "Carbamazepine is a CYP3A4 substrate; clarithromycin is a potent "
            "CYP3A4 inhibitor, leading to a 2–3-fold rise in carbamazepine levels."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid combination or monitor carbamazepine levels closely. "
            "Consider azithromycin as an alternative antibiotic."
        ),
    ),
    Interaction(
        drug1="Trimethoprim",
        drug2="Warfarin",
        description=(
            "Trimethoprim enhances Warfarin anticoagulation via enzyme inhibition."
        ),
        mechanism=(
            "Trimethoprim inhibits CYP2C8 and may indirectly affect Warfarin "
            "metabolism. It also reduces Warfarin renal clearance."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor INR during and for several days after trimethoprim treatment. "
            "Adjust Warfarin dose if necessary."
        ),
    ),
    Interaction(
        drug1="Metronidazole",
        drug2="Alcohol",
        description=(
            "A disulfiram-like reaction occurs: flushing, nausea, vomiting, "
            "headache, and hypotension."
        ),
        mechanism=(
            "Metronidazole (and its metabolites) inhibit aldehyde dehydrogenase, "
            "causing acetaldehyde to accumulate when alcohol is consumed."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Patients must avoid all alcohol during metronidazole therapy "
            "and for at least 48 hours after the last dose."
        ),
    ),
    # ── Immunosuppressants ────────────────────────────────────────────────────
    Interaction(
        drug1="Cyclosporine",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin greatly increases cyclosporine blood levels, "
            "raising the risk of nephrotoxicity and other side effects."
        ),
        mechanism=(
            "Clarithromycin inhibits CYP3A4 and P-glycoprotein, the primary "
            "clearance pathways for cyclosporine."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid combination or reduce cyclosporine dose significantly. "
            "Monitor trough levels and renal function closely."
        ),
    ),
    Interaction(
        drug1="Tacrolimus",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin substantially increases tacrolimus exposure, "
            "leading to nephrotoxicity and potential organ rejection "
            "if under-dosed on dose reduction."
        ),
        mechanism=(
            "Tacrolimus is metabolised primarily by CYP3A4 and transported by "
            "P-glycoprotein. Clarithromycin inhibits both, causing 3–10-fold "
            "increases in tacrolimus exposure."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Monitor tacrolimus trough levels daily and reduce dose appropriately. "
            "Consider a macrolide that is a weaker CYP3A4 inhibitor."
        ),
    ),
    Interaction(
        drug1="Cyclosporine",
        drug2="Simvastatin",
        description=(
            "Combination substantially raises simvastatin levels, greatly "
            "increasing risk of myopathy and rhabdomyolysis."
        ),
        mechanism=(
            "Cyclosporine inhibits OATP1B1 hepatic uptake transporter and "
            "CYP3A4, preventing simvastatin elimination."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Avoid simvastatin in patients taking cyclosporine. Use pravastatin "
            "at lowest effective dose instead."
        ),
    ),
    # ── Diabetes ──────────────────────────────────────────────────────────────
    Interaction(
        drug1="Metformin",
        drug2="Alcohol",
        description=(
            "Alcohol combined with metformin increases the risk of lactic acidosis."
        ),
        mechanism=(
            "Alcohol inhibits hepatic gluconeogenesis and increases lactate "
            "production. Metformin impairs hepatic lactate clearance; together "
            "they raise plasma lactate levels."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Patients should minimise alcohol intake while taking metformin. "
            "Avoid alcohol in patients with renal or hepatic impairment."
        ),
    ),
    Interaction(
        drug1="Glipizide",
        drug2="Fluconazole",
        description=(
            "Fluconazole increases glipizide plasma levels, causing prolonged "
            "and severe hypoglycaemia."
        ),
        mechanism=(
            "Glipizide is metabolised by CYP2C9. Fluconazole is a potent CYP2C9 "
            "inhibitor, reducing glipizide metabolism."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Monitor blood glucose closely. Consider dose reduction of glipizide "
            "and use an alternative antifungal if possible."
        ),
    ),
    Interaction(
        drug1="Insulin",
        drug2="Alcohol",
        description=(
            "Alcohol potentiates insulin-induced hypoglycaemia and inhibits "
            "the counter-regulatory glucagon response."
        ),
        mechanism=(
            "Alcohol suppresses hepatic gluconeogenesis and inhibits the "
            "catecholamine and glucagon responses to hypoglycaemia, deepening "
            "and prolonging low blood glucose episodes."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Patients on insulin must be counselled about hypoglycaemia risk "
            "with alcohol. Eat when drinking and monitor blood glucose closely."
        ),
    ),
    Interaction(
        drug1="Metformin",
        drug2="Ciprofloxacin",
        description=(
            "Fluoroquinolones can cause glucose dysregulation, either hyperglycaemia "
            "or hypoglycaemia, complicating diabetes management."
        ),
        mechanism=(
            "Ciprofloxacin affects insulin secretion by blocking pancreatic "
            "β-cell KATP channels. This can unpredictably alter blood glucose."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor blood glucose more frequently during fluoroquinolone therapy "
            "in diabetic patients."
        ),
    ),
    # ── Sildenafil / PDE5 inhibitors ──────────────────────────────────────────
    Interaction(
        drug1="Sildenafil",
        drug2="Nitroglycerin",
        description=(
            "The combination of sildenafil with nitrates (including nitroglycerin, "
            "isosorbide mononitrate, and isosorbide dinitrate) causes severe, "
            "potentially life-threatening hypotension."
        ),
        mechanism=(
            "Both sildenafil (PDE5 inhibition) and nitrates (cGMP production) "
            "increase cyclic GMP in smooth muscle, causing profound vasodilation "
            "and precipitous blood-pressure drop."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Absolutely contraindicated. Do not use together. "
            "Nitrates should not be given within 24 hours of sildenafil."
        ),
    ),
    Interaction(
        drug1="Sildenafil",
        drug2="Ritonavir",
        description=(
            "Ritonavir markedly increases sildenafil plasma levels, risking "
            "severe hypotension and priapism."
        ),
        mechanism=(
            "Ritonavir is a potent CYP3A4 inhibitor; sildenafil is primarily "
            "metabolised by CYP3A4, leading to >10-fold increases in sildenafil "
            "exposure."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Sildenafil for erectile dysfunction is contraindicated with ritonavir. "
            "For pulmonary arterial hypertension, the maximum dose is 20 mg every "
            "48 hours."
        ),
    ),
    # ── Miscellaneous ─────────────────────────────────────────────────────────
    Interaction(
        drug1="Allopurinol",
        drug2="Azathioprine",
        description=(
            "Allopurinol dramatically increases azathioprine toxicity, causing "
            "severe bone marrow suppression."
        ),
        mechanism=(
            "Allopurinol inhibits xanthine oxidase, which is required for the "
            "inactivation of 6-mercaptopurine (the active metabolite of "
            "azathioprine), leading to accumulation of toxic levels."
        ),
        severity=Severity.CONTRAINDICATED,
        recommendation=(
            "Avoid combination. If allopurinol is necessary, reduce azathioprine "
            "dose by 75% and monitor FBC closely."
        ),
    ),
    Interaction(
        drug1="Colchicine",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin markedly increases colchicine levels, causing "
            "colchicine toxicity (myopathy, pancytopenia, multiorgan failure)."
        ),
        mechanism=(
            "Colchicine is a substrate of both CYP3A4 and P-glycoprotein. "
            "Clarithromycin inhibits both, greatly reducing colchicine elimination."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid combination. Reduce colchicine dose or use an alternative "
            "antibiotic. Monitor for GI symptoms and muscle pain."
        ),
    ),
    Interaction(
        drug1="Theophylline",
        drug2="Erythromycin",
        description=(
            "Erythromycin increases theophylline levels, raising the risk "
            "of serious toxicity."
        ),
        mechanism=(
            "Erythromycin inhibits CYP1A2, the primary enzyme metabolising "
            "theophylline, causing accumulation."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Reduce theophylline dose by 25–50% when erythromycin is added. "
            "Monitor serum theophylline levels closely."
        ),
    ),
    Interaction(
        drug1="Dexamethasone",
        drug2="Warfarin",
        description=(
            "Corticosteroids can both increase and decrease Warfarin effect; "
            "net result is unpredictable and monitoring is essential."
        ),
        mechanism=(
            "Corticosteroids alter hepatic metabolism of Warfarin via CYP450 "
            "induction. High-dose or prolonged steroids may enhance Warfarin "
            "effect through unknown mechanisms."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor INR closely when starting, changing, or stopping "
            "corticosteroid therapy."
        ),
    ),
    Interaction(
        drug1="Prednisone",
        drug2="Ibuprofen",
        description=(
            "Combining corticosteroids and NSAIDs greatly increases the risk "
            "of GI ulceration and haemorrhage."
        ),
        mechanism=(
            "Corticosteroids reduce prostaglandin-mediated gastric mucosal "
            "protection. NSAIDs inhibit COX enzymes, reducing cytoprotective "
            "prostaglandins. Together the risk is additive."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid this combination. If both are required, add a proton pump "
            "inhibitor or misoprostol for gastroprotection."
        ),
    ),
    Interaction(
        drug1="Rifampicin",
        drug2="Oral contraceptives",
        description=(
            "Rifampicin substantially reduces the efficacy of combined oral "
            "contraceptives, increasing the risk of unintended pregnancy."
        ),
        mechanism=(
            "Rifampicin is a potent inducer of CYP3A4 and P-glycoprotein, "
            "dramatically increasing the metabolism of oestrogen and progestogen "
            "components."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Use additional contraception (e.g. barrier methods) during "
            "rifampicin therapy and for 4 weeks after stopping."
        ),
    ),
    Interaction(
        drug1="St. John's Wort",
        drug2="Oral contraceptives",
        description=(
            "St. John's Wort reduces the blood levels of oral contraceptives, "
            "risking contraceptive failure."
        ),
        mechanism=(
            "Hyperforin induces CYP3A4 and P-glycoprotein, accelerating "
            "metabolism and reducing systemic exposure of hormonal contraceptives."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Use barrier contraception while taking St. John's Wort. "
            "Counsel patients about this interaction."
        ),
    ),
    Interaction(
        drug1="Ciprofloxacin",
        drug2="Antacids",
        description=(
            "Antacids containing aluminium, magnesium, or calcium markedly "
            "reduce ciprofloxacin absorption."
        ),
        mechanism=(
            "Ciprofloxacin chelates polyvalent metal ions in the gut lumen, "
            "forming insoluble complexes that cannot be absorbed."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Separate doses by at least 2 hours (ciprofloxacin before, "
            "or 6 hours after, antacid administration)."
        ),
    ),
    Interaction(
        drug1="Doxycycline",
        drug2="Antacids",
        description=(
            "Antacids and dairy products reduce doxycycline absorption, "
            "potentially causing treatment failure."
        ),
        mechanism=(
            "Doxycycline chelates divalent cations (Ca²⁺, Mg²⁺, Al³⁺, Fe²⁺), "
            "forming non-absorbable complexes in the GI tract."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Take doxycycline 1–2 hours before antacids or dairy products. "
            "Avoid iron-containing products within 3 hours."
        ),
    ),
    Interaction(
        drug1="Quetiapine",
        drug2="Clarithromycin",
        description=(
            "Clarithromycin can dramatically increase quetiapine plasma levels, "
            "risking QTc prolongation, sedation, and hypotension."
        ),
        mechanism=(
            "Quetiapine is predominantly metabolised by CYP3A4. Clarithromycin "
            "inhibits CYP3A4, raising quetiapine AUC substantially."
        ),
        severity=Severity.MAJOR,
        recommendation=(
            "Avoid combination or reduce quetiapine dose significantly. "
            "Consider azithromycin as alternative antibiotic."
        ),
    ),
    Interaction(
        drug1="Haloperidol",
        drug2="Carbamazepine",
        description=(
            "Carbamazepine reduces haloperidol plasma levels, potentially "
            "causing loss of antipsychotic effect."
        ),
        mechanism=(
            "Carbamazepine induces CYP3A4 and CYP2D6, both involved in "
            "haloperidol metabolism, reducing its plasma concentrations by "
            "50–60%."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor for worsening psychiatric symptoms when combining these "
            "drugs. Consider dose adjustment."
        ),
    ),
    Interaction(
        drug1="Cimetidine",
        drug2="Warfarin",
        description=(
            "Cimetidine increases Warfarin levels by inhibiting its hepatic "
            "metabolism."
        ),
        mechanism=(
            "Cimetidine is a broad CYP450 inhibitor (CYP1A2, CYP2C9, CYP2D6, "
            "CYP3A4), reducing Warfarin clearance and raising INR."
        ),
        severity=Severity.MODERATE,
        recommendation=(
            "Monitor INR when cimetidine is added or discontinued. Consider "
            "switching to famotidine or ranitidine (fewer interactions)."
        ),
    ),
    # ── Minor interactions ────────────────────────────────────────────────────
    Interaction(
        drug1="Metformin",
        drug2="Furosemide",
        description=(
            "Furosemide may slightly increase metformin plasma concentrations. "
            "The effect is modest and rarely clinically significant in patients "
            "with normal renal function."
        ),
        mechanism=(
            "Furosemide competes with metformin for tubular secretion via the "
            "organic cation transporter (OCT2) in the renal proximal tubule, "
            "mildly reducing metformin clearance."
        ),
        severity=Severity.MINOR,
        recommendation=(
            "No dose adjustment is usually necessary. Monitor renal function and "
            "blood glucose, especially in patients with impaired renal function."
        ),
    ),
    Interaction(
        drug1="Atenolol",
        drug2="Aspirin",
        description=(
            "High-dose aspirin and other NSAIDs may mildly attenuate the "
            "antihypertensive effect of atenolol, though the clinical impact "
            "at low (antiplatelet) aspirin doses is minimal."
        ),
        mechanism=(
            "NSAIDs inhibit prostaglandin synthesis, which partially counteracts "
            "the vasodilatory and natriuretic effects that contribute to the "
            "antihypertensive action of beta-blockers."
        ),
        severity=Severity.MINOR,
        recommendation=(
            "No action usually required at low aspirin doses. Monitor blood "
            "pressure if high-dose or long-term NSAID use is initiated."
        ),
    ),
]


def _build_interaction_map(
    interactions: list,
) -> Dict[FrozenSet[str], Interaction]:
    """Index interaction list by a frozenset of lowercased drug names."""
    result: Dict[FrozenSet[str], Interaction] = {}
    for interaction in interactions:
        key = frozenset(
            [interaction.drug1.lower(), interaction.drug2.lower()]
        )
        result[key] = interaction
    return result


def _build_alias_map(drugs: list) -> Dict[str, str]:
    """Return a mapping of every alias (lowercased) → canonical drug name."""
    alias_map: Dict[str, str] = {}
    for drug in drugs:
        for name in drug.all_names():
            alias_map[name.lower()] = drug.name
    return alias_map


# Public singletons used by the checker
INTERACTION_MAP: Dict[FrozenSet[str], Interaction] = _build_interaction_map(
    _RAW_INTERACTIONS
)
ALIAS_MAP: Dict[str, str] = _build_alias_map(DRUG_ALIASES)
ALL_DRUG_NAMES: List[str] = sorted(ALIAS_MAP.keys())
