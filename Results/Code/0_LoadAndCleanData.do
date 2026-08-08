*** Load, label and clean data 

clear all
cd "/Users/svsalin/Desktop/course_exper/Results" // use your working directory here!

//------------------------
//------------------------
//------------------------
//------------------------

//------------------------
// Session 1
// Get raw data (output from oTree)
import delim "Input/Session_1/design_exp_2025-09-09.csv", delimiters(",") varnames(1) clear
gen session = 1
save "Input/rawdata_1", replace

import delim "Input/Session_1/PageTimes-2025-09-09.csv", delimiters(",") varnames(1) clear
gen session = 1
save "Input/pagetimes_1", replace

//------------------------
// Session 2
// Get raw data (output from oTree)
import delim "Input/Session_2/design_exp_2025-09-24.csv", delimiters(",") varnames(1) clear
gen session = 2
save "Input/rawdata_2", replace

import delim "Input/Session_2/PageTimes-2025-09-24.csv", delimiters(",") varnames(1) clear
gen session = 2
save "Input/pagetimes_2", replace

//------------------------
//------------------------

// For now, just use session 1 data -- later also session 2
/**/ 
use "Input/rawdata_1", clear
save "Input/rawdata", replace

use "Input/pagetimes_1", clear
save "Input/pagetimes", replace

// Merge sessions: Need to be careful later when merging pagetimes into rawdata
/*
use "Input/rawdata_1", clear
append using "Input/rawdata_2", force
save "Input/rawdata", replace

use "Input/pagetimes_1", clear
append using  "Input/pagetimes_2", force
save "Input/pagetimes", replace
*/

// Did not check out session 2 yet -- needs to be done before merge
// Also requires care when merging in pagetimes later on (by session and id, not just id)

//------------------------
//------------------------
//------------------------
//------------------------
// Response data

use "Input/rawdata", clear

// rename main identifying vars
rename participantid_in_session id
rename subsessionround_number page
label variable id "participant id"
label variable page "page id (1-40)"
order session id page
sort session id page

// keep only participants who completed study
keep if participant_index_in_pages==participant_max_page_index

// drop redundant data
drop participantcode participantlabel participant_is_bot participant_index_in_pages participant_max_page_index participant_current_app_name participant_current_page_name
drop participantvisited participantmturk_worker_id participantmturk_assignment_id participantpayoff playerid_in_group playerrole playerpayoff
drop playerisleaving
drop groupid_in_subsession sessioncode sessionlabel sessionmturk_hitid sessionmturk_hitgroupid sessioncomment sessionis_demo

// split into participant vs question level data, forcing question level data to end
order id page participanttime_started_utc playerbrowser_first playerlast_name playerfirst_name playerstudent_number playerdemographics_age playerdemographics_sex playerdemographics_fininterest playerdemographics_investor playerdemographics_investorhisto playerdemographics_investorexper playerdemographics_financeprof playerdemographics_riskaffinity playerdemographics_percentages playerdemographics_intuition playerdemographics_ideasvsfacts playerdemographics_analysisvsins playerinterest_rate_inflation playerbonds_riskier playerhighest_return_asset playerhighest_fluctuations_asset playerrisk_spreading_money playerstock_mutual_fund playerinvest_mutual_fund playermortgage_payment playersavings_interest playermutual_fund_statement playerbond_purchase playercredit_card_debt playerfaith1 playerfaith2 playerfaith3 playerfaith4 playerfaith5 playerfaith6 playerfaith7 playerfaith8 playerfaith9 playerfaith10 playerfaith11 playerfaith12 playeroverconfidence1 playeroverconfidence2 playeroverconfidence3 playerquestion playerexperiment_group

//------------------------
// Fill participant-level variables into all rows
by id (page), sort: replace playerbrowser_first = playerbrowser_first[1]
by id (page), sort: replace playerlast_name = playerlast_name[1]
by id (page), sort: replace playerfirst_name = playerfirst_name[1]
by id (page), sort: replace playerstudent_number = playerstudent_number[1]
by id (page), sort: replace playerdemographics_age = playerdemographics_age[1]
by id (page), sort: replace playerdemographics_sex = playerdemographics_sex[2]
by id (page), sort: replace playerdemographics_fininterest = playerdemographics_fininterest[3]
by id (page), sort: replace playerdemographics_investor = playerdemographics_investor[4]
by id (page), sort: replace playerdemographics_investorhisto = playerdemographics_investorhisto[5]
by id (page), sort: replace playerdemographics_investorexper = playerdemographics_investorexper[6]
by id (page), sort: replace playerdemographics_financeprof = playerdemographics_financeprof[7]
by id (page), sort: replace playerdemographics_riskaffinity = playerdemographics_riskaffinity[8]
by id (page), sort: replace playerdemographics_percentages = playerdemographics_percentages[1]
by id (page), sort: replace playerdemographics_intuition = playerdemographics_intuition[2]
by id (page), sort: replace playerdemographics_ideasvsfacts = playerdemographics_ideasvsfacts[3]
by id (page), sort: replace playerdemographics_analysisvsins = playerdemographics_analysisvsins[4]
by id (page), sort: replace playerinterest_rate_inflation = playerinterest_rate_inflation[1]
by id (page), sort: replace playerbonds_riskier = playerbonds_riskier[2]
by id (page), sort: replace playerhighest_return_asset = playerhighest_return_asset[3]
by id (page), sort: replace playerhighest_fluctuations_asset = playerhighest_fluctuations_asset[4]
by id (page), sort: replace playerrisk_spreading_money = playerrisk_spreading_money[5]
by id (page), sort: replace playerstock_mutual_fund = playerstock_mutual_fund[6]
by id (page), sort: replace playerinvest_mutual_fund = playerinvest_mutual_fund[1]
by id (page), sort: replace playermortgage_payment = playermortgage_payment[2]
by id (page), sort: replace playersavings_interest = playersavings_interest[3]
by id (page), sort: replace playermutual_fund_statement = playermutual_fund_statement[4]
by id (page), sort: replace playerbond_purchase = playerbond_purchase[5]
by id (page), sort: replace playercredit_card_debt = playercredit_card_debt[6]
by id (page), sort: replace playerfaith1 = playerfaith1[1]
by id (page), sort: replace playerfaith2 = playerfaith2[2]
by id (page), sort: replace playerfaith3 = playerfaith3[3]
by id (page), sort: replace playerfaith4 = playerfaith4[4]
by id (page), sort: replace playerfaith5 = playerfaith5[5]
by id (page), sort: replace playerfaith6 = playerfaith6[6]
by id (page), sort: replace playerfaith7 = playerfaith7[1]
by id (page), sort: replace playerfaith8 = playerfaith8[2]
by id (page), sort: replace playerfaith9 = playerfaith9[3]
by id (page), sort: replace playerfaith10 = playerfaith10[4]
by id (page), sort: replace playerfaith11 = playerfaith11[5]
by id (page), sort: replace playerfaith12 = playerfaith12[6]
by id (page), sort: replace playeroverconfidence1 = playeroverconfidence1[1]
by id (page), sort: replace playeroverconfidence2 = playeroverconfidence2[2]
by id (page), sort: replace playeroverconfidence3 = playeroverconfidence3[3]

