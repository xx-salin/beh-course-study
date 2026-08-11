
******************* Results by Experiment (preliminary testing)
*** for examining success of each experiment currently





use "Output/responses", clear

* E1 Conjunction fallacy
sum e1_bankteller e1_feministbankteller if experiment_id==1
by treatment, sort: sum e1_bankteller e1_feministbankteller if experiment_id==1
count if e1_feministbankteller>e1_bankteller & experiment_id==1

* E2 Gambler's fallacy
sum e2_heads e2_tails if experiment_id==2
by treatment, sort: sum e2_heads if experiment_id==2
ttest e2_heads==0.5 if experiment_id==2 & treatment==0

* E3 Hot hand fallacy
sum e3_makeshot if experiment_id==3
by treatment, sort: sum e3_makeshot if experiment_id==3
ttest e3_makeshot==0.5 if experiment_id==3

* E4 Disposition effect
sum e4_sellwinner if experiment_id==4
by treatment, sort: sum e4_sellwinner if experiment_id==4
ttest e4_sellwinner==0.5 if experiment_id==4 & treatment==0

* E5 Base rate fallacy (Bayes-correct = .414)
sum e5_pcorrect if experiment_id==5
by treatment, sort: sum e5_pcorrect if experiment_id==5
ttest e5_pcorrect==0.414 if experiment_id==5 & treatment==0
ttest e5_pcorrect==0.414 if experiment_id==5 & treatment==1

* E6 Illusion of control
sum e6_control if experiment_id==6
by treatment, sort: sum e6_control if experiment_id==6
ttest e6_control==0.5 if experiment_id==6

* E7 Anchoring
sum e7_height if experiment_id==7
by treatment, sort: sum e7_height if experiment_id==7
ttest e7_height, by(treatment)

* E8 Hindsight bias
sum e8_successprob if experiment_id==8
by treatment, sort: sum e8_successprob if experiment_id==8
ttest e8_successprob, by(treatment)




* E9 Present bias
sum e9_immediate if experiment_id==9
by treatment, sort: sum e9_immediate if experiment_id==9

* E10 Loss aversion
sum e10_safe if experiment_id==10
by treatment, sort: sum e10_safe if experiment_id==10
ttest e10_safe, by(treatment)

* E11 Endowment effect
sum e11_value if experiment_id==11
by treatment, sort: sum e11_value if experiment_id==11, detail

* E12 Decoy effect
sum e12_target if experiment_id==12
by treatment, sort: sum e12_target if experiment_id==12

* E13 Framing effect
sum e13_safe if experiment_id==13
by treatment, sort: sum e13_safe if experiment_id==13
ttest e13_safe, by(treatment)

* E14 Status quo bias
sum e14_stay if experiment_id==14
by treatment, sort: sum e14_stay if experiment_id==14
ttest e14_stay==0.5 if experiment_id==14

* E15 Sunk cost fallacy
sum e15_sunk if experiment_id==15
by treatment, sort: sum e15_sunk if experiment_id==15
ttest e15_sunk, by(treatment)

* E16 Mental accounting
sum e16_buy if experiment_id==16
by treatment, sort: sum e16_buy if experiment_id==16
ttest e16_buy, by(treatment)





* E17 Ultimatum game
sum e17_offer e17_accept if experiment_id==17
by treatment, sort: sum e17_offer e17_accept if experiment_id==17
ttest e17_offer, by(treatment)
ttest e17_accept, by(treatment)
ttest e17_offer == e17_accept if experiment_id==17

* E18 Dictator game
sum e18_dictator if experiment_id==18
by treatment, sort: sum e18_dictator if experiment_id==18
ttest e18_dictator, by(treatment)

* E19 Trust game
sum e19_send if experiment_id==19
by treatment, sort: sum e19_send if experiment_id==19
ttest e19_send, by(treatment)

* E20 Public goods game
sum e20_contribution if experiment_id==20
by treatment, sort: sum e20_contribution if experiment_id==20
ttest e20_contribution, by(treatment)

