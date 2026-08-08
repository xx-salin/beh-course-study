*-----------------------------------------------
* Load Excel file
*-----------------------------------------------
import excel "Input/rCum_distributions_new.xlsx", firstrow clear

* Columns A–J = Asset A returns
* Columns K–T = Asset B returns

* ==== 2. Frequency of Outperformance (annual) ====
gen FrequencyOfOutperformance = 0
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (K > A)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (L > B)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (M > C)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (N > D)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (O > E)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (P > F)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (Q > G)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (R > H)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (S > I)
replace FrequencyOfOutperformance = FrequencyOfOutperformance + (T > J)

* ==== 3. Cumulative returns for Frequency of Leadership ====
gen cumretA1 = A
gen cumretB1 = K

gen cumretA2 = (1 + cumretA1) * (1 + B) - 1
gen cumretB2 = (1 + cumretB1) * (1 + L) - 1

gen cumretA3 = (1 + cumretA2) * (1 + C) - 1
gen cumretB3 = (1 + cumretB2) * (1 + M) - 1

gen cumretA4 = (1 + cumretA3) * (1 + D) - 1
gen cumretB4 = (1 + cumretB3) * (1 + N) - 1

gen cumretA5 = (1 + cumretA4) * (1 + E) - 1
gen cumretB5 = (1 + cumretB4) * (1 + O) - 1

gen cumretA6 = (1 + cumretA5) * (1 + F) - 1
gen cumretB6 = (1 + cumretB5) * (1 + P) - 1

gen cumretA7 = (1 + cumretA6) * (1 + G) - 1
gen cumretB7 = (1 + cumretB6) * (1 + Q) - 1

gen cumretA8 = (1 + cumretA7) * (1 + H) - 1
gen cumretB8 = (1 + cumretB7) * (1 + R) - 1

gen cumretA9 = (1 + cumretA8) * (1 + I) - 1
gen cumretB9 = (1 + cumretB8) * (1 + S) - 1

gen cumretA10 = (1 + cumretA9) * (1 + J) - 1
gen cumretB10 = (1 + cumretB9) * (1 + T) - 1

* ==== 4. Frequency of Leadership (cumulative) ====
gen FrequencyOfLeadership = 0
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB1 > cumretA1)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB2 > cumretA2)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB3 > cumretA3)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB4 > cumretA4)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB5 > cumretA5)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB6 > cumretA6)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB7 > cumretA7)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB8 > cumretA8)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB9 > cumretA9)
replace FrequencyOfLeadership = FrequencyOfLeadership + (cumretB10 > cumretA10)

gen row_to_use = _n - 1

* ==== 5. Keep only relevant columns ====
keep row_to_use FrequencyOfOutperformance FrequencyOfLeadership

* ==== 6. Save as .dta for merging ====
save "Input/returns_summary.dta", replace