//------------------------
// Reshuffle responses to questions
by id (page), sort: replace playerdatarows = playerdatarows[1] if playerquestion==26 // move used rows from xlsx to the investment questions
drop if page==1 // drop welcome page
drop if page>=34 // drop survey pages

//------------------------
// Make question number variable and treatment allocation dummy
rename playerquestion question_id
label variable question_id "question identifier"
gen treatment = (playerexperiment_group=="B")
label variable treatment "0 (1) if A (B)"
order id question_id treatment page
sort id question_id treatment page
drop playerexperiment_group

//------------------------
// Generate new identifier and labels for questions
gen experiment_id = . 
gen experiment_label = "-"
label variable experiment_id "experiment identifier"
label variable experiment_label "experiment label"
replace experiment_id = 1 if question_id==0
replace experiment_label = "conjunction fallacy" if question_id==0
replace experiment_id = 2 if question_id==1
replace experiment_label = "gambler's fallacy" if question_id==1
replace experiment_id = 3 if question_id==2
replace experiment_label = "hot hand fallacy" if question_id==2
replace experiment_id = 4 if question_id==3
replace experiment_label = "disposition effect" if question_id==3
replace experiment_id = 5 if question_id==4
replace experiment_label = "base rate fallacy" if question_id==4
replace experiment_id = 6 if question_id==5
replace experiment_label = "illusion of control" if question_id==5
replace experiment_id = 7 if question_id==6
replace experiment_label = "anchoring effect" if question_id==6
replace experiment_id = 8 if question_id==7
replace experiment_label = "hindsight bias" if question_id==7

replace experiment_id = 9 if question_id==8
replace experiment_label = "present bias" if question_id==8
replace experiment_id = 10 if question_id==9
replace experiment_label = "loss aversion" if question_id==9
replace experiment_id = 11 if question_id==10
replace experiment_label = "endowment effect" if question_id==10
replace experiment_id = 12 if question_id==11
replace experiment_label = "decoy effect" if question_id==11
replace experiment_id = 13 if question_id==12
replace experiment_label = "framing effect" if question_id==12
replace experiment_id = 14 if question_id==13
replace experiment_label = "status quo bias" if question_id==13
replace experiment_id = 15 if question_id==14
replace experiment_label = "sunk cost fallacy" if question_id==14
replace experiment_id = 16 if question_id==15
replace experiment_label = "mental accounting" if question_id==15

replace experiment_id = 17 if question_id==16
replace experiment_label = "ultimatum game" if question_id==16
replace experiment_id = 18 if question_id==17
replace experiment_label = "dictator game" if question_id==17
replace experiment_id = 19 if question_id==18
replace experiment_label = "trust/investment game" if question_id==18
replace experiment_id = 20 if question_id==19
replace experiment_label = "public goods game" if question_id==19
replace experiment_id = 21 if question_id==20
replace experiment_label = "prisoner's dilemma" if question_id==20
replace experiment_id = 22 if question_id==21
replace experiment_label = "coordination game" if question_id==21
replace experiment_id = 23 if question_id==22
replace experiment_label = "bertrand/price competition" if question_id==22
replace experiment_id = 24 if question_id==23
replace experiment_label = "cournot/quantity competition" if question_id==23

replace experiment_id = 25 if question_id==24
replace experiment_label = "SSW market" if question_id==24
replace experiment_id = 26 if question_id==25
replace experiment_label = "wisdom of the crowd" if question_id==25

replace experiment_id = 27 if question_id==26 & page==28
replace experiment_label = "counting heuristic 1 (4)" if question_id==26 & page==28
replace experiment_id = 28 if question_id==26 & page==29
replace experiment_label = "counting heuristic 2 (4)" if question_id==26 & page==29
replace experiment_id = 29 if question_id==26 & page==30
replace experiment_label = "counting heuristic 3 (4)" if question_id==26 & page==30
replace experiment_id = 30 if question_id==26 & page==31
replace experiment_label = "counting heuristic 4 (4)" if question_id==26 & page==31

replace experiment_id = 31 if question_id==27 & page==32
replace experiment_label = "deterministic mirror" if question_id==27 & page==32
replace experiment_id = 32 if question_id==27 & page==33
replace experiment_label = "separate vs together" if question_id==27 & page==33

order id experiment_id experiment_label treatment page
sort id experiment_id experiment_label treatment page
drop question_id

//---------------------   
//------------------------
// Rename/generate and label experiment level variables

//---------------------   
// e1: conjunction fallacy
by treatment, sort: sum treatment playerconjunction_bank_teller_a playerconjunction_bank_teller_fe playerconjunction_bank_teller_b v28 if experiment_id==1
// treatment 0: A <-> probability between 0 and 100
// treatment 1: B <-> frequency out of 1000 between 0 and 1000
gen e1_bankteller = playerconjunction_bank_teller_a/100
replace e1_bankteller = playerconjunction_bank_teller_b/1000 if e1_bankteller==.
gen e1_feministbankteller = playerconjunction_bank_teller_fe/100
replace e1_feministbankteller = v28/1000 if e1_feministbankteller==.
label variable e1_bankteller "Probability for bank teller"
label variable e1_feministbankteller "Probability for bank teller & active in feminist movement"
bro id experiment_id experiment_label treatment page playerconjunction_bank_teller_a playerconjunction_bank_teller_fe playerconjunction_bank_teller_b v28 e1_bankteller e1_feministbankteller if experiment_id==1
drop playerconjunction_bank_teller_a playerconjunction_bank_teller_fe playerconjunction_bank_teller_b v28
// check results
sum treatment e1_bankteller e1_feministbankteller if experiment_id==1
count if e1_feministbankteller>e1_bankteller & experiment_id==1 // logically impossible
count if e1_feministbankteller==e1_bankteller & experiment_id==1 // unlikely (all feminists)
count if e1_feministbankteller<e1_bankteller & experiment_id==1 // should be 100
reg e1_feministbankteller treatment if experiment_id==1
reg e1_bankteller treatment if experiment_id==1
// --> lower likelihood if treatment==1 <-> if we ask for a frequency out of 1000 instead of a probability out of 100