* E21 Prisoner's dilemma
sum e21_cooperate if experiment_id==21
by treatment, sort: sum e21_cooperate if experiment_id==21
ttest e21_cooperate, by(treatment)

* E22 Coordination game
tab e22_choice treatment if experiment_id==22, col
sum e22_belief if experiment_id==22
by treatment, sort: sum e22_belief if experiment_id==22
ttest e22_belief, by(treatment)

* E23 Bertrand price
sum e23_price if experiment_id==23
by treatment, sort: sum e23_price if experiment_id==23
ttest e23_price, by(treatment)

* E24 Cournot quantity
sum e24_quantity if experiment_id==24
by treatment, sort: sum e24_quantity if experiment_id==24
ttest e24_quantity, by(treatment)







* E25 SSW market
sum e25_wtp_0-e25_wtp_11 e25_wta_0-e25_wta_11 if experiment_id==25
forvalues i=0/11 {
    ttest e25_wta_`i'==e25_wtp_`i' if experiment_id==25
}

* E26 Wisdom of the crowd
sum e26_michael e26_daniel e26_christoph if experiment_id==26
by treatment, sort: sum e26_michael e26_daniel e26_christoph if experiment_id==26* E26 Wisdom of the crowd
sum e26_michael e26_daniel e26_christoph if experiment_id==26
by treatment, sort: sum e26_michael e26_daniel e26_christoph if experiment_id==26

foreach p in michael daniel christoph {
    display "=== `p' ==="
    sdtest e26_`p' if experiment_id==26, by(treatment)
}






* ============================================
* E27-E30 Counting heuristic
* ============================================

* --- benchmark matched to the display format each subject saw ---
gen benchmark = .
replace benchmark = FrequencyOfOutperformance if treatment==0  
replace benchmark = FrequencyOfLeadership     if treatment==1 
label variable benchmark "Times Asset B beat Asset A (matched to display)"

* which asset the counting heuristic points to (5 = tie, left missing)
gen heur_B = .
replace heur_B = 1 if benchmark > 5 & benchmark < .
replace heur_B = 0 if benchmark < 5
label variable heur_B "Heuristic favours Asset B"

* --- per round: does choice / belief follow the heuristic? ---
forvalues n = 27/30 {

    gen chose_B`n' = .
    replace chose_B`n' = 1 if e`n'_choice=="Asset B"
    replace chose_B`n' = 0 if e`n'_choice=="Asset A"

    gen bel_B`n' = .
    replace bel_B`n' = 1 if e`n'_belief=="Asset B"
    replace bel_B`n' = 0 if e`n'_belief=="Asset A"

    gen match_choice`n' = (chose_B`n'==heur_B) if chose_B`n'<. & heur_B<.
    gen match_belief`n' = (bel_B`n'  ==heur_B) if bel_B`n'  <. & heur_B<.

    display _n "===== ROUND `n' ====="
    ttest match_choice`n' == 0.5 if experiment_id==`n'
    ttest match_belief`n' == 0.5 if experiment_id==`n'

    * does it hold in both display formats?
    ttest match_choice`n' if experiment_id==`n', by(treatment)
}

* --- descriptives ---
sum benchmark FrequencyOfOutperformance FrequencyOfLeadership if experiment_id>=27 & experiment_id<=30
tab heur_B treatment if experiment_id>=27 & experiment_id<=30, col

* how often the two benchmarks disagree (the identifying variation)
gen disagree = (FrequencyOfOutperformance>5) != (FrequencyOfLeadership>5)
tab disagree if experiment_id>=27 & experiment_id<=30

* --- "Same Expected Return" is dropped above; report its rate separately ---
forvalues n = 27/30 {
    tab e`n'_belief if experiment_id==`n'
}





* E31 Deterministic mirror
tab e31_box1 treatment if experiment_id==31, col

* E32 Insurance plan
tab e32_insurance treatment if experiment_id==32, col chi2