// Idea for next experiment: 
// Make between-subject design, that should increase the frequency of logically wrong responses...
// ==> Ask for bank teller if treatment==0 and feminist bank teller if treatment==1
// That way we do not have the probability vs frequency variation anymore, but that is not the main point anyhow (was just an idea because we wanted some between-subject variation)

//---------------------   
// e2: gambler's fallacy
by treatment, sort: sum treatment playergambler_heads_a playergambler_tails_a playergambler_heads_b playergambler_tails_b if experiment_id==2
// treatment 0: A <-> (H,H,H,H,H,H)
// treatment 1: B <-> (H,T,H,T,H,T)
gen e2_heads = playergambler_heads_a/100
replace e2_heads = playergambler_heads_b/100 if e2_heads==.
gen e2_tails = playergambler_tails_a/100
replace e2_tails = playergambler_tails_b/100 if e2_tails==.
label variable e2_heads "Probability for heads"
label variable e2_tails "Probability for tails"
bro id experiment_id experiment_label treatment page playergambler_heads_a playergambler_tails_a playergambler_heads_b playergambler_tails_b e2_heads e2_tails if experiment_id==2
drop playergambler_heads_a playergambler_tails_a playergambler_heads_b playergambler_tails_b
// check results
sum treatment e2_heads e2_tails if experiment_id==2
count if (e2_heads!=0.5 | e2_tails!=0.5) & experiment_id==2 // participants believing in unfair coin
gen temp_edge = e2_heads-e2_tails
reg temp_edge treatment if experiment_id==2
// --> nothing significant and plausibly both typos (one off or missing zero)

// Idea for next experiment: 
// Instead of presenting the sequence of flips as a description on one screen, we can have participants "flip" sequentially, varying the sequence between subject...
// ==> Same allocation between-subject as before, but... 
// - for the non-alternating sequence we could maybe even randomize whether it is all H or all T for each subject?
// - for the alternating sequence we could maybe even randomize the order of a representative sample (3xH and 3xT) for each subject?
// That way, I there might be stronger treatment effects, because the sequential drawing is more activating. But also check how this was done in the original studies... 
// Independently: We could strike out the "fair". That means it is not irrational to assume the coin is unfair, but a reasonable prior is still 50/50, and Bayesian updating based on merely 6 draws should not move beliefs much (need to calculate!)

//---------------------   
// e3: hot hand fallacy
by treatment, sort: sum treatment playerhothand_a playerhothand_b if experiment_id==3
// treatment 0: A <-> probability to make next shot (0-100)
// treatment 1: B <-> frequency to make next shot (0-100)
gen e3_makeshot = playerhothand_a/100
replace e3_makeshot = playerhothand_b/100 if e3_makeshot==.
label variable e3_makeshot "Probability to make next shot after streak of 5"
bro id experiment_id experiment_label treatment page playerhothand_a playerhothand_b e3_makeshot if experiment_id==3
drop playerhothand_a playerhothand_b
// check results
sum treatment e3_makeshot if experiment_id==3
reg e3_makeshot treatment if experiment_id==3
// --> nothing significant yet, but wide confidence interval...

// Idea for next experiment: This does not really test whether people are extrapolating too much because there is no objective benchmark without data
// --> check existing studies to find out how to do this better! Probably just comparison with actual data, but can something be done to generate irrational beliefs without the need to compare to outside data? 

//---------------------   
// e4: disposition effect
by treatment, sort: sum treatment playerdisposition_a playerdisposition_b if experiment_id==4
// treatment 0: A <-> Which stock do you sell? [A is winner with 100% return to $100, B is loser with -50% return to $100]
// treatment 1: B <-> Which stock do you keep? [A is winner with 100% return to $100, B is loser with -50% return to $100]
gen e4_sellwinner = 1 if experiment_id==4 & ((playerdisposition_a=="Stock A")|(playerdisposition_b=="Stock B"))
replace e4_sellwinner = 0 if experiment_id==4 & ((playerdisposition_a=="Stock B")|(playerdisposition_b=="Stock A"))
label variable e4_sellwinner "Sells winner"
bro id experiment_id experiment_label treatment page playerdisposition_a playerdisposition_b e4_sellwinner if experiment_id==4
drop playerdisposition_a playerdisposition_b
// check results
sum treatment e4_sellwinner if experiment_id==4 
reg e4_sellwinner treatment if experiment_id==4 
// --> a reverse disposition effect that is highly significant when we ask for which stock to "sell", but gone when asking for which stock to "keep"
ttest e4_sellwinner==0.5 if experiment_id==4 & treatment==0
ttest e4_sellwinner==0.5 if experiment_id==4 & treatment==1

// Idea for next experiment: I think this is interesting. Think about it and maybe keep it. Relation to classical DE experiments? 

//---------------------   
// e5: base rate fallacy
by treatment, sort: sum treatment playerbaserate_a playerbaserate_b if experiment_id==5
// treatment 0: A <-> probability (0-100)
// treatment 1: B <-> frequency (0-1000)
gen e5_pcorrect = playerbaserate_a/100 if experiment_id==5
replace e5_pcorrect = playerbaserate_b/1000 if experiment_id==5 & e5_pcorrect==.
label variable e5_pcorrect "Probability actually blue"
bro id experiment_id experiment_label treatment page playerbaserate_a playerbaserate_b e5_pcorrect if experiment_id==5
drop playerbaserate_a playerbaserate_b
// check results: Note that the correct p(blue|identified as blue) = 80%*15%/(80%*15%+20%*85%) = 41.4% [another common response for participants who went through the calculations would be 15%/(80%*15%+20%*85%)=51.7%]
sum treatment e5_pcorrect if experiment_id==5 
reg e5_pcorrect treatment if experiment_id==5 
// --> pretty good on average in the A group with probabilities (41.9%), but a bit underestimated in the B group (around 33%)--i.e., against the general pattern--although that's stat. insig.
ttest e5_pcorrect==0.414 if experiment_id==5 & treatment==0
ttest e5_pcorrect==0.414 if experiment_id==5 & treatment==1

// Idea for next experiment: 
// - Need to check screenshots from actual experiment; what we have in docx is super-confusing for B, might be fixed in actual oTree implementation?
// - Think alternative B versions?

//---------------------   
// e6: illusion of control


// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
// TEMP: List of variables for each experiment that need to be transformed and labeled like above
// - check word file with screenshots to identify treatments, 
// - rescale to make comparable between treatment groups if necessary
// -> Then delete the list below


// e6: illusion of control

// same scale
// playerillusioncontrol_a ["Pick my own numbers", "Let the system choose", "Either"]
// playerillusioncontrol_b ["Number picking group", "Random number group", "Either"]
// treatment 0: A <-> Which option do you choose? 
// treatment 1: B <-> Which group is the winner most likely in? 

by treatment, sort: sum treatment playerillusioncontrol_a playerillusioncontrol_b if experiment_id==6

// same conceptual scale: preference for control
gen e6_control = .
replace e6_control = 1 if experiment_id==6 & ///
    (playerillusioncontrol_a=="Pick my own numbers" | playerillusioncontrol_b=="Number picking group")
replace e6_control = 0 if experiment_id==6 & ///
    (playerillusioncontrol_a=="Let the system choose" | playerillusioncontrol_b=="Random number group")

label variable e6_control "Prefers control over randomness"
bro id treatment playerillusioncontrol_a playerillusioncontrol_b e6_control if experiment_id==6
drop playerillusioncontrol_a playerillusioncontrol_b


// e7: anchoring bias

// same scale
// playerhindsight [0-500]
// treatment 0: A <-> median 30yo Swiss spruce tree height estimate with example (anchor) given 100 meters
// treatment 1: B <-> median 30yo Swiss spruce tree height estimate with example (anchor) given 10 meters

by treatment, sort: sum treatment playeranchoring_a playeranchoring_b if experiment_id==7

gen e7_height = playeranchoring_a
replace e7_height = playeranchoring_b if e7_height==.

label variable e7_height "Estimated height of Swiss spruce (meters)"
bro id treatment playeranchoring_a playeranchoring_b e7_height if experiment_id==7
drop playeranchoring_a playeranchoring_b


// e8: hindsight bias

// same scale
// playerhindsight [0-100]
// treatment 0: A <-> How likely do you think that the company will succeed in %
// treatment 1: B <-> How likely do you think it was that the company would success in %

by treatment, sort: sum treatment playerhindsight_a playerhindsight_b if experiment_id==8

gen e8_successprob = playerhindsight_a/100
replace e8_successprob = playerhindsight_b/100 if e8_successprob==.

label variable e8_successprob "Perceived probability of company success"
bro id treatment playerhindsight_a playerhindsight_b e8_successprob if experiment_id==8
drop playerhindsight_a playerhindsight_b


// e9: present bias
// playerpresentbias_a playerpresentbias_b

// same scale
// playerpresentbias_a ["$20 now", "$50 in 1 month"]
// playerpresentbias_b ["$20 in 12 months", "$50 in 13 month"]
// treatment 0: A <->
// treatment 1: B <->

by treatment, sort: sum treatment playerpresentbias_a playerpresentbias_b if experiment_id==9

gen e9_immediate = .
replace e9_immediate = 1 if experiment_id==9 & ///
    (playerpresentbias_a=="$20 now" | playerpresentbias_b=="$20 in 12 months")
replace e9_immediate = 0 if experiment_id==9 & ///
    (playerpresentbias_a=="$50 in 1 month" | playerpresentbias_b=="$50 in 13 month")

label variable e9_immediate "Chooses earlier smaller reward"
bro id treatment playerpresentbias_a playerpresentbias_b e9_immediate if experiment_id==9
drop playerpresentbias_a playerpresentbias_b


// e10: loss aversion
//playerlossaversion_a playerlossaversion_b

// same scale
// playerlossaversion_a ["A sure gain of €500", "A 50% chance to gain another €1000, a 50% chance to gain €0"]
// playerlossaversion_b ["A sure loss of €500", "A 50% chance to lose €0, a 50% chance to lose €1000"]
// treatment 0: A <-> Given that you have €1000, what would you prefer
// treatment 1: B <-> Given that you have €2000, what would you prefer

by treatment, sort: sum treatment playerlossaversion_a playerlossaversion_b if experiment_id==10

gen e10_safe = .
replace e10_safe = 1 if experiment_id==10 & ///
    (playerlossaversion_a=="A sure gain of €500" | playerlossaversion_b=="A sure loss of €500")
replace e10_safe = 0 if experiment_id==10 & ///
    (playerlossaversion_a!="A sure gain of €500" & playerlossaversion_b!="A sure loss of €500")

label variable e10_safe "Chooses sure option"
bro id treatment playerlossaversion_a playerlossaversion_b e10_safe if experiment_id==10
drop playerlossaversion_a playerlossaversion_b


// e11: endowment effect
// playerendowment_a playerendowment_b

// same scale
// treatment 0: A <-> How much would you sell this mug given to you as a gift?
// treatment 1: B <-> How much would you pay for this mug?

by treatment, sort: sum treatment playerendowment_a playerendowment_b if experiment_id==11

gen e11_value = playerendowment_a
replace e11_value = playerendowment_b if e11_value==.

label variable e11_value "Valuation of mug (EUR)"
bro id treatment playerendowment_a playerendowment_b e11_value if experiment_id==11
drop playerendowment_a playerendowment_b


// e12: decoy effect
// playerdecoy_a playerdecoy_b

// same scale
// playerdecoy_a ["€10 for 1GB data", "€14 for 1.5GB data", "€15 for 2GB data"]
// playerdecoy_b ["€10 for 1GB data", "€15 for 2GB data"]
// treatment 0: A <-> Which data plan would you pick? 
// treatment 1: B <-> Which data plan would you pick?

by treatment, sort: sum treatment playerdecoy_a playerdecoy_b if experiment_id==12

gen e12_target = .
replace e12_target = 1 if experiment_id==12 & ///
    (playerdecoy_a=="€15 for 2GB data" | playerdecoy_b=="€15 for 2GB data")
replace e12_target = 0 if experiment_id==12 & e12_target==.

label variable e12_target "Chooses target option"
bro id treatment playerdecoy_a playerdecoy_b e12_target if experiment_id==12
drop playerdecoy_a playerdecoy_b


// e13: framing effect
// playerframing_a playerframing_b

// same scale
// playerframing ["Program A", "Program B"]
// treatment 0: A <-> Choose a health program. [a. 200 people will be helped, b. 1/3 chance that all 600 will be helped, 2/3 chance that no one will be helped]
// treatment 1: B <-> Choose a health program. [a. 400 people will not be helped, b. 2/3 chance that all 600 will not helped, 1/3 chance that everyone will be helped]

by treatment, sort: sum treatment playerframing_a playerframing_b if experiment_id==13

gen e13_safe = .
replace e13_safe = 1 if experiment_id==13 & ///
    (playerframing_a=="Program A" | playerframing_b=="Program A")
replace e13_safe = 0 if experiment_id==13 & ///
    (playerframing_a=="Program B" | playerframing_b=="Program B")

label variable e13_safe "Chooses certain option"
bro id treatment playerframing_a playerframing_b e13_safe if experiment_id==13
drop playerframing_a playerframing_b


// e14: status quo bias
// playerstatusquo_a playerstatusquo_b

// same scale
// playerstatusquo_a ["Stay with A", "Switch to B"]
// playerstatusquo_b ["Stay with B", "Switch to A"]
// We only care about whether or not the participants choose to stay or switch, not the actual plan.
// treatment 0: A <-> a. Stay with plan A or b. switch to B will slightly higher coverage and higher cost.
// treatment 1: B <-> a. Stay with B or b. switch to A with slightly lower coverage.

by treatment, sort: sum treatment playerstatusquo_a playerstatusquo_b if experiment_id==14

gen e14_stay = .
replace e14_stay = 1 if experiment_id==14 & ///
    (playerstatusquo_a=="Stay with A" | playerstatusquo_b=="Stay with B")
replace e14_stay = 0 if experiment_id==14 & ///
    (playerstatusquo_a=="Switch to B" | playerstatusquo_b=="Switch to A")

label variable e14_stay "Stays with default option"
bro id treatment playerstatusquo_a playerstatusquo_b e14_stay if experiment_id==14
drop playerstatusquo_a playerstatusquo_b


// e15: sunk cost fallacy
// playersunkcost_a playersunkcost_b

// same scale
// playersunkcost ["Stay and eat more", "Leave"]
// treatment 0: A <-> You paid to eat at a buffet. After 20 minutes you are full, do you ...
// treatment 1: B <-> You are given a free voucher to eat at a buffet. After 20 minutes you are full, do you ...

by treatment, sort: sum treatment playersunkcost_a playersunkcost_b if experiment_id==15

gen e15_sunk = .
replace e15_sunk = 1 if experiment_id==15 & ///
    (playersunkcost_a=="Stay and eat more" | playersunkcost_b=="Stay and eat more")
replace e15_sunk = 0 if experiment_id==15 & ///
    (playersunkcost_a=="Leave" | playersunkcost_b=="Leave")

label variable e15_sunk "Continues due to sunk cost"
bro id treatment playersunkcost_a playersunkcost_b e15_sunk if experiment_id==15
drop playersunkcost_a playersunkcost_b


// e16: mental accounting
// playermentalaccounting_a playermentalaccounting_b

// same scale
// playermentalaccounting ["Yes","No"]
// treatment 0: A <-> You have a movie ticket for a movie but lost it. Do you buy another? a. yes, b. no
// treatment 1: B <-> You have put aside money to buy a ticket but lost the money. Do you still buy the ticket? a. yes, b. no

by treatment, sort: sum treatment playermentalaccounting_a playermentalaccounting_b if experiment_id==16

gen e16_buy = .
replace e16_buy = 1 if experiment_id==16 & ///
    (playermentalaccounting_a=="Yes" | playermentalaccounting_b=="Yes")
replace e16_buy = 0 if experiment_id==16 & ///
    (playermentalaccounting_a=="No" | playermentalaccounting_b=="No")

label variable e16_buy "Buys ticket again"
bro id treatment playermentalaccounting_a playermentalaccounting_b e16_buy if experiment_id==16
drop playermentalaccounting_a playermentalaccounting_b


// e17: ultimatum game
// playerultimatum_offer_a playerultimatum_accept_a // playerultimatum_offer_b playerultimatum_accept_b

// same scale
// playerultimatum_offer "how much do you offer" [€0 - €10]
// playerultimatum_accept "how much do you accept"[€0 - €10]
// treatment 0: A <-> The other is a stranger 
// treatment 1: B <-> The other is a close friend 

gen e17_offer = playerultimatum_offer_a
replace e17_offer = playerultimatum_offer_b if e17_offer==.
gen e17_accept = playerultimatum_accept_a
replace e17_accept = playerultimatum_accept_b if e17_accept==.

label variable e17_offer "Ultimatum offer (EUR)"
label variable e17_accept "Minimum acceptable offer (EUR)"
drop playerultimatum_offer_a playerultimatum_offer_b playerultimatum_accept_a playerultimatum_accept_b


// e18: dictator game
// playerdictator_amount_a playerdictator_amount_b

// same scale
// playerdictator_amount "how much do you offer" [€0 - €10]
// treatment 0: A <-> The other is a stranger 
// treatment 1: B <-> The other is a family member

by treatment, sort: sum treatment ///
    playerdictator_amount_a playerdictator_amount_b ///
    if experiment_id==18

gen e18_dictator = playerdictator_amount_a
replace e18_dictator = playerdictator_amount_b if e18_dictator==.

label variable e18_dictator "Dictator transfer (€0–€10)"

bro id treatment ///
    playerdictator_amount_a playerdictator_amount_b ///
    e18_dictator if experiment_id==18

drop playerdictator_amount_a playerdictator_amount_b



// e19: trust game
// playertrust_send_a playertrust_send_b playertrust_return_3_a playertrust_return_3_b playertrust_return_6_a playertrust_return_6_b playertrust_return_9_a playertrust_return_9_b playertrust_return_12_a playertrust_return_12_b playertrust_return_15_a playertrust_return_15_b playertrust_return_18_a playertrust_return_18_b playertrust_return_21_a playertrust_return_21_b playertrust_return_24_a playertrust_return_24_b playertrust_return_27_a playertrust_return_27_b playertrust_return_30_a playertrust_return_30_b

// same scale
// playertrust_send "how much do you send" [€0 - €10]
// playertrust_return_3 "How much do you return if receiving 3" [€0 - €3]
// playertrust_return_6 "How much do you return if receiving 6" [€0 - €6]
// etc ...
// playertrust_return_30 "How much do you return if receiving 6" [€0 - €30]
// treatment 0: A <-> The other is a stranger 
// treatment 1: B <-> The other is a family member 

by treatment, sort: sum treatment ///
    playertrust_send_a playertrust_send_b ///
    if experiment_id==19

gen e19_send = playertrust_send_a
replace e19_send = playertrust_send_b if e19_send==.

label variable e19_send "Trust game: amount sent (€0–€10)"

bro id treatment ///
    playertrust_send_a playertrust_send_b ///
    e19_send if experiment_id==19

foreach x in 3 6 9 12 15 18 21 24 27 30 {
    gen e19_return_`x' = playertrust_return_`x'_a
    replace e19_return_`x' = playertrust_return_`x'_b if e19_return_`x'==.
    label variable e19_return_`x' ///
        "Trust game: return if received `x' (€0–€`x')"
}

drop playertrust_send_a playertrust_send_b ///
     playertrust_return_*_a playertrust_return_*_b



// e20: public goods game
// playerpublic_goods_contrib_a playerpublic_goods_contrib_b

// same scale
// playerpublic_goods_contrib "how much do you contribute" [€0 - €10] 
// treatment 0: A <-> The others are strangers 
// treatment 1: B <-> The others are close friends

by treatment, sort: sum treatment ///
    playerpublic_goods_contrib_a playerpublic_goods_contrib_b ///
    if experiment_id==20

gen e20_contribution = playerpublic_goods_contrib_a
replace e20_contribution = playerpublic_goods_contrib_b if e20_contribution==.

label variable e20_contribution ///
    "Public goods contribution (€0–€10)"

bro id treatment ///
    playerpublic_goods_contrib_a playerpublic_goods_contrib_b ///
    e20_contribution if experiment_id==20

drop playerpublic_goods_contrib_a playerpublic_goods_contrib_b



// e21: prisoners dilemma
// playerprisoner_choice_a playerprisoner_choice_b

// same scale
// playerprisoner_choice ["Cooperate", "Defect"] "Cooperate or defect"
// treatment 0: A <-> stranger
// treatment 1: B <-> family member

by treatment, sort: sum treatment ///
    playerprisoner_choice_a playerprisoner_choice_b ///
    if experiment_id==21

gen e21_cooperate = .
replace e21_cooperate = 1 if experiment_id==21 & ///
    (playerprisoner_choice_a=="Cooperate" | playerprisoner_choice_b=="Cooperate")
replace e21_cooperate = 0 if experiment_id==21 & ///
    (playerprisoner_choice_a=="Defect" | playerprisoner_choice_b=="Defect")

label variable e21_cooperate "Cooperates (1) vs defects (0)"

bro id treatment ///
    playerprisoner_choice_a playerprisoner_choice_b ///
    e21_cooperate if experiment_id==21

drop playerprisoner_choice_a playerprisoner_choice_b



// e22: coordination game
// playercoord_restaurant_choice_a playercoord_other_likelihood_a playercoord_restaurant_choice_b playercoord_other_likelihood_b

// same scale
// playercoord_restaurant_choice ["Täffä","Nanapo Sushi"] "Choice of restaurant"
// playercoord_other_likelihood [0-100] "Likelihood of the other player choosing the same restaurant"
// treatment 0: A <-> stranger
// treatment 1: B <-> close friend

by treatment, sort: sum treatment ///
    playercoord_restaurant_choice_a playercoord_other_likelihood_a ///
    playercoord_restaurant_choice_b playercoord_other_likelihood_b ///
    if experiment_id==22

gen e22_choice = playercoord_restaurant_choice_a
replace e22_choice = playercoord_restaurant_choice_b if e22_choice==""

gen e22_belief = playercoord_other_likelihood_a/100
replace e22_belief = playercoord_other_likelihood_b/100 if e22_belief==.

label variable e22_choice "Chosen restaurant"
label variable e22_belief "Belief other chooses same restaurant (0–1)"

bro id treatment ///
    playercoord_restaurant_choice_a playercoord_other_likelihood_a ///
    playercoord_restaurant_choice_b playercoord_other_likelihood_b ///
    e22_choice e22_belief if experiment_id==22

drop playercoord_restaurant_choice_a playercoord_restaurant_choice_b ///
     playercoord_other_likelihood_a playercoord_other_likelihood_b


// e23: bertrand/price
// playerbertrand_price_a playerbertrand_price_b

// same scale
// playerbertrand_price [1-10] "The price to set"
// treatment 0: A <-> stranger
// treatment 1: B <-> close friend

by treatment, sort: sum treatment ///
    playerbertrand_price_a playerbertrand_price_b ///
    if experiment_id==23

gen e23_price = playerbertrand_price_a
replace e23_price = playerbertrand_price_b if e23_price==.

label variable e23_price "Bertrand price (€1–€10)"

bro id treatment ///
    playerbertrand_price_a playerbertrand_price_b ///
    e23_price if experiment_id==23

drop playerbertrand_price_a playerbertrand_price_b


// e24: cournot/quantity
// playercournot_quantity_a playercournot_quantity_b

// same scale
// playercournot_quantity [0-10] "Units to produce"
// treatment 0: A <-> stranger
// treatment 1: B <-> close friend

by treatment, sort: sum treatment ///
    playercournot_quantity_a playercournot_quantity_b ///
    if experiment_id==24

gen e24_quantity = playercournot_quantity_a
replace e24_quantity = playercournot_quantity_b if e24_quantity==.

label variable e24_quantity "Cournot quantity (0–10 units)"

bro id treatment ///
    playercournot_quantity_a playercournot_quantity_b ///
    e24_quantity if experiment_id==24

drop playercournot_quantity_a playercournot_quantity_b


// e25: SSW
//playerssw_wtp_0_a playerssw_wta_0_a playerssw_wtp_0_b playerssw_wta_0_b playerssw_wtp_1_a playerssw_wtp_1_b playerssw_wta_1_a playerssw_wta_1_b playerssw_wtp_2_a playerssw_wtp_2_b playerssw_wta_2_a playerssw_wta_2_b playerssw_wtp_3_a playerssw_wtp_3_b playerssw_wta_3_a playerssw_wta_3_b playerssw_wtp_4_a playerssw_wtp_4_b playerssw_wta_4_a playerssw_wta_4_b playerssw_wtp_5_a playerssw_wtp_5_b playerssw_wta_5_a playerssw_wta_5_b playerssw_wtp_6_a playerssw_wtp_6_b playerssw_wta_6_a playerssw_wta_6_b playerssw_wtp_7_a playerssw_wtp_7_b playerssw_wta_7_a playerssw_wta_7_b playerssw_wtp_8_a playerssw_wtp_8_b playerssw_wta_8_a playerssw_wta_8_b playerssw_wtp_9_a playerssw_wtp_9_b playerssw_wta_9_a playerssw_wta_9_b playerssw_wtp_10_a playerssw_wtp_10_b playerssw_wta_10_a playerssw_wta_10_b playerssw_wtp_11_a playerssw_wtp_11_b playerssw_wta_11_a playerssw_wta_11_b

// same scale
// all variables [0 - 11*11.85]
// playerssw_wtp_i "WTP at period i"
// playerssw_wta_i "WTA at period i"
// treatment 0: A <-> stranger
// treatment 1: B <-> close friend

forvalues i=0/11 {
    gen e25_wtp_`i' = playerssw_wtp_`i'_a
    replace e25_wtp_`i' = playerssw_wtp_`i'_b if e25_wtp_`i'==.
    gen e25_wta_`i' = playerssw_wta_`i'_a
    replace e25_wta_`i' = playerssw_wta_`i'_b if e25_wta_`i'==.
    label variable e25_wtp_`i' "WTP period `i'"
    label variable e25_wta_`i' "WTA period `i'"
}
drop playerssw_wtp_* playerssw_wta_*


// e26: wisdom of the crowd
// playerwisdom_michael_a playerwisdom_daniel_a playerwisdom_christoph_a playerwisdom_michael_b playerwisdom_daniel_b playerwisdom_christoph_b

// same scale
// all variables [130 - 220]
// playerwisdom_michael "The guessed height of Michael"
// playerwisdom_daniel "The guessed height of Daniel"
// playerwisdom_christoph "The guessed height of Christoph"
// treatment 0: A <-> with no suggestion
// treatment 1: B <-> with optional suggestions


foreach p in michael daniel christoph {
    gen e26_`p' = playerwisdom_`p'_a
    replace e26_`p' = playerwisdom_`p'_b if e26_`p'==.
    label variable e26_`p' "Guessed height of `p'"
}
drop playerwisdom_*

//---
// Note on counting heuristic rounds: 
// - playerdatarows identifies the rows from rCum_distributions_new.xlsx where the returns for that participant come from
// - these rows need to be imported from the xlsx and merged into the data for each of the rounds
// - then, we need to infer treatments and calculate average returns (benchmark for beliefs)
// -- How often did Asset B outperform Asset A (based on annual returns) <-> Half of participants see annual returns and beliefs/choices should be driven by which asset outperformed frequently
// -- How often did Asset B lead Asset A (based on cumulative returns) <-> Half of participants see cumulative returns and beliefs/choices should be driven by which asset led frequently
// -- Which asset was ahead at the end of the decade (<-> had the higher (geo)mean return)
// -- Which asset had the higher average return (<-> should coincide with the last one) --> relevant to evaluate beliefs

// e27 to e30 use the same variable for both treatment groups
// e27: counting heuristic
// playerdatarows playercognitivelimitinvestment_1 playercognitivelimitinvestmentop 

// playercognitivelimitinvestment_1 "Which asset do you choose to invest in" ["Asset A", "Asset B"]
// playercognitivelimitinvestmentop  "Which asset do you expect to have higher expected return" ["Asset A", "Asset B", "Same Expected Return"]

// treatment 0: A <-> Annual return chart
// treatment 1: B <-> Culmulative return chart

// e28: counting heuristic
// playerdatarows playercognitivelimitinvestment_2 v136 

// playercognitivelimitinvestment_1 "Which asset do you choose to invest in" ["Asset A", "Asset B"]
// v136  "Which asset do you expect to have higher expected return" ["Asset A", "Asset B", "Same Expected Return"]

// treatment 0: A <-> Annual return chart
// treatment 1: B <-> Culmulative return chart

// e29: counting heuristic
// playerdatarows playercognitivelimitinvestment_3 v138 

// playercognitivelimitinvestment_1 "Which asset do you choose to invest in" ["Asset A", "Asset B"]
// v138  "Which asset do you expect to have higher expected return" ["Asset A", "Asset B", "Same Expected Return"]

// treatment 0: A <-> Annual return chart
// treatment 1: B <-> Culmulative return chart

// e30: counting heuristic
// playerdatarows playercognitivelimitinvestment_4 v140

// playercognitivelimitinvestment_1 "Which asset do you choose to invest in" ["Asset A", "Asset B"]
// v140  "Which asset do you expect to have higher expected return" ["Asset A", "Asset B", "Same Expected Return"]

// treatment 0: A <-> Annual return chart
// treatment 1: B <-> Culmulative return chart

* Remove brackets
gen str temp = substr(playerdatarows,2,length(playerdatarows)-2)

* Split into separate elements
split temp, parse(",")  // creates temp1 temp2 temp3 temp4

* Match question to correct column
gen row_to_use = .
replace row_to_use = real(temp1) if experiment_id==27
replace row_to_use = real(temp2) if experiment_id==28
replace row_to_use = real(temp3) if experiment_id==29
replace row_to_use = real(temp4) if experiment_id==30

// BUGFIX: row_to_use is only defined (non-missing) for experiment_id 27-30.
// A plain `merge` + `keep if _merge==3` on the whole dataset would drop every
// row where row_to_use is missing -- i.e. ALL other experiments (1-26,31,32)
// -- because Stata's merge treats missing keys as non-matching. So we split
// off just the rows that need the returns_summary merge, merge those, and
// append everything else back untouched.
preserve
    keep if experiment_id==27 | experiment_id==28 | experiment_id==29 | experiment_id==30
    merge m:1 row_to_use using "Input/returns_summary.dta"
    keep if _merge==3
    drop _merge
    tempfile counting_heuristic_merged
    save `counting_heuristic_merged'
restore
drop if experiment_id==27 | experiment_id==28 | experiment_id==29 | experiment_id==30
append using `counting_heuristic_merged'
drop temp temp1 temp2 temp3 temp4 row_to_use
// append puts the counting-heuristic rows at the end; restore the usual row order
sort id experiment_id experiment_label treatment page

// e27
gen e27_choice = playercognitivelimitinvestment_1
gen e27_belief = playercognitivelimitinvestmentop
label variable e27_choice "Chosen asset (round 1)"
label variable e27_belief "Belief: higher expected return (round 1)"

// e28
gen e28_choice = playercognitivelimitinvestment_2
gen e28_belief = v136
label variable e28_choice "Chosen asset (round 2)"
label variable e28_belief "Belief: higher expected return (round 2)"

// e29
gen e29_choice = playercognitivelimitinvestment_3
gen e29_belief = v138
label variable e29_choice "Chosen asset (round 3)"
label variable e29_belief "Belief: higher expected return (round 3)"

// e30
gen e30_choice = playercognitivelimitinvestment_4
gen e30_belief = v140
label variable e30_choice "Chosen asset (round 4)"
label variable e30_belief "Belief: higher expected return (round 4)"



//---

// e31: deterministic mirror 
// playercognitivelimitbox_1_a playercognitivelimitbox_1_b playercognitivelimitbox_2 playercognitivelimitbox_3 playercognitivelimitbox_4 playercognitivelimitbox_5 playercognitivelimitbox_6 playercognitivelimitbox_7 playercognitivelimitbox_8 playercognitivelimitbox_9 playercognitivelimitbox_10 playercognitivelimitbox_11 playercognitivelimitbox_12 playercognitivelimitbox_13 playercognitivelimitbox_14 playercognitivelimitbox_15 playercognitivelimitbox_16 playercognitivelimitbox_17 playercognitivelimitbox_18 playercognitivelimitbox_19 playercognitivelimitbox_20 playercognitivelimitbox_21

// all variables ["A","B"]
// playercognitivelimitbox_i "Which box do you choose for scenario i"
// For scenario 1, there are 1 variable for each treatment group, this is to help with displaying the main question. For other scenario, there is only one variable.
// treatment 0: A <-> Randomly choose B
// treatment 1: B <-> Average of Bs


gen e31_box1 = playercognitivelimitbox_1_a
replace e31_box1 = playercognitivelimitbox_1_b if e31_box1==""

label variable e31_box1 "Chosen box scenario 1"

// e32: separate vs together 
//playercognitivelimitinsurance

// playercognitivelimitinsurance "Which insurance plan will you choose"
// treatment 0: A <-> Multipage display
// treatment 1: B <-> All in one page display

gen e32_insurance = playercognitivelimitinsurance
label variable e32_insurance "Chosen insurance plan"


//------------------------
// Rename and label participant level variables 
// participanttime_started_utc playerbrowser_first 
// playerlast_name playerfirst_name playerstudent_number 
// playerdemographics_age playerdemographics_sex playerdemographics_fininterest playerdemographics_investor playerdemographics_investorhisto playerdemographics_investorexper playerdemographics_financeprof playerdemographics_riskaffinity  playerdemographics_percentages playerdemographics_intuition playerdemographics_ideasvsfacts playerdemographics_analysisvsins 

// Aggregate measures (financial literacy, faith in intuition, overconfidence)
//playerinterest_rate_inflation playerbonds_riskier playerhighest_return_asset playerhighest_fluctuations_asset playerrisk_spreading_money playerstock_mutual_fund playerinvest_mutual_fund playermortgage_payment playersavings_interest playermutual_fund_statement playerbond_purchase playercredit_card_debt 
// playerfaith1 playerfaith2 playerfaith3 playerfaith4 playerfaith5 playerfaith6 playerfaith7 playerfaith8 playerfaith9 playerfaith10 playerfaith11 playerfaith12 
// playeroverconfidence1 playeroverconfidence2 playeroverconfidence3

// Drop redundant variables

// save
save "Output/responses", replace

//------------------------
//------------------------
//------------------------
//------------------------
// Viewing times for the total study and subsections

//------------------------
use "Input/pagetimes", clear
drop if app_name==""

// rename main identifying vars
rename participant_id_in_session id
rename round_number page
order session page_index page
sort session id page_index page

// drop redundant data
drop session_code participant_code timeout_happened is_wait_page

// keep only participants who completed the experiment
by session id (page_index page), sort: egen page_max = max(page)
sum page_max
keep if page_max==40
drop page_max

// calculate time per page and total viewing time
by session id (page_index page), sort: gen page_viewingtime = epoch_time_completed[_n]-epoch_time_completed[_n-1] if _n>1
by session id (page_index page), sort: egen total_viewingtime = total(page_viewingtime)
replace total_viewingtime = total_viewingtime/60

// drop redundant data
drop page_index app_name epoch_time_completed

// label and save full viewing time dataset
label variable id "participant id"
label variable page "page id (1-40)"
label variable page_name "page name"
label variable page_viewingtime "page viewing time (seconds)"
label variable total_viewingtime "total viewing time (minutes)"

save "Output/viewingtimes_full", replace
by page, sort: sum page_viewingtime
sum total_viewingtime, det

//------------------------
use  "Output/viewingtimes_full", clear

// participant level data
drop page page_name page_viewingtime
duplicates drop
sort id
duplicates report id

// save
save "Output/viewingtimes_participantlevel", replace

//------------------------
use  "Output/viewingtimes_full", clear

// participant x page level data
drop total_viewingtime
duplicates drop
sort id
duplicates report id

// save
save "Output/viewingtimes_pagelevel", replace

//------------------------
//------------------------
//------------------------
//------------------------
// Merge data -- Full data non-anonymized

use "Output/responses", clear

// get viewing time for whole study
merge m:1 id using "Output/viewingtimes_participantlevel", keepusing(total_viewingtime)
drop if _merge==2
drop _merge

// get viewing time for each page
merge 1:1 id page using "Output/viewingtimes_pagelevel", keepusing(page page_name page_viewingtime)
drop if _merge==2
drop _merge

// save
save "Output/mergeddata_full", replace

//------------------------
//------------------------
// Anonymized dataset

use  "Output/mergeddata_full", clear

// drop identifying information name x2 and student number

// make some variables more coarse to avoid identification via demographics age...

// save
save "Output/mergeddata_anonymized", replace


//------------------------
//------------------------
// Split up into one sheet per experiment (for excel in-class analyses)

sort treatment

bro id experiment_id experiment_label treatment page /// 
e1_* ///
page_viewingtime total_viewingtime ///
participanttime_started_utc playerbrowser_first playerlast_name playerfirst_name playerstudent_number playerdemographics_age playerdemographics_sex playerdemographics_fininterest playerdemographics_investor playerdemographics_investorhisto playerdemographics_investorexper playerdemographics_financeprof playerdemographics_riskaffinity playerdemographics_percentages playerdemographics_intuition playerdemographics_ideasvsfacts playerdemographics_analysisvsins playerinterest_rate_inflation playerbonds_riskier playerhighest_return_asset playerhighest_fluctuations_asset playerrisk_spreading_money playerstock_mutual_fund playerinvest_mutual_fund playermortgage_payment playersavings_interest playermutual_fund_statement playerbond_purchase playercredit_card_debt playerfaith1 playerfaith2 playerfaith3 playerfaith4 playerfaith5 playerfaith6 playerfaith7 playerfaith8 playerfaith9 playerfaith10 playerfaith11 playerfaith12 playeroverconfidence1 playeroverconfidence2 playeroverconfidence3 /// 
if experiment_id==1
